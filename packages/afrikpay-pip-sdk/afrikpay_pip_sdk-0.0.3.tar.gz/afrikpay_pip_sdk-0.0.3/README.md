<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Simple python package</h3>
  <p align="center">
    <a href="https://github.com/Georges-Ngandeu/SimplePythonPackage"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/Georges-Ngandeu/SimplePythonPackage">View Demo</a>
    ·
    <a href="https://github.com/Georges-Ngandeu/SimplePythonPackage">Report Bug</a>
    ·
    <a href="https://github.com/Georges-Ngandeu/SimplePythonPackage">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li><a href="#getting">Getting started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">Ecommerce Integration</a></li>
    <li><a href="#license">Bill Integration</a></li>
    <li><a href="#license">Airtime Integration</a></li>
    <li><a href="#license">Account Integration</a></li>
    <li><a href="#contact">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>


<!-- GETTING STARTED -->
## Getting Started
This python library was created with the purpose of facilitating the integration of our payment api to our partners. It is an ongoing work. Suggestions to ameliorate the api are welcome. 
<!-- USAGE EXAMPLES -->
## Ecommerce integration
Let's suppose you want to integrate ecommerce payments on you system. Here are the two main steps to get the job done in the development environment.
You an uncomment the code to test the others apis. 
```
from afrikpay_pip_sdk import Ecommerce

#testing some ecommerce api

ecommerce = Ecommerce(
  'AFC6617',
  '661671d0bd7bef499e7d80879c27d95e',
  '7777',
  'http://34.86.5.170:8086/api/ecommerce/collect/',
  'http://34.86.5.170:8086/api/ecommerce/payout/',
  'http://34.86.5.170:8086/api/ecommerce/deposit/',
  'http://34.86.5.170:8086/api/ecommerce/changekey/',
  'http://34.86.5.170:8086/api/ecommerce/transaction/status/')

#ecommerce payment with mtn
response = ecommerce.collect(
  'mtn_mobilemoney_cm',
  '677777777',
  4000,
  '123456'
)
print(response)

# ecommerce payment with orange
# response = ecommerce.collect(
#     'orange_money_cm',
#     '699999999',
#     400,
#     0000
# )
#print(response)

#response = ecommerce.deposit()
#print(response)

# change ecommerce apikey
#response = ecommerce.changeKey()
#print(response)

# get ecommerce transaction status
#response = ecommerce.transactionStatus('128_1622044090')
#print(response)

```
## Bill integration
If you want to integrate bill payments apis on you system, here are the two main steps to get the job done in the development environment. You an uncomment the code to test the others apis.
```
from afrikpay_pip_sdk import Bill

#testing bill api
bill = Bill(
  '3620724907638658',
  '3620724907638658',
  'e825e83873eafffff315fc3f22db2d59',
  'afrikpay',
  'http://34.86.5.170:8086/api/bill/v2/',
  'http://34.86.5.170:8086/api/bill/getamount/',
  'http://34.86.5.170:8086/api/bill/status/v2/')

#camwater
response = bill.payBill(
  'camwater',
  '111111111111111',
  1000,
  'cash',
  '96543'
)
print(response)

# response = bill.getBillAmount(
#     'camwater',
#     '111111111111111',
# )
#print(response)

# response = bill.getBillStatus(
#     '96543',
# )
# print(response)

#eneoprepay
# response = bill.payBill(
#     'eneoprepay',
#     '014111111111',
#     1000,
#     'cash',
#     'qsde14'
# )
# print(response)

# response = bill.getBillAmount(
#     'eneoprepay',
#     '014111111111',
# )
# print(response)

# response = bill.getBillStatus(
#     'qsde14',
# )
# print(response)
```
## Airtime integration
If you want to integrate airtime apis on you system, here are the two main steps to get the job done in the development environment. You an uncomment the code to test the others apis.
```
from afrikpay_pip_sdk import Airtime

#testing airtime apis
airtime = Airtime(
  '3620724907638658',
  '3620724907638658',
  'e825e83873eafffff315fc3f22db2d59',
  'afrikpay',
  'http://34.86.5.170:8086/api/airtime/v2/',
  'http://34.86.5.170:8086/api/airtime/status/v2/')

response = airtime.makeAirtime(
  'mtn',
  '677777777',
  1000,
  'cash',
  '123456789'
)
print(response)

# response = airtime.airtimeStatus(
#     '123456789'
# )
# print(response)
```
## Account integration
If you want to integrate account apis on you system, here are the two main steps to get the job done in the development environment. You an uncomment the code to test the others apis.
```
from afrikpay_pip_sdk import Account

#testing account apis
account = Account(
  '3620724907638658',
  '3620724907638658',
  'e825e83873eafffff315fc3f22db2d59',
  'http://34.86.5.170:8086/api/account/transaction/status/',
  'http://34.86.5.170:8086/api/account/agent/balance/v2/',
  'http://34.86.5.170:8086/api/account/developer/changekey/')

response = account.balance()
print(response)
```
## How to switch to production ?
You can explore the src folder to see the default production setup. Just use the appropriate apikey, store code, agentid for production. If you have any problem using the library please contact us, we will be happy to help you. 
<!-- LICENSE -->
## License

<!-- CONTACT -->
## Contact

Project Link: [https://github.com/Georges-Ngandeu/SimplePythonPackage](https://github.com/Georges-Ngandeu/SimplePythonPackage)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* []()
* []()
* []()

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/github_username