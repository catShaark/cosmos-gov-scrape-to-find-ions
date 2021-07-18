import requests



url_proposals = "https://api.cosmostation.io/v1/gov/proposals"
r_proposals = requests.get(url=url_proposals)
all_proposals = r_proposals.json()


last_proposal_id = max(all_proposals, key=lambda x: x["proposal_id"])["proposal_id"]

