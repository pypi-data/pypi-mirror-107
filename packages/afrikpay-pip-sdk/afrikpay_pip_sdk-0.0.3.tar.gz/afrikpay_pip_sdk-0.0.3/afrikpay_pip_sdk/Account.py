import requests, hashlib

class Account:
    def __init__(
        self,
        agentId,
        agentPlatform,
        apiKey,
        transactionStatusUrl = 'http://35.204.26.22:8086/api/account/transaction/status/',
        balanceUrl = 'http://35.204.26.22:8086/api/account/agent/balance/v2/',
        changeKeyUrl = 'http://35.204.26.22:8086/api/account/developer/changekey/'
    ):
        self.agentId = agentId
        self.agentPlatform = agentPlatform
        self.apiKey = apiKey
        self.transactionStatusUrl = transactionStatusUrl
        self.balanceUrl = balanceUrl
        self.changeKeyUrl = changeKeyUrl

    def __repr__(self):
        return str(self.agentId + " - " + self.apiKey)

    def balance(self):
        hash = hashlib.md5((str(self.agentId) + str(self.apiKey)).encode()).hexdigest()
        params = {
            'agentid': self.agentId,
            'agentplatform': self.agentPlatform,
            'hash': hash
        }
        response = requests.post(url = self.balanceUrl, params = params)
        return response.json()

    def changeKey(self):
        params = {
            'agentid': self.agentId,
            'apiKey': self.agentPlatform
        }
        response = requests.post(url = self.changeKeyUrl, params = params)
        return response.json()

    def transactionStatus(self,transactionId):
        params = {
            'transactionid': transactionId
        }
        response = requests.post(url = self.transactionStatusUrl, params = params)
        return response.json()

