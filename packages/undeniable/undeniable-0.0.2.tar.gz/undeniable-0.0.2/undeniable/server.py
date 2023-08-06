# native
import json
import logging
import json

# server related
from aiohttp import web
import aiohttp_cors

import rocksdb

from undeniable.core.solana import get_blocktime, get_memo_text
from undeniable.protocol.undeniable import Undie

##### should move out of here
class Logger:
    def __init__(self, file, level=logging.DEBUG):
        logging.basicConfig(
            filename=file,
            format="[%(levelname)s] %(asctime)s: %(message)s",
            level=level,
        )

    def debug(self, msg):
        logging.debug(msg)

    def info(self, msg):
        logging.info(msg)

    def warn(self, msg):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)

    def critical(self, msg):
        logging.critical(msg)


class Server:
    def __init__(self, port, logger, ipfsclient, solanaclient):
        self._port = port

        self.ipfsclient = ipfsclient
        self.client = solanaclient
        self.db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
        # self.user_datastore = rocksdb.DB("users.db", rocksdb.Options(create_if_missing=True))

        app = web.Application(client_max_size=10 * 100 * 100 * 100)

        app.router.add_route("POST", "/mint", self._mint_nft_new)
        app.router.add_route("POST", "/lookup", self._lookup_user_by_lookupkey)
        app.router.add_route("POST", "/nfts", self._resolve_undeniable_nfts_full)
        app.router.add_route("POST", "/reveal", self._reveal_nft)

        cors = aiohttp_cors.setup(
            app,
            defaults={
                "https://app.undeniable.link": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers=("X-Requested-With", "Content-Type", "content-type"),
                    allow_methods="*",
                    max_age=3600,
                ),
                "http://localhost:3000": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers=("X-Requested-With", "Content-Type", "content-type"),
                    allow_methods="*",
                    max_age=3600,
                ),
            },
        )

        [cors.add(route) for route in list(app.router.routes())]

        self._app = app
        self._logger = logger

    async def _mint_nft_new(self, request):
        request_body_json = await request.text()
        body = json.loads(request_body_json)

        # sever data
        target_wallet = body.get("wallet")

        # encryption data
        is_encrypted = body.get("is_encrypted")
        # encryption = body.get("encryption")
        json_key = {"k": "42xeO1N-6Gb70fGAPVbGuc4f2xxLK1i-Y4VWGhnfx20", "kty": "oct"}

        # content
        encoding = body.get("content").get("encoding")
        rtype = body.get("content").get("type")
        raw = body.get("content").get("raw")

        # meta
        title = body.get("meta").get("title")
        shortname = body.get("meta").get("shortname")
        mediatype = body.get("meta").get("type")

        undie = Undie()
        (output_tx_sig, cid_to_store, token, key) = undie.mint_new_nft(
            ipfsclient=self.ipfsclient,
            solana_client=self.client,
            is_encrypted=is_encrypted,
            encoding=encoding,
            rtype=rtype,
            raw_data=raw,
            title=title,
            shortname=shortname,
            mediatype=mediatype,
            target_wallet=target_wallet,
            json_key=json_key,
        )

        response = {
            "solana_signature": output_tx_sig,
            "ipfs_location": cid_to_store,
            "token_address": token,
            "key": key,
        }
        return web.Response(
            status=200,
            text=json.dumps(response, default=str),
            content_type="application/json",
        )

    async def _reveal_nft(self, request):
        request_body_json = await request.text()
        body = json.loads(request_body_json)

        toke = body.get("nft")
        key = body.get("key")
        # serialized_key = json.dumps(body.get("key"))

        un = Undie()
        (cid, output_tx_sig, tomakepublic) = un.store_key_in_ipfs_and_record_on_chain(
            toke=toke, key=key, client=self.client, ipfsclient=self.ipfsclient
        )

        output = {
            "key": cid,
            "solana_signature": output_tx_sig,
            "content": tomakepublic,
        }

        return web.Response(
            status=200,
            text=json.dumps(output, default=str),
            content_type="application/json",
        )

    async def _resolve_undeniable_nfts_full(self, request):
        request_body_json = await request.text()
        body = json.loads(request_body_json)
        toke = body.get("pubkey")

        un = Undie()
        resolved_tokens = un.resolve_all_undeniable_tokens(
            address=toke, client=self.client, ipfsclient=self.ipfsclient
        )

        return web.Response(
            status=200,
            text=json.dumps(resolved_tokens, default=str),
            content_type="application/json",
        )

    async def _lookup_user_by_lookupkey(self, request):
        print("_lookup_user_by_lookupkey")
        request_body_json = await request.text()
        body = json.loads(request_body_json)
        print("HERE")
        # print(body)
        if body.get("type") == "username":
            username = body.get("username")
            print(f"username: {username}")

            key = f"username::{username}"
            result = self.db.get(key.encode("utf-8"))
            print(result)

            if result is None:
                print("adding new value")
                self.db.put(key.encode("utf-8"), json.dumps(body).encode("utf-8"))

            else:
                print("response body username")
                return web.Response(
                    status=200,
                    text=json.dumps(json.loads(result.decode()), default=str),
                    # content_type="application/json",
                )

        if body.get("type") == "lookupKey":
            lookup_key = body.get("lookupKey")
            print(f"lookupKey: {lookup_key}")

            key = f"lookupKey::{lookup_key}"
            result = self.db.get(key.encode("utf-8"))
            print(result)

            if result is None:
                print("adding new value")
                self.db.put(key.encode("utf-8"), json.dumps(body).encode("utf-8"))

            else:
                print("response body lookup")
                return web.Response(
                    status=200,
                    text=json.dumps(json.loads(result.decode()), default=str),
                    # content_type="application/json",
                )

        return web.Response(
            status=200,
            text=json.dumps(body, default=str),
            # content_type="application/json",
        )

    def run(self):
        self._logger.info("Starting server")
        web.run_app(self._app, port=self._port)
