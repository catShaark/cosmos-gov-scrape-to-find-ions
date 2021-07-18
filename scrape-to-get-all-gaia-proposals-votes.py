import json
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

import requests


f = open("proposals_gaia.jsonl", 'w')


url_proposals = "https://api.cosmostation.io/v1/gov/proposals"
r_proposals = requests.get(url=url_proposals)
all_proposals = r_proposals.json()


last_proposal_id = max(all_proposals, key=lambda x: x["proposal_id"])["proposal_id"]



url_proposal_from_cosmostation = "https://api.cosmostation.io/v1/gov/proposal/votes/"
url_proposal_from_hubble = "https://hubble.figment.io/cosmos/chains/cosmoshub-version/governance/proposals/"

version_map = ['1']*6 + ['2']*14 + ['3']*18 + ['4']*1000

for id in range(1, last_proposal_id+1):
    r_proposal_id = requests.get(url=url_proposal_from_cosmostation + str(id))
    proposal_id = r_proposal_id.json()
    print(url_proposal_from_cosmostation + str(id))
    try :
        e = proposal_id["error_code"]
        print(e)

        continue
    except KeyError:
        pass
    if len(proposal_id["votes"]) != 0:
        proposal_id['id'] = id
        json.dump(proposal_id, f)
        f.write('\n')

    else:

        url = url_proposal_from_hubble.replace('version', version_map[id]) + str(id)
        try:
            document = urlopen(url)
        except:

            continue




        html = document.read()

        soup = BeautifulSoup(html, "html.parser")
        proposal_id = {}

        tally = {"yes_num": 0, "abstain_num": 0, "no_num": 0, "no_with_veto_num": 0}
        vote_options_and_amount = soup.findAll("div", {"class": re.compile(r"tally flex-column align-items-center*")})
        vote_options = ["yes_amount", "abstain_amount", "no_amount", "no_with_veto_amount"]

        for idd, vo in enumerate(vote_options_and_amount):
            tally[vote_options[idd]] = vo.find('span').contents[0]




        votes = soup.findAll("tr", {"data-vote-id": re.compile(r".*")})
        v_list = []
        for i in votes:

            vote = {}

            vote["voter"] = ""

            vote["moniker"] = ""

            vote["option"] = "VOTE_OPTION_" + i.find("td").contents[0].upper()
            if vote["option"] == "VOTE_OPTION_YES":
                tally["yes_num"] += 1
            elif vote["option"] == "VOTE_OPTION_ABSTAIN":
                tally["abstain_num"] += 1
            elif vote["option"] == "VOTE_OPTION_NO":
                tally["no_num"] += 1
            else :
                tally["no_with_veto_num"] += 1
            try:
                vote["voter"] = i.find('a').span.contents[0]
            except AttributeError:
                vote["moniker"] = i.find('a').contents[0].strip()

            vote["tx_hash"] = ""
            vote["time"] = ""
            v_list.append(vote)
        proposal_id["tally"] = tally
        proposal_id["votes"] = v_list
        proposal_id["id"] = id
        json.dump(proposal_id, f)
        f.write('\n')







