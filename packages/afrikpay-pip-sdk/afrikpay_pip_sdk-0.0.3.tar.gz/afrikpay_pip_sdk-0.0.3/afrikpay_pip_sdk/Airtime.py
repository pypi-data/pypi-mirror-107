import requests, hashlib

class Airtime:
    def __init__(
        self,
        agentId,
        agentPlatform,
        apiKey,
        agentPassword = '',
        airtimeUrl = 'http://35.204.26.22:8086/api/airtime/v2/',
        airtimeStatusUrl = 'http://35.204.26.22:8086/api/airtime/status/v2/'):
        
        self.agentId = agentId
        self.agentPlatform = agentPlatform
        self.apiKey = apiKey
        self.agentPassword = hashlib.md5((str(agentPassword)).encode()).hexdigest()

        self.airtimeUrl = airtimeUrl
        self.airtimeStatusUrl = airtimeStatusUrl

    def __repr__(self):
        return str(self.agentId + " - " + self.apiKey)

    def makeAirtime(
        self,
        operator,
        reference,
        amount,
        mode,
        processingNumber = ''):

        hash = hashlib.md5((str(operator) + str(reference) + str(amount) + str(self.apiKey)).encode()).hexdigest()

        params = {
            'operator': operator,
            'reference': reference,
            'amount': amount,
            'mode': mode,
            'agentid': self.agentId,
            'agentplatform': self.agentPlatform,
            'agentpwd': self.agentPassword,
            'hash': hash,
            'processingnumber': processingNumber
        }

        response = requests.post(url = self.airtimeUrl, params = params)
        return response.json()

    def airtimeStatus(self, processingNumber):
        hash = hashlib.md5((str(processingNumber) + str(self.apiKey)).encode()).hexdigest()
        params = {
            'processingnumber': processingNumber,
            'agentplatform': self.agentPlatform,
            'agentid': self.agentId,
            'hash': hash,
        }

        response = requests.post(url = self.airtimeStatusUrl, params = params)
        return response.json()


