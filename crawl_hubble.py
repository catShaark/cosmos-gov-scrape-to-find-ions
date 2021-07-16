
from urllib.request import urlopen


from bs4 import BeautifulSoup





# to get all validator from cosmoshub-4
# get mapping from valoper to acc addr
# get mapping from moniker to acc addr
url_hubble = "https://hubble.figment.io/cosmos/chains/cosmoshub-1/validators/"


def get_validator_valoper(hub_version,big_addr):

    document = urlopen(url_hubble.replace('1', str(hub_version)) + big_addr)
    html = document.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup.find("a", {'class': "validator-info__value technical"}).contents[0].strip()


