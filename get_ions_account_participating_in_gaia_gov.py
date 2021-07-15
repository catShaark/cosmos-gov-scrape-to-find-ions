import re
from urllib.request import urlopen

import regex as regex
import requests
import json

from bs4 import BeautifulSoup
from regex import Regex

url_validators = "https://api.cosmostation.io/v1/staking/validators"
r_validators = requests.get(url=url_validators)
all_validators = r_validators.json()

moniker_to_addr = {}
valoper_to_addr = {}
for v in all_validators:
    moniker_to_addr[re.sub("[^0-9a-zA-Z]+", "", v['moniker'])] = v['account_address']
    valoper_to_addr[v['operator_address']] = v['account_address']



url_hubble = "https://hubble.figment.io/cosmos/chains/cosmoshub-"


for i in range(1, 4):
    document = urlopen(url_hubble + str(i))
    html = document.read()
    soup = BeautifulSoup(html, "html.parser")
    validators_valoper = soup.findAll("td", {'class': "d-none"})
    validators_moiker = soup.findAll("strong")
    for moniker, valoper in zip(validators_moiker, validators_valoper):
        try:
            valoper = re.search("cosmos[\S]*", str(valoper))[0]
            moniker = re.sub("[^0-9a-zA-Z]+", "", moniker.contents[0])
            print(valoper, moniker)
            moniker_to_addr[moniker] = valoper_to_addr[valoper]

        except:
            print(valoper, moniker, "fuck")
            pass
        if moniker == "Delega Networks♾ ":
            print(valoper)
            print(valoper_to_addr[valoper])


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
            if moniker_to_addr.get(re.sub("[^0-9a-zA-Z]+", "", vote["moniker"])) is None:
                s_gov_account.add(re.sub("[^0-9a-zA-Z]+", "", vote["moniker"]))
                print(vote["moniker"])
            else:
                s_gov_account.add(moniker_to_addr[re.sub("[^0-9a-zA-Z]+", "",vote["moniker"])])
        else :
            s_gov_account.add("voter")

h = open("dict.json", "w")
json.dump(moniker_to_addr, h)

g = open("ions_account_that_participate_in_cosmos_gov.json", "w")
json.dump(list(l_ion_accounts.intersection(s_gov_account)), g)
