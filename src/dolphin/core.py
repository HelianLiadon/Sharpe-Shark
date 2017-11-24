import requests
import json

AUTH = ()
BASEURL = ""

class Ratios:
    BETA = 15
    PEARSON = 19
    RENDEMENT = 21
    RENDEMENT_ANN = 17
    SHARPE = 20
    VAR = 22
    VOLATILITE = 18
    EXPOSITION = 29


def SetServerInfo(url, creds):
    global AUTH
    global BASEURL
    AUTH = creds
    BASEURL = url

def GetServerInfo():
    return (BASEURL, AUTH)

def GetAllAssets():
    try:
        r = requests.get(BASEURL + '/asset', auth=AUTH, verify=False)
        return json.loads(r.text)

    except BaseException as Err:
        print("[GetAllAssets] Unhandled exception: " + str(Err))
        raise

def GetAsset(AssetId):
    try:
        r = requests.get(BASEURL + '/asset/' + str(AssetId),
                         auth=AUTH,
                         verify=False)
        return json.loads(r.text)

    except BaseException as Err:
        print("[GetAsset] Unhandled exception: " + str(Err))
        raise

def GetRatios():
    try:
        r = requests.get(BASEURL + '/ratio',
                         auth=AUTH,
                         verify=False)
        return json.loads(r.text)

    except BaseException as Err:
        print("[GetRatios] Unhandled exception: " + str(Err))
        raise

def ComputeRatios(PortfolioId, Rats=[Ratios.SHARPE]):
    try:
        data = {"asset": PortfolioId, "ratio": Rats}
        jdata = json.dumps(data)
        r = requests.post(BASEURL + "/ratio/invoke",
                         data=jdata,
                         auth=AUTH,
                         verify=False)

        return json.loads(r.text)

    except BaseException as Err:
        print("[ComputeRatios] Unhandled exception: " + str(Err))
        raise
