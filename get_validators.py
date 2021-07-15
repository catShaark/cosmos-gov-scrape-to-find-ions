import re
import time
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from selenium import webdriver

import requests
import json

url_validators = "https://api.cosmostation.io/v1/staking/validators"
r_validators = requests.get(url=url_validators)
all_validators = r_validators.json()

moniker_to_addr = {}
valoper_to_addr = {}
for v in all_validators:
    moniker_to_addr[v['moniker']] = v['account_address']
    valoper_to_addr[v['operator_address']] = v['account_address']

url_hubble = "https://hubble.figment.io/cosmos/chains/cosmoshub-"


moniker_to_acc_addr = {}
url_cosmostation = "https://api.cosmostation.io/v1/staking/validator/"

for i in range(1, 4):


    document = urlopen(url_hubble + str(i))
    html = document.read()

    # this renders the JS code and stores all
    # of the information in static HTML code.

    # Now, we could simply apply bs4 to html variable
    soup = BeautifulSoup(html, "html.parser")
    validators_valoper = soup.findAll("td", {'class': "d-none"})
    validators_moiker = soup.findAll("strong")
    for moniker, valoper in zip(validators_moiker,validators_valoper):
        try:
            valoper = re.search("cosmos[\S]*", str(valoper))[0]
            moniker = moniker.contents[0]
            moniker_to_addr[moniker] = valoper_to_addr[valoper]
        except:
            pass








