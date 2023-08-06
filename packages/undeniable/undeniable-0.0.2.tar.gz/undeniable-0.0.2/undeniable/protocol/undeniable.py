import json
from pathlib import Path

from jwcrypto import jwk, jwe
from jwcrypto.common import json_encode

from jsonschema import validate

from undeniable.core.solana import (
    get_blocktime,
)


class Undie:
    def __init__(self):
        path = f"{Path(__file__).resolve().parent}/spec.json"
        self.spec = json.load(open(path))

    def resolve_all_undeniable_tokens(self, address, client, ipfsclient):

        tokens = client.get_users_token_accounts_full(address)

        resolved_tokens = []
        for key, value in tokens.items():
            # print(value)

            (mint_sig, mint_cid) = value.get("mint")

            (reveal_sig, reveal_cid, reveal_item) = None, None, None
            if "reveal" in value:
                (reveal_sig, reveal_cid) = value.get("reveal")

            mint_item = ipfsclient.fetch_item(mint_cid)

            if reveal_cid != None:
                # reveal_item = self.ipfsclient.fetch_item(reveal_cid)
                try:
                    print("fetching from IPFS")
                    reveal_item = ipfsclient.fetch_item(reveal_cid).get("key")
                    print(reveal_item)
                except Exception as e:
                    print("Fetching from Solana")
                    reveal_cid = reveal_cid.replace("\\", "")
                    reveal_item = json.loads(reveal_cid)
                    print(reveal_item)

            if reveal_item != None:

                serialized_key = json.dumps(reveal_item)
                serialized_enc = json.dumps(mint_item.get("content").get("raw"))

                # if 'spec' in item:
                #     if item.get('spec') == 'Qmi...dfg':

                undie = Undie()
                val = b"failed"
                try:
                    val = undie.decrypt_nft_artifact(
                        enc=serialized_enc, key=serialized_key
                    )
                except Exception as e:
                    pass

                mint_item["content"]["raw"] = val.decode()
                mint_item["is_encrypted"] = False

            output = {
                "item": mint_item,
                "addr": key,
                "memo": mint_cid,
                "reveal_cid": reveal_cid,
            }
            resolved_tokens.append(output)
        return resolved_tokens

    def store_key_in_ipfs_and_record_on_chain(self, toke, key, client, ipfsclient):
        txs = client.solana_client.get_confirmed_signature_for_address2(toke).get(
            "result"
        )
        nft_minting_signature = txs[0].get("signature")

        # examine the minting transaction
        tx = client.solana_client.get_confirmed_transaction(nft_minting_signature)

        # parse keys from tx
        account_keys = (
            tx.get("result").get("transaction").get("message").get("accountKeys")
        )
        (issuer, token_account, token_addr, _, owner_addr) = account_keys[0:5]

        print("should write reveal to ipfs")

        # add key content to IPFS
        tomakepublic = {"prior": nft_minting_signature, "key": key}

        cid = ipfsclient.add_nft_reveal_key(tomakepublic)

        output = client.null_ransfer_token(
            token_key=toke, token_associated=token_account, dest=owner_addr, data=cid
        )
        output_tx_sig = output.get("result")

        print(f"Wrote to chain at:\t\t{output_tx_sig}")
        return (cid, output_tx_sig, tomakepublic)

    def validate_nft_artifact(self, data):
        # data = {
        #     "spec": "Qmi...dfg",
        #     "minter": None,
        #     "jwe": None,
        #     "is_encrypted": False,
        #     "content": {
        #         "cid": None,
        #         "type": "raw",
        #         "encoding": "base64",
        #         "raw": "data:image/png;base64,iVBORw0KGgoAA....AAAAASUVORK5CYII="
        #     },
        #     "meta": {
        #         "title": "My Fire Anchor",
        #         "shortname": "FIREA",
        #         "mediatype": "image"
        #     }
        # }
        is_valid = False

        try:
            validate(instance=data, schema=self.spec)
            is_valid = True
        except Exception as e:
            # raise e
            pass
        finally:
            pass

        print("Yay! its valid")

    def build_nft_artifact(self):
        return

    def build_encrypted_nft_artifact(self, payload, json_key):
        # key = jwk.JWK.generate(kty='oct', size=256)
        key = jwk.JWK().from_json(json.dumps(json_key))

        headers = {"alg": "A256KW", "enc": "A256CBC-HS512"}
        # payload = "My Encrypted message"
        jwetoken = jwe.JWE(payload.encode("utf-8"), json_encode(headers))
        jwetoken.add_recipient(key)
        enc = json.loads(jwetoken.serialize())
        key = json.loads(key.export())
        return (headers, key, enc)

    def decrypt_nft_artifact(self, enc, key):

        jkey = jwk.JWK().from_json(key)
        jwetoken = jwe.JWE()
        jwetoken.deserialize(enc)
        jwetoken.decrypt(jkey)
        payload = jwetoken.payload
        return payload

    def mint_new_nft(
        self,
        ipfsclient,
        solana_client,
        is_encrypted,
        encoding,
        rtype,
        raw_data,
        title,
        shortname,
        mediatype,
        target_wallet,
        json_key,
    ):

        print(f"Adding\t\t\t\t{title}")

        # data = {"raw": raw_data, "filename": title, "shortname": shortname}

        # check which spec -  hardcode for now

        # check if encrypted
        # if so add jwe headers and make key? or take key?

        # update encryption key
        # update jwe key

        # check media type
        # check encoding type
        # check if should point or embed

        data = {
            "spec": "Qmi...dfg",
            "minter": {"item": "Minted by undeniable", "nonce": 0},
            "jwe": None,
            "is_encrypted": is_encrypted,
            "content": {
                "cid": None,
                "type": rtype,
                "encoding": encoding,
                "raw": raw_data,
            },
            "meta": {"title": title, "shortname": shortname, "mediatype": mediatype},
        }

        key = None
        if is_encrypted:
            payload = data.get("content").get("raw")
            (headers, key, enc) = self.build_encrypted_nft_artifact(payload, json_key)

            data["jwe"] = headers
            data["content"]["raw"] = enc

        # cid = None
        cid = "Qm..fa"
        if rtype == "ipfs":
            # should upload contents to IPFS

            toupload = data.get("content").get("raw")
            print(toupload)
            # cid = self.upload_content_to_ipfs(toupload)

            #### store json if encrypted
            cid = ipfsclient.add_content_blob(data=json.dumps(toupload).encode("utf-8"))

            # data["jwe"] = headers
            data["content"]["raw"] = None
            data["content"]["cid"] = cid
        elif rtype == "embed":
            pass
        else:
            print("not a valid option")
            return

        is_valid = self.validate_nft_artifact(data)
        print(is_valid)
        print(key)
        # print(json.dumps(data, indent=4))

        # # cid_to_store = ipfsclient.add_new_item(prior="", data=data, nonce=None)
        cid_to_store = ipfsclient.add_nft_artifact(data=data)

        print(f"Stored data at:\t\t\t{cid_to_store}")

        # # # write the CID to chain
        (output, token) = solana_client.write_memo_mint_to_other(
            cid_to_store, target_wallet
        )
        output_tx_sig = output.get("result")
        transaction = solana_client.fetch_transaction(output_tx_sig)
        blocktime = get_blocktime(transaction)
        print(f"Blocktime:\t\t\t{blocktime}")
        print(f"Wrote to chain at:\t\t{output_tx_sig}")
        return (output_tx_sig, cid_to_store, token, key)
