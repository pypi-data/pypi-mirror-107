import requests, hashlib

class Ecommerce:
    def __init__(
        self,
        store,
        apiKey,
        secretCode = '',
        collectUrl = 'http://35.204.26.22:8086/api/ecommerce/collect/',
        payoutUrl = 'http://35.204.26.22:8086/api/ecommerce/payout/',
        depositUrl = 'http://35.204.26.22:8086/api/ecommerce/deposit/',
        changeKeyUrl = 'http://35.204.26.22:8086/api/ecommerce/changekey/',
        transactionStatusUrl = 'http://35.204.26.22:8086/api/ecommerce/transaction/status/',
        acceptUrl = '',
        cancelUrl = '',
        declineUrl = '',
        notifyUrl = ''):

        self.store = store
        self.apiKey = apiKey
        self.secretCode = secretCode
        self.collectUrl = collectUrl
        self.payoutUrl = payoutUrl
        self.depositUrl = depositUrl
        self.changeKeyUrl = changeKeyUrl
        self.transactionStatusUrl = transactionStatusUrl
        self.acceptUrl = acceptUrl
        self.cancelUrl = cancelUrl
        self.declineUrl = declineUrl
        self.notifyUrl = notifyUrl

    def collect(
        self,
        provider,
        reference,
        amount,
        code = '',
        purchaseRef = '',
        description = ''):

        if provider == 'mtn_mobilemoney_cm':
            return self.makePayment(
                provider,
                reference,
                amount,
                code,
                purchaseRef,
                description)
        elif provider == 'orange_money_cm':
            return self.makePayment(
                provider,
                reference,
                amount,
                code,
                purchaseRef,
                description)
        elif provider == 'express_union_mobilemoney':
            return self.makePayment(
                provider,
                '237' + reference,
                amount,
                code,
                purchaseRef,
                description)
        elif provider == 'afrikpay':
            return self.makePayment(
                provider,
                '237' + reference,
                amount,
                code,
                purchaseRef,
                description)
        else:
            print('Invalid provider')

    def deposit(self):
        hash = hashlib.md5((str(self.store) + str(self.apiKey)).encode()).hexdigest()
        params = {
            'store': self.store,
            'hash': hash
        }
        response = requests.post(url = self.depositUrl, params = params)
        return response.json()

    def payout(
        self,
        provider,
        reference,
        amount,
        purchaseRef = '',
        description = ''):

        if provider == 'mtn_mobilemoney_cm':
            return self.makePayout(
                provider,
                reference,
                amount,
                purchaseRef,
                description)
        elif provider == 'orange_money_cm':
            return self.makePayout(
                provider,
                reference,
                amount,
                purchaseRef,
                description)
        elif provider == 'express_union_mobilemoney':
            return self.makePayout(
                provider,
                '237' + reference,
                amount,
                purchaseRef,
                description)
        elif provider == 'afrikpay':
            return self.makePayout(
                provider,
                '237' + reference,
                amount,
                purchaseRef,
                description)
        else:
            print('Invalid provider')

    def changeKey(self):
        hash = hashlib.md5((str(self.store) + str(self.apiKey)).encode()).hexdigest()
        params = {
            'store': self.store,
            'hash': hash
        }
        response = requests.post(url = self.changeKeyUrl, params = params)
        return response.json()

    def transactionStatus(
        self,
        purchaseRef):

        hash = hashlib.md5((str(purchaseRef) + str(self.apiKey)).encode()).hexdigest()
        params = {
            'purchaseref': purchaseRef,
            'store': self.store,
            'hash': hash
        }
        response = requests.post(url = self.transactionStatusUrl, params = params)
        return response.json()

    def makePayment(
        self,
        provider,
        reference,
        amount,
        code = '',
        purchaseRef = '',
        description = ''):

        hash = hashlib.md5((str(provider) + str(reference) + str(amount) + str(self.apiKey)).encode()).hexdigest()

        params = {
            'provider': provider,
            'reference': reference,
            'amount': amount,
            'description': description,
            'purchaseref': purchaseRef,
            'store': self.store,
            'hash': hash,
            'code': code,
            'notifurl': self.notifyUrl,
            'accepturl': self.acceptUrl,
            'cancelurl': self.cancelUrl,
            'declineurl': self.declineUrl
        }

        response = requests.post(url = self.collectUrl, params = params)
        return response.json()

    def makePayout(
        self,
        provider,
        reference,
        amount,
        purchaseRef = '',
        description = ''):

        hash = hashlib.md5((str(provider) + str(reference) + str(amount) + str(self.apiKey)).encode()).hexdigest()
        password = hashlib.md5((str(self.secretCode)).encode()).hexdigest()
        params = {
            'provider': provider,
            'reference': reference,
            'amount': amount,
            'description': description,
            'purchaseref': purchaseRef,
            'store': self.store,
            'hash': hash,
            'password': password
        }
        response = requests.post(url = self.payoutUrl, params = params)
        return response.json()

    def __repr__(self):
        return str(self.store + " - " + self.apiKey)

