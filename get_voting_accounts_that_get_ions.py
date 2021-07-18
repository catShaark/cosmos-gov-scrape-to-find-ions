import re
from urllib.request import urlopen
from crawl_biggdiper import get_validator_acc
from crawl_hubble import get_validator_valoper
import requests
import json

from bs4 import BeautifulSoup

h = open("moniker_to_addr.json", 'r')
moniker_to_addr = json.load(h)

f1 = open("ions.json", "r")
l_ion_account_with_amount = json.load(f1)
l_ion_accounts = set(l_ion_account_with_amount.keys())


f2 = open("../votes.jsonl", "r")
json_list = list(f2)
l_gov_proposals = []
s_gov_account = set()
for json_str in json_list:
    result = json.loads(json_str)
    l_gov_proposals.append(result)

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
            s_gov_account.add(vote["voter"])


g = open("voting_accounts_that_get_ions2.json", "w")
json.dump(list(l_ion_accounts.intersection(s_gov_account)), g)

k = open("voting_accounts.json", "w")
json.dump(list(s_gov_account), k)
