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
