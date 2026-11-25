import json, math
C=json.load(open("/home/claude/skm/work/counter108v2.json"))["count_times_sec"]
END=round(C[36]+1.6,3)
OM=[None,3.3]+[C[n-1]+2.0 for n in range(2,109)]
S=[None]+[C[n]+1.3 for n in range(1,108)]
IM={ # clean-image fractions: face, mala
 "s02":{"src":"assets/img/sks108-b1-s02-dawn-dhyan-2x.jpg","face":(0.50,0.27),"mala":(0.37,0.475),"det":[(0.12,0.20),(0.85,0.30)]},
 "s03":{"src":"assets/img/sks108-b1-s03-tapasvi-mukh-2x.jpg","face":(0.52,0.33),"mala":(0.34,0.55),"det":[(0.18,0.20),(0.88,0.25)]},
 "s04":{"src":"assets/img/sks108-b1-s04-kamal-sarovar-2x.jpg","face":(0.50,0.30),"mala":(0.37,0.50),"det":[(0.15,0.15),(0.88,0.70)]},
 "s05":{"src":"assets/img/sks108-b1-s05-gufa-dhyan-2x.jpg","face":(0.53,0.30),"mala":(0.38,0.48),"det":[(0.10,0.55),(0.90,0.60)]},
 "s06":{"src":"assets/img/sks108-b2-s06-mala-sparsh-2x.jpg","face":(0.58,0.24),"mala":(0.33,0.47),"det":[(0.20,0.12),(0.82,0.35)]},
 "s07":{"src":"assets/img/sks108-b2-s07-havan-se-darshan-2x.jpg","face":(0.68,0.25),"mala":(0.58,0.43),"det":[(0.30,0.35),(0.57,0.82)]},
}
def pool(t,kind):
    if t<125: P={"M":["s02","s04","s03","s02"],"A":["s03","s02","s04"],"B":["s02","s04","s03"]}
    elif t<245: P={"M":["s04","s05","s06","s03"],"A":["s05","s04","s06","s03"],"B":["s04","s05","s07"]}
    else: P={"M":["s05","s06","s04","s02"],"A":["s06","s05","s07","s03"],"B":["s07","s05","s06"]}
    return P[kind]
shots=[]
shots.append(dict(img="s03",clip="hook_s03",t0=0.0,t1=6.4,focus="face",z0=1.0,z1=1.14,anchor=(0.5,0.42)))
shots.append(dict(img="s02",clip="hook_s02",t0=6.4,t1=9.8,focus="face",z0=1.25,z1=1.4,anchor=(0.5,0.42)))
shots.append(dict(img="s04",t0=9.8,t1=round(S[1]+2.3,3),focus="mala",z0=1.15,z1=1.3,anchor=(0.40,0.46)))
cnt={"M":0,"A":0,"B":0}; last="s04"
n=1
while True:
    b1=S[n]+2.3; b2=S[n]+5.5; b3=S[n]+7.9
    nxt = S[n+1]+2.3 if n+1<=107 else None
    seg=[("A",b1,b2),("B",b2,b3),("M",b3,nxt)]
    for kind,a,b in seg:
        if a>=END: break
        b=min(b,END) if b else END
        pl=[p for p in pool(a,kind) if p!=last] ; img=pl[cnt[kind]%len(pl)]; cnt[kind]+=1
        if kind=="M" and img=="s07": img="s05"
        if kind=="A": sh=dict(focus="face",z0=1.55,z1=1.75,anchor=(0.5,0.40))
        elif kind=="B":
            d=IM[img]["det"][cnt["B"]%2]; sh=dict(focus="det",det=d,z0=1.0,z1=1.12,anchor=(0.5,0.45),pan=(-60 if cnt["B"]%2 else 60))
            if img=="s07": sh=dict(focus="face",z0=1.0,z1=1.1,anchor=(0.6,0.35))
        else: sh=dict(focus="mala",z0=1.18,z1=1.32,anchor=(0.40,0.46))
        sh.update(img=img,t0=round(a,3),t1=round(b,3)); shots.append(sh); last=img
    if nxt is None or nxt>=END: break
    n+=1
# fix: first generated shot must start where hook ends
shots[3]["t0"]=shots[2]["t1"]
data=dict(END=END,OM=OM[1:37+1],S=[s for s in S[1:38]],C=C[:38],IM={k:{"src":v["src"],"face":v["face"],"mala":v["mala"]} for k,v in IM.items()},
 shots=shots, milestones=[{"n":11,"t":round(S[11]+1.3,3)},{"n":21,"t":round(S[21]+1.3,3)}],
 cta=[{"t":62.0,"kind":"like"},{"t":272.0,"kind":"sub"}])
open("data.js","w").write("window.DATA="+json.dumps(data)+";")
print([ (round(x["t1"]-x["t0"],2),x["t0"]) for x in shots if x["t1"]-x["t0"]>5]); print("END",END,"shots",len(shots)); print([ (s['img'],s['t0'],s['t1']) for s in shots[:8]])
L=[s['t1']-s['t0'] for s in shots]; print("shot len min %.2f max %.2f"%(min(L),max(L)))
