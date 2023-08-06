# solana core
import solana.rpc.types as types
import solana.system_program as sp
import spl.token.instructions as spl_token

from solana.rpc.api import Client
from solana.account import Account
from solana.transaction import AccountMeta, Transaction, TransactionInstruction
from solana.blockhash import Blockhash
from solana.publickey import PublicKey

# solana program lib
from spl.token._layouts import ACCOUNT_LAYOUT, MINT_LAYOUT
from spl.token.constants import TOKEN_PROGRAM_ID

# native
from operator import itemgetter

import datetime
import time
import re
import json

# for caching
import rocksdb

class SolanaClient(object):
    """docstring for solana_client"""

    def __init__(self):
        super(SolanaClient, self).__init__()
        self.memo_program_id = "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr"
        # self.solana_client = Client("https://devnet.solana.com")
        # self.network = "https://testnet.solana.com"
        self.network = "https://devnet.solana.com"
        self.solana_client = Client(self.network)
        self.acc = None
        assert self.solana_client.is_connected(), True


        # databases for caching confirmed TX's
        self.cache = rocksdb.DB("solana_cache.db", rocksdb.Options(create_if_missing=True))
        self.txcache = rocksdb.DB("solana_tx_cache.db", rocksdb.Options(create_if_missing=True))

    def set_account(self, key32bytes):
        # check that private key material is correct length
        if len(key32bytes) != 32:
            return
        self.acc = Account(secret_key=key32bytes)

    def get_money(self, amount):
        # wrapped airdrop method
        print(f"Get dat money\t\t\t{amount}")
        results = self.solana_client.request_airdrop(
            self.acc.public_key(), amount * 1000000000
        )
        print(results)

    def get_users_token_accounts(self, pubkey):
        results = self.solana_client.get_token_accounts_by_owner(
            owner=pubkey,
            opts=types.TokenAccountOpts(
                program_id=TOKEN_PROGRAM_ID, encoding="jsonParsed"
            ),
        )

        tokens = results.get("result").get("value")

        accounts = {}
        for t in tokens:
            acc = t.get("account").get("data").get("parsed")
            tok_acc = acc.get("info").get("mint")
            tok_amt = acc.get("info").get("tokenAmount").get("amount")


            # check if we have this cachec!

            cache_result = self.cache.get(tok_acc.encode("utf-8"))

            if cache_result is not None:
                cache_result = json.loads(cache_result.decode())
                accounts[tok_acc] = cache_result
                print(f"TKN::\t{tok_acc}:\tfound in cache!")
                continue

            txs = self.solana_client.get_confirmed_signature_for_address2(tok_acc).get(
                "result"
            )

            print(f"you got {len(txs)} txs")
            most_recent = txs[-1]
            sig = most_recent.get("signature")

            tx = self.solana_client.get_confirmed_transaction(sig)

            memo = get_memo_text(tx)

            tkn_value = {
                "addr": tok_acc,
                "amt": tok_amt,
                "memo": memo,
            }

            # add to cache
            print(f"TKN::\t{tok_acc}:\taddeing to cache!")
            self.cache.put(tok_acc.encode("utf-8"), json.dumps(tkn_value).encode("utf-8"))


            accounts[tok_acc] = tkn_value

        return accounts

    def get_users_token_accounts_full(self, pubkey):

        # should check if this is a duped token account
        # if it is we should check if its after the first one
        # we should check that it conforms to a key TX
        # we should check if it contains an IPFS hash
        # we should resolve and check that it is a valid key
        # we should then resolve the key
        # we should resolve the NFT and show the un encrypted one


        results = self.solana_client.get_token_accounts_by_owner(
            owner=pubkey,
            opts=types.TokenAccountOpts(
                program_id=TOKEN_PROGRAM_ID, encoding="jsonParsed"
            ),
        )

        tokens = results.get("result").get("value")
        unique_keys = list(set([t.get("account").get("data").get("parsed").get("info").get("mint") for t in tokens]))
        signature_reformatted = {}

        accounts_described = {}

        for uk in unique_keys:
            key = uk.encode("utf-8")

            tx_values = self.solana_client.get_confirmed_signature_for_address2(uk).get(
                "result"
            )

            sorted_transactions = sorted(tx_values, key=itemgetter('blockTime')) 
            
            for index, transaction in enumerate(sorted_transactions):
                # check if the tx is a mint
                is_mint = False
                is_key = False

                sig = transaction.get("signature")
                cache_result = self.txcache.get(sig.encode("utf-8"))

                if cache_result is None:
                    tx = self.solana_client.get_confirmed_transaction(sig)
                    self.txcache.put(sig.encode("utf-8"), json.dumps(tx).encode("utf-8"))
                else:
                    tx = json.loads(cache_result.decode())

                instructions = tx.get("result").get("transaction").get("message").get("instructions")
                log_messages = tx.get("result").get("meta").get("logMessages")

                memo = get_memo_text(tx)

                if len(instructions) == 7: # has correct number of instructions
                    if memo.startswith("Qm"): # is an IPFS base58 hash
                        if index == 0: # only if this is the first TX
                            is_mint = True

                if len(instructions) == 3: # has correct number of instructions
                    # if memo.startswith("Qm"): # is an IPFS base58 hash
                    if index > 0: # only if this is the first TX
                        is_key = True

                # should only have one key - if key exists then cancel the next one
                # eariest is best

                if uk not in accounts_described:
                    accounts_described[uk] = {}

                if is_mint:
                    accounts_described[uk]["mint"] = (sig, memo)
                elif is_key:
                    accounts_described[uk]["reveal"] = (sig, memo)
                else:
                    if "other" not in accounts_described[uk]:
                        accounts_described[uk]["other"] = []
                    accounts_described[uk]["other"].append((sig, memo))

                # stop looking if we have both a mint and key
                if "mint" in accounts_described[uk]:
                    if accounts_described[uk]["mint"] is not None: 
                        if "reveal" in accounts_described[uk]:
                            if accounts_described[uk]["reveal"] is not None: 
                                break

        return accounts_described

    def transfer_token(self, token_key, token_associated, dest, amount=1, fund=False):
        recent_blockhash = self.solana_client.get_recent_blockhash()

        recent_blockhash_value = Blockhash(
            recent_blockhash["result"]["value"]["blockhash"]
        )
        print(f"Recent blockhash\t\t{recent_blockhash_value}")

        size_account_layout = ACCOUNT_LAYOUT.sizeof()
        balance_needed = self.solana_client.get_minimum_balance_for_rent_exemption(size_account_layout).get("result")

        print(f"Balance needed\t\t\t{balance_needed}")

        txn = Transaction()
        txn.recent_blockhash = recent_blockhash_value
        nft_public_key = PublicKey(token_key)
        new_account = Account()
        signers = [self.acc, new_account]
        pk = PublicKey(dest)

        print(f"Des public key {pk}")
        print(f"New account: {new_account.public_key()}")

        # create new account
        new_account_tx_inst = sp.create_account(
            sp.CreateAccountParams(
                from_pubkey=self.acc.public_key(),
                new_account_pubkey=new_account.public_key(),
                lamports=balance_needed,
                space=ACCOUNT_LAYOUT.sizeof(),
                program_id=TOKEN_PROGRAM_ID,
            )
        )

        # convert account into token account for specific NFT
        init_acc = spl_token.initialize_account(
            spl_token.InitializeAccountParams(
                account=new_account.public_key(),
                mint=nft_public_key,
                owner=PublicKey(dest),
                program_id=TOKEN_PROGRAM_ID,
            )
        )

        transfer_inst = spl_token.transfer(
            spl_token.TransferParams(
                program_id=TOKEN_PROGRAM_ID,
                source=PublicKey(token_associated),
                dest=new_account.public_key(),
                owner=self.acc.public_key(),
                amount=1,
                signers=[],
            )
        )

        [
            txn.add(tx_instr)
            for tx_instr in [
                new_account_tx_inst,
                init_acc,
                transfer_inst,
            ]
        ]
        print(f"Instructions added\t\t✅")

        # signed by all accounts
        txn.sign(*signers)

        print(f"Signers signed\t\t\t✅")

        print(txn)

        output = self.solana_client.send_raw_transaction(txn.serialize())
        return output

    def null_ransfer_token(self, token_key, token_associated, dest, data, amount=1, fund=False):
        recent_blockhash = self.solana_client.get_recent_blockhash()

        recent_blockhash_value = Blockhash(
            recent_blockhash["result"]["value"]["blockhash"]
        )
        print(f"Recent blockhash\t\t{recent_blockhash_value}")

        size_account_layout = ACCOUNT_LAYOUT.sizeof()
        balance_needed = self.solana_client.get_minimum_balance_for_rent_exemption(size_account_layout).get("result")

        print(f"Balance needed\t\t\t{balance_needed}")

        txn = Transaction()
        txn.recent_blockhash = recent_blockhash_value
        nft_public_key = PublicKey(token_key)
        new_account = Account()
        signers = [self.acc, new_account]
        pk = PublicKey(dest)

        print(f"Des public key {pk}")
        print(f"New account: {new_account.public_key()}")


        # write a memo with hash
        txinst = TransactionInstruction(
            keys=[
                AccountMeta(
                    pubkey=self.acc.public_key(), is_signer=True, is_writable=True
                ),
            ],
            program_id=self.memo_program_id,
            data=data,
        )

        # create new account
        new_account_tx_inst = sp.create_account(
            sp.CreateAccountParams(
                from_pubkey=self.acc.public_key(),
                new_account_pubkey=new_account.public_key(),
                lamports=balance_needed,
                space=ACCOUNT_LAYOUT.sizeof(),
                program_id=TOKEN_PROGRAM_ID,
            )
        )

        # convert account into token account for specific NFT
        init_acc = spl_token.initialize_account(
            spl_token.InitializeAccountParams(
                account=new_account.public_key(),
                mint=nft_public_key,
                owner=PublicKey(dest),
                program_id=TOKEN_PROGRAM_ID,
            )
        )

        [
            txn.add(tx_instr)
            for tx_instr in [
                txinst,
                new_account_tx_inst,
                init_acc,
            ]
        ]
        print(f"Instructions added\t\t✅")

        # signed by all accounts
        txn.sign(*signers)

        print(f"Signers signed\t\t\t✅")

        print(txn)

        output = self.solana_client.send_raw_transaction(txn.serialize())
        return output

    def write_memo_mint_to_other(self, data, dest):

        if self.acc is None:
            print("please set account first")
            return

        decimals = 0
        mint_account = Account()
        new_account = Account()
        signers = [self.acc, mint_account, new_account]

        signer_names = ["Account", "Token", "Special"]
        [
            print(f"{signer_names[i]}\t\t\t\t{s.public_key()}")
            for i, s in enumerate(signers)
        ]

        recent_blockhash = self.solana_client.get_recent_blockhash()

        recent_blockhash_value = Blockhash(
            recent_blockhash["result"]["value"]["blockhash"]
        )
        print(f"Recent blockhash\t\t{recent_blockhash_value}")

        balance_needed = self.solana_client.get_minimum_balance_for_rent_exemption(
            ACCOUNT_LAYOUT.sizeof()
        ).get("result")

        print(f"Balance needed\t\t\t{balance_needed}")

        txn = Transaction()
        txn.recent_blockhash = recent_blockhash_value

        # write a memo with hash
        txinst = TransactionInstruction(
            keys=[
                AccountMeta(
                    pubkey=self.acc.public_key(), is_signer=True, is_writable=True
                ),
            ],
            program_id=self.memo_program_id,
            data=data,
        )

        # create account which is the NFT
        account_tx_inst = sp.create_account(
            sp.CreateAccountParams(
                from_pubkey=self.acc.public_key(),
                new_account_pubkey=mint_account.public_key(),
                lamports=balance_needed,
                space=MINT_LAYOUT.sizeof(),
                program_id=TOKEN_PROGRAM_ID,
            )
        )

        # allow owner to mint new token
        mint_tx_inst = spl_token.initialize_mint(
            spl_token.InitializeMintParams(
                program_id=TOKEN_PROGRAM_ID,
                mint=mint_account.public_key(),
                decimals=decimals,
                mint_authority=self.acc.public_key(),
                freeze_authority=None,
            )
        )

        ######
        # create new account
        new_account_tx_inst = sp.create_account(
            sp.CreateAccountParams(
                from_pubkey=self.acc.public_key(),
                new_account_pubkey=new_account.public_key(),
                lamports=balance_needed,
                space=ACCOUNT_LAYOUT.sizeof(),
                program_id=TOKEN_PROGRAM_ID,
            )
        )

        # convert account into token account for specific NFT
        init_acc = spl_token.initialize_account(
            spl_token.InitializeAccountParams(
                account=new_account.public_key(),
                mint=mint_account.public_key(),
                owner=PublicKey(dest),
                program_id=TOKEN_PROGRAM_ID,
            )
        )

        # mint the only token to this special account
        mint_to = spl_token.mint_to(
            spl_token.MintToParams(
                program_id=TOKEN_PROGRAM_ID,
                mint=mint_account.public_key(),
                dest=new_account.public_key(),
                mint_authority=self.acc.public_key(),
                amount=1,
                signers=[],
            )
        )
        #####

        # remove ability to mint more tokens
        set_authority_tx_inst = spl_token.set_authority(
            spl_token.SetAuthorityParams(
                program_id=TOKEN_PROGRAM_ID,
                account=mint_account.public_key(),
                authority=spl_token.AuthorityType.MINT_TOKENS,
                current_authority=self.acc.public_key(),
                new_authority=None,
                signers=[],
            )
        )

        [
            txn.add(tx_instr)
            for tx_instr in [
                txinst,
                account_tx_inst,
                mint_tx_inst,
                new_account_tx_inst,
                init_acc,
                mint_to,
                set_authority_tx_inst,
            ]
        ]
        print(f"Instructions added\t\t✅")

        # signed by all accounts
        txn.sign(*signers)

        print(f"Signers signed\t\t\t✅")

        output = self.solana_client.send_raw_transaction(txn.serialize())
        return (output, mint_account.public_key())

    def fetch_transaction(self, solana_sig):
        transaction = None
        max_retries, i = 10, 0
        while i <= max_retries:
            # print(f"try count: {i}")
            transaction = self.solana_client.get_confirmed_transaction(solana_sig)
            if transaction.get("result") != None:
                break
            i += 1
            time.sleep(2)
        return transaction


def first_item_or_default(_list, _default):
    return next(iter(_list), _default)


def get_memo_text(transaction):
    parsed_memo = ""
    for log in transaction.get("result").get("meta").get("logMessages"):
        if log.startswith("Program log: Memo "):
            parsed_memo = re.sub("Program log: Memo \(len .*\): ", "", log)
            parsed_memo = parsed_memo[1:-1]  # remove "'s
            break

    return parsed_memo


def get_blocktime(transaction):
    ms = transaction.get("result").get("blockTime")
    as_datetime = datetime.datetime.fromtimestamp(ms)
    return as_datetime


def get_signer(transaction):
    first_signer = first_item_or_default(
        transaction.get("result").get("transaction").get("message").get("accountKeys"),
        "",
    )
    return first_signer
