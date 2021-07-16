import re
from urllib.request import urlopen
from crawl_biggdiper import get_validator_acc
from crawl_hubble import get_validator_valoper
import regex as regex
import requests
import json

from bs4 import BeautifulSoup
from regex import Regex




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


k = open("list_of_special_addr.txt", "r+")

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






f1 = open("ions.json", "r")
l_ion_account_with_amount = json.load(f1)
l_ion_accounts = set(l_ion_account_with_amount.keys())


f2 = open("votes.jsonl", "r")
json_list = list(f2)
l_gov_proposals = []
s_gov_account = set()
for json_str in json_list:
    result = json.loads(json_str)
    l_gov_proposals.append(result)
print('-----------------')
for proposal in l_gov_proposals:
    votes = proposal['votes']
    for vote in votes:

        if vote["voter"] == "":
            moniker = vote["moniker"].strip()
            if moniker_to_addr.get(moniker) is None:
                print(moniker)
            else:
                s_gov_account.add(moniker_to_addr[moniker])
        else:
            s_gov_account.add("voter")

h = open("dict2.json", "w")
json.dump(moniker_to_addr, h)

g = open("ions_account_that_participate_in_cosmos_gov.json", "w")
json.dump(list(l_ion_accounts.intersection(s_gov_account)), g)
