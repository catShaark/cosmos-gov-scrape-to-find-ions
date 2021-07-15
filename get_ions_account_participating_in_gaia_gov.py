import requests
import json

url_validators = "https://api.cosmostation.io/v1/staking/validators"
r_validators = requests.get(url=url_validators)
all_validators = r_validators.json()

moniker_to_addr = {}
for v in all_validators:
    moniker_to_addr[v['moniker']] = v['account_address']

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

for proposal in l_gov_proposals:
    votes = proposal['votes']
    for vote in votes:
        if vote["voter"] == "":
            if moniker_to_addr.get(vote["moniker"]) is None:
                s_gov_account.add(vote["moniker"])
            else:
                s_gov_account.add(moniker_to_addr[vote["moniker"]])
        else :
            s_gov_account.add("voter")

g = open("ions_account_that_participate_in_cosmos_gov.json", "w")
json.dump(list(l_ion_accounts.intersection(s_gov_account)), g)
