import json
import numpy
import numpy as np

f = open("dict2.json", "r")
g = open("ions_account_that_participate_in_cosmos_gov_2.json", "r")
k = open("votes.jsonl", "r")
d = open("ions.json", "r")
q = open("accounts_that_voted_but_didn't_recivece_airdrop.txt", "r")
ll = open("delegator_of_sikka.json", "r")

accounts_that_voted_but = q.read().splitlines()
delegators_of_sikka = json.load(ll)["result"]
delegators_of_sikka = set(map(lambda x: x["delegator_address"], delegators_of_sikka))
ions_of = json.load(d)

accounts = {}

lis = json.load(g)
print(len(set(lis)))
for id, account in enumerate(lis):
    accounts[account] = {"ions": ions_of[account],
                         "num_of_votes": 0,
                         "num_of_votes_that_pass": 0,
                         "id": id,
                         "double_voting": 0,
                         "yes": 0,
                         "no": 0,
                         "abstain": 0,
                         "veto": 0
                         }


json_list = list(k)
proposals = []
for json_str in json_list:
    result = json.loads(json_str)
    proposals.append(result)

moniker_to_addr = json.load(f)

A = np.zeros((138, 37))

set_voting_accounts = set()

for proposal in proposals[:26]:
    id = proposal["id"]
    s = set()
    for vote in proposal['votes']:
        voter = vote['voter']
        if voter == "":
            voter = moniker_to_addr[vote["moniker"]]
        if accounts.get(voter) is not None:
        # accounts[voter][id] = [vote["option"]]
            accounts[voter]["num_of_votes"] += 1
            if voter not in s:
                s.add(voter)
            else:
                accounts[voter]["double_voting"] += 1

            if vote["option"] == "VOTE_OPTION_YES":
                accounts[voter]["yes"] += 1
                # if id not in [2, 4, 14, 26]:
                #     accounts[voter]["num_of_votes_that_pass"] += 1
            elif vote["option"] == "VOTE_OPTION_NO":
                accounts[voter]["no"] += 1
                # if id in [2, 4, 14, 26]:
                #     accounts[voter]["num_of_votes_that_pass"] += 1

            elif vote["option"] == "VOTE_OPTION_ABSTAIN":
                accounts[voter]["abstain"] += 1

            else :
                accounts[voter]["veto"] += 1
                # if id in [2, 4, 14, 26]:
                #     accounts[voter]["num_of_votes_that_pass"] += 1
        set_voting_accounts.add(voter)

num_of_outlier = 0

for acc in accounts:
    details = accounts[acc]
    if details["ions"] < details["num_of_votes"]:
        num_of_outlier += 1
        print('%s,%d,%d,%d,%d,%d,%d' %(acc, details["ions"], details["num_of_votes"], details["abstain"], details["no"], details["veto"], details["double_voting"]))
    # if details["double_voting"] != 0:
    #     print(',', details["double_voting"], end=" ")
    # if details["abstain"] != 0:
    #     print(',', details["abstain"], end=" ")
    # print()

# for acc in accounts:
#     details = accounts[acc]
#     if details["double_voting"] != 0:
#         print(acc, ',', details["double_voting"])

# print(num_of_outlier)
#
# min_i = 1
# min = 9999
# for i in range(20, 26):
#     num_of_outlier = 0
#     for vote in proposals[i]['votes']:
#         voter = vote['voter']
#         if voter == "":
#             voter = moniker_to_addr[vote["moniker"]]
#         if accounts.get(voter) is not None:
#             # accounts[voter][id] = [vote["option"]]
#
#             accounts[voter]["num_of_votes"] += 1
#     for acc in accounts:
#         details = accounts[acc]
#         print(details["ions"], ',', details["num_of_votes"])
#         if details["ions"] != details["num_of_votes"]:
#             num_of_outlier += 1
#     if num_of_outlier < min:
#         min = num_of_outlier
#         min_i = i
#
#     # print(details["ions"], ',', details["num_of_votes"], ',', details["num_of_votes_that_pass"], )
#
# print(min_i, min)
set_ions_acc = set(ions_of.keys())
print(len(set_ions_acc))
print(len(delegators_of_sikka))

accounts_not_staked_to_sikka_but_have_ions = set_ions_acc.difference(delegators_of_sikka)

print(len(set_ions_acc.difference(delegators_of_sikka)))
print(len(set_voting_accounts.difference(accounts_not_staked_to_sikka_but_have_ions)))
print(len(set_voting_accounts.intersection(delegators_of_sikka)))
# for i in accounts_not_staked_to_sikka_but_have_ions:
#     print(i)



print(len(accounts))





