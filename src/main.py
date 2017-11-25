import copy
import json
import random
import time

from dolphin import core as dc
from dolphin.utils import *

CURRENCY = {}
PRT_ID = 0
STARTTIME = 0

MAX_ITER = 10
NBR_PRT_POP = 300
PRT_SELECT = 30

def getDelta():
    return round(time.time() - STARTTIME, 2)

class Portfolio:
    def __init__(self, data, score=0):
        self.data = data
        self.score = score

def generateDefaultPortfolio():
    prt = {}
    prt["label"] = "PORTFOLIO_USER9"
    prt["currency"] = CURRENCY
    prt["type"] = "front"
    prt["values"] = { "2012-01-01": [] }
    classPrt = Portfolio(prt)
    return classPrt

def generateRandomPortfolio(assets):
    prt = generateDefaultPortfolio()
    ass = random.choices(assets, k=20)

    # minVal / (minVal + 19 * maxVal) >= 0.01, and
    # maxVal / (maxVal + minVal * 19) <= 0.1
    # so you end up with a broadest possible range
    # of about maxVal = 2 * minVal
    # The demonstration is left to the reviewer as an exercice :)
    minVal = 1.0
    maxVal = 2.0
    weights = [random.uniform(minVal, maxVal) for i in range(20)]
   
    sm = sum(weights)
    for i in range(20):
        weights[i] /= sm
        #print(weights)
    
    for assetIdx in range(len(ass)):
        dct = {
            "asset" : {
                "asset": asset_id(ass[assetIdx]),
                "quantity": weights[assetIdx]
            }
        }
        prt.data["values"]["2012-01-01"].append(dct)

    return prt

def getFirstPortfolioPopulation(assets):
    print("[{}]Getting first population...".format(getDelta()))
    global CURRENCY
    global PRT_ID

    for ass in assets:
        if asset_type(ass) == "PORTFOLIO":
            PRT_ID = asset_id(ass)
            CURRENCY = dc.getPortfolio(PRT_ID)["currency"]
            break
   
    prt_pop = []
    for i in range(NBR_PRT_POP):
        prt_pop.append(generateRandomPortfolio(assets))

    return prt_pop

def score(portfolio):
    worked = False
    #print(json.dumps(portfolio.data, indent=4))
    #print(json.dumps(ratios, indent=4))
    while not worked:
        try:
            dc.setPortfolio(PRT_ID, portfolio.data)
            ratios = dc.computeRatios([PRT_ID], rats=[dc.Ratios.SHARPE])
            nbrStr = ratios[PRT_ID]["{}".format(dc.Ratios.SHARPE)]["value"]
            worked = True
        except BaseException as Err:
            print(ratios)
            print("Retrying...")
            #raise
    result = float(nbrStr.replace(",", "."))
    portfolio.score = result
    return result
    #print(json.dumps(ratios, indent=4))


def select(portfolioPop):
    print("[{}]Selecting...".format(getDelta()))
    return sorted(portfolioPop, key=score, reverse=True)[:PRT_SELECT]

def mutate(portfolio):
    new_prt = copy.deepcopy(portfolio)
    assets = new_prt.data["values"]["2012-01-01"]
    keyFunct = lambda x: x["quantity"]
    sm = sum(asset["quantity"] for asset in assets)
    while True:
        for asset in new_prt.data["values"]["2012-01-01"]:
            asset["quantity"] *= random.uniform(0.95, 1.05)
        
        if max(assets, key=keyFunct) <= 0.1 * sm and \
            min(assets, key=keyFunct) >= 0.01 * sm:
            break

    return new_prt

def repopulate(prtPop, assets):
    print("[{}]Repopulating...".format(getDelta()))
    maxNonNew = 0.4 * NBR_PRT_POP
    ln = len(prtPop)
    for prt in prtPop:
        for i in range(PRT_SELECT, int(maxNonNew // ln)):
            prtPop.append(mutate(prt))

    diff = NBR_PRT_POP - len(prtPop)
    for i in range(diff):
        prtPop.append(generateRandomPortfolio(assets))

    return prtPop


def set_best(prtPop):
    print("Getting and setting the best portfolio...")
    bestPrt = max(prtPop, key=score)
    dc.setPortfolio(PRT_ID, bestPrt.data)
    with open("result.json", "w") as f:
        f.write(json.dumps(bestPrt.__dict__, indent=4))

if __name__ == "__main__":
    STARTTIME = time.time()
    print("[{}]Setting server info...".format(getDelta()))
    dc.setServerInfo("https://dolphin.jump-technology.com:3389/api/v1",
                     ("epita_user_9", "dolphin16116"))
    
    print("[{}]Getting assets...".format(getDelta()))
    assets = dc.getAllAssets()

    prtPop = getFirstPortfolioPopulation(assets)
    for i in range(MAX_ITER):
        print("[{}]Iter : {}/{}".format(getDelta(), i+1, MAX_ITER))
        prtPop = select(prtPop)
        with open("tmp_result_{}".format(i), "w") as tmpf:
            print("[{}]Saving...".format(getDelta()))
            for prt in prtPop:
                tmpf.write(json.dumps(prt.__dict__, indent=4))
        repopulate(prtPop, assets)
    
    set_best(prtPop)
