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

def GetAsset(assetId):
    try:
        r = requests.get(BASEURL + '/asset/' + str(assetId),
                         auth=AUTH,
                         verify=False)
        return json.loads(r.text)

    except BaseException as Err:
        print("[GetAsset] Unhandled exception: " + str(Err))
        raise

def GetAssetQuote(assetId, startDate=None, endDate=None):
    par = {}
    if startDate is not None:
        par["start_date"] = startDate
    if endDate is not None:
        par["end_date"] = endDate

    try:
        r = requests.get(BASEURL + '/asset/{}/quote'.format(assetId),
                         auth=AUTH,
                         params=par,
                         verify=False)
        return json.loads(r.text)

    except BaseException as Err:
        print("[GetAssetQuote] Unhandled exception: " + str(Err))
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

def ComputeRatios(portfolioId, rats=[Ratios.SHARPE]):
    try:
        data = {"asset": portfolioId, "ratio": rats}
        jdata = json.dumps(data)
        r = requests.post(BASEURL + "/ratio/invoke",
                         data=jdata,
                         auth=AUTH,
                         verify=False)

        return json.loads(r.text)

    except BaseException as Err:
        print("[ComputeRatios] Unhandled exception: " + str(Err))
        raise
