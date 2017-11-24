import requests
import json

AUTH = ()
BASEURL = ""

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
