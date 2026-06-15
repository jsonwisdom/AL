from typing import TypedDict, Literal

Status = Literal["TAINTED","DIVERGED","STALE","LOW_SAMPLE","NULL","BRONZE","SILVER","GOLD","PLATINUM"]

class Evidence(TypedDict):
    V:int; F:int; C:int; S_total:int; S_obs:int; W:int
    delta_t_days:float; age_days:float
    root_consistent:bool; fake_green_count:int

def result(status, score, sf, wf, conf):
    return {"status":status,"score_value":round(score,2),"surface_factor":round(sf,3),"witness_factor":round(wf,3),"confidence":round(conf,3)}

def arcade_status_engine(e: Evidence, min_sample_threshold:int=2, stale_threshold_days:float=1.0):
    if e["fake_green_count"] > 0:
        return result("TAINTED",0,0,0,0)

    T = e["V"] + e["F"] + e["C"]
    if T == 0:
        return result("NULL",0,0,0,0)

    sf = e["S_obs"] / e["S_total"] if e["S_total"] > 0 else 0
    wf = min(1, e["W"] / 5)
    score = 100 * (e["V"] / T) * sf * wf

    Cw = min(1, e["W"] / 10)
    Ct = min(1, e["delta_t_days"] / 30)
    Cd = 1 - (0.5 if e["C"] > 0 else 0)
    Cr = 1 if e["root_consistent"] else 0
    conf = Cw * Ct * Cd * Cr

    if e["C"] > 0 or not e["root_consistent"]:
        status = "DIVERGED"
    elif e["age_days"] > stale_threshold_days:
        status = "STALE"
    elif T < min_sample_threshold:
        status = "LOW_SAMPLE"
    elif score >= 90 and conf >= 0.8:
        status = "PLATINUM"
    elif score >= 80 and conf >= 0.7:
        status = "GOLD"
    elif score >= 60:
        status = "SILVER"
    elif score >= 30:
        status = "BRONZE"
    else:
        status = "NULL"

    return result(status,score,sf,wf,conf)
