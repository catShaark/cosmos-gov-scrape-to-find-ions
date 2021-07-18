import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from crawl_hubble import get_validator_valoper
from crawl_biggdiper import get_validator_acc
import requests
import json

# to get all validator from cosmoshub-4
# get mapping from valoper to acc addr
# get mapping from moniker to acc addr
url_validators = "https://api.cosmostation.io/v1/staking/validators"
r_validators = requests.get(url=url_validators)
all_validators = r_validators.json()

moniker_to_addr = {}
valoper_to_addr = {}
for v in all_validators:
    moniker_to_addr[v['moniker'].strip()] = v['account_address']
    valoper_to_addr[v['operator_address']] = v['account_address']


url_hubble = "https://hubble.figment.io/cosmos/chains/cosmoshub-"


for i in range(1, 4):
    document = urlopen(url_hubble + str(i))
    html = document.read()
    soup = BeautifulSoup(html, "html.parser")
    validators = soup.findAll("tr")[1:]
    for validator in validators:
        valoper = validator.find("td", {'class': "d-none"})
        moniker = validator.find("strong")
        if moniker is None:
            big_addr = validator.find("span", {'class': 'technical'}).contents[0]
            temp = get_validator_valoper(i, big_addr)
            moniker_to_addr[big_addr[:13] + '...'] = temp
            print(1, big_addr, temp)

        else:
            try:
                moniker = moniker.contents[0].strip()
                valoper = re.search("cosmos[\S]*", str(valoper))[0]
                print(2, valoper, moniker)
                moniker_to_addr[moniker] = valoper_to_addr[valoper]
            except:
                try:
                    moniker_to_addr[moniker] = get_validator_acc(hub_version=i, valoper=valoper)
                    print(4, valoper, moniker)
                except:
                    print(5, valoper, moniker)
                    pass


h = open("moniker_to_addr.json", "w")
json.dump(moniker_to_addr, h)





