import requests, hashlib

class Bill:
    def __init__(
        self,
        agentId, 
        agentPlatform, 
        apiKey,
        agentPassword = '',
        billUrl = 'http://35.204.26.22:8086/api/bill/v2/',
        billAmountUrl = 'http://35.204.26.22:8086/api/bill/getamount/',
        billStatusUrl = 'http://35.204.26.22:8086/api/bill/status/v2/'
    ):
        self.agentId= agentId
        self.agentPlatform = agentPlatform
        self.billUrl = billUrl
        self.agentPassword = hashlib.md5((str(agentPassword)).encode()).hexdigest()
        self.billAmountUrl = billAmountUrl
        self.billStatusUrl = billStatusUrl
        self.apiKey = apiKey

    def __repr__(self):
        return str(self.store + " - " + self.apiKey)

    def payBill(
        self,
        biller,
        billid,
        amount,
        mode,
        processingNumber = ''
    ):
        hash = hashlib.md5((str(biller) + str(billid) + str(amount) + str(self.apiKey)).encode()).hexdigest()

        params = {
            'biller': biller,
            'billid': billid,
            'amount': amount,
            'mode': mode,
            'agentid': self.agentId,
            'agentplatform': self.agentPlatform,
            'agentpwd': self.agentPassword,
            'hash': hash,
            'processingnumber': processingNumber
        }

        response = requests.post(url = self.billUrl, params = params)
        return response.json()

    def getBillAmount(
        self,
        biller,
        billid):

        hash = hashlib.md5((str(biller) + str(billid) + str(self.apiKey)).encode()).hexdigest()

        params = {
            'biller': biller,
            'billid': billid,
            'agentid': self.agentId,
            'hash': hash
        }

        response = requests.post(url = self.billAmountUrl, params = params)
        return response.json()


    def getBillStatus(
        self,
        processingNumber = ''):

        hash = hashlib.md5((str(processingNumber) + str(self.apiKey)).encode()).hexdigest()

        params = {
            'agentid': self.agentId,
            'agentplatform': self.agentPlatform,
            'processingnumber': processingNumber,
            'hash': hash
        }

        response = requests.post(url = self.billStatusUrl, params = params)
        return response.json()



