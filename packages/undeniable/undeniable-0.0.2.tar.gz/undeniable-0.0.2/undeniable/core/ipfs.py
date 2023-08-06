import ipfshttpclient

class IPFSClient(object):
	"""docstring for ipfs_client"""
	def __init__(self):
		super(IPFSClient, self).__init__()
		# self.client = ipfshttpclient.connect('/dns/ipfs.infura.io/tcp/5001/https')
		self.client = ipfshttpclient.connect()

	def add_new_item(self, prior, data, nonce):
		blob = {
		    "prior": prior,
		    "nonce": nonce,
		    "data": data
		}
		cid = self.client.add_json(blob)
		return cid

	def add_nft_reveal_key(self, data):
		cid = self.client.add_json(data)
		return cid

	def add_nft_artifact(self, data):
		cid = self.client.add_json(data)
		return cid

	def add_content_blob(self, data):
		cid = self.client.add_bytes(data)
		return cid

	def fetch_item(self, cid):
		result = self.client.get_json(cid)
		return result