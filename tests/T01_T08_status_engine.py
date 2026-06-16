from arcade_status_engine import arcade_status_engine

tests = [
("T01",dict(V=50,F=0,C=0,S_total=5,S_obs=5,W=10,delta_t_days=30,age_days=0,root_consistent=True,fake_green_count=1),"TAINTED"),
("T02",dict(V=50,F=0,C=0,S_total=5,S_obs=5,W=10,delta_t_days=30,age_days=0,root_consistent=False,fake_green_count=0),"DIVERGED"),
("T03",dict(V=1,F=0,C=0,S_total=5,S_obs=5,W=1,delta_t_days=1,age_days=0,root_consistent=True,fake_green_count=0),"LOW_SAMPLE"),
("T04",dict(V=0,F=0,C=0,S_total=5,S_obs=0,W=0,delta_t_days=0,age_days=0,root_consistent=True,fake_green_count=0),"NULL"),
("T05",dict(V=50,F=0,C=0,S_total=5,S_obs=5,W=10,delta_t_days=30,age_days=2,root_consistent=True,fake_green_count=0),"STALE"),
("T06",dict(V=1,F=4,C=0,S_total=5,S_obs=1,W=1,delta_t_days=.5,age_days=0,root_consistent=True,fake_green_count=0),"NULL"),
("T07",dict(V=50,F=0,C=0,S_total=5,S_obs=5,W=10,delta_t_days=30,age_days=0,root_consistent=True,fake_green_count=0),"PLATINUM"),
("T08",dict(V=49,F=0,C=1,S_total=5,S_obs=5,W=10,delta_t_days=30,age_days=0,root_consistent=True,fake_green_count=0),"DIVERGED"),
]

passed=0
for name,e,want in tests:
    got=arcade_status_engine(e)
    ok=got["status"]==want
    passed+=ok
    print(("✅" if ok else "❌"), name, "Expected:", want, "Got:", got["status"], got)

print(f"Passed: {passed}/{len(tests)}")
if passed != len(tests):
    raise SystemExit(1)
