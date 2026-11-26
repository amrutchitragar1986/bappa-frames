import json, math
C=json.load(open("/home/claude/skm/work/counter108v2.json"))["count_times_sec"]
P1END=round(C[36]+1.6,3)
P2END=round(C[72]+1.6,3)
C=C+[1086.42]   # kuru kuru of mantra 108 (matched in the audio)
PA0=round(C[105]+1.3+2.6,3)
END=1104.6
CHANT_END=1092.7
OM=[None,3.3]+[C[n-1]+2.0 for n in range(2,109)]
S=[None]+[C[n]+1.3 for n in range(1,109)]
IM={ # clean-image fractions: face, mala
 "s02":{"src":"assets/img/sks108-b1-s02-dawn-dhyan-2x.jpg","face":(0.50,0.27),"mala":(0.37,0.475),"det":[(0.12,0.20),(0.85,0.30)]},
 "s03":{"src":"assets/img/sks108-b1-s03-tapasvi-mukh-2x.jpg","face":(0.52,0.33),"mala":(0.34,0.55),"det":[(0.18,0.20),(0.88,0.25)]},
 "s04":{"src":"assets/img/sks108-b1-s04-kamal-sarovar-2x.jpg","face":(0.50,0.30),"mala":(0.37,0.50),"det":[(0.15,0.15),(0.88,0.70)]},
 "s05":{"src":"assets/img/sks108-b1-s05-gufa-dhyan-2x.jpg","face":(0.53,0.30),"mala":(0.38,0.48),"det":[(0.10,0.55),(0.90,0.60)]},
 "s06":{"src":"assets/img/sks108-b2-s06-mala-sparsh-2x.jpg","face":(0.58,0.24),"mala":(0.33,0.47),"det":[(0.20,0.12),(0.82,0.35)]},
 "s07":{"src":"assets/img/sks108-b2-s07-havan-se-darshan-2x.jpg","face":(0.68,0.25),"mala":(0.58,0.43),"det":[(0.30,0.35),(0.57,0.82)]},
 "s08":{"src":"assets/img/sks108-b2-s08-himalaya-shikhar-2x.jpg","face":(0.50,0.25),"mala":(0.37,0.45),"det":[(0.15,0.25),(0.85,0.30)]},
 "s09":{"src":"assets/img/sks108-b2-s09-ganga-tat-2x.jpg","face":(0.45,0.25),"mala":(0.33,0.48),"det":[(0.85,0.25),(0.80,0.62)]},
 "s10":{"src":"assets/img/sks108-b2-s10-van-ashram-2x.jpg","face":(0.48,0.27),"mala":(0.36,0.45),"det":[(0.12,0.40),(0.85,0.50)]},
 "s11":{"src":"assets/img/sks108-b2-s11-sandhya-ghat-2x.jpg","face":(0.55,0.25),"mala":(0.43,0.45),"det":[(0.20,0.30),(0.88,0.35)]},
 "s12":{"src":"assets/img/sks108-b3-s12-godhuli-2x.jpg","face":(0.50,0.25),"mala":(0.36,0.46),"det":[(0.15,0.60),(0.80,0.33)]},
 "s14":{"src":"assets/img/sks108-b4-s14-deep-mala-ratri-2x.jpg","face":(0.50,0.22),"mala":(0.40,0.42),"det":[(0.20,0.30),(0.82,0.30)]},
 "s15":{"src":"assets/img/sks108-b3-s15-chandra-dhyan-2x.jpg","face":(0.52,0.22),"mala":(0.40,0.44),"det":[(0.55,0.08),(0.12,0.75)]},
 "s16":{"src":"assets/img/sks108-b3-s16-brahmand-2x.jpg","face":(0.50,0.24),"mala":(0.40,0.45),"det":[(0.15,0.12),(0.88,0.12)]},
 "s17":{"src":"assets/img/sks108-b3-s17-swarna-kamal-2x.jpg","face":(0.50,0.26),"mala":(0.41,0.46),"det":[(0.10,0.30),(0.90,0.30)]},
 "pa1":{"src":"assets/img/sks108-b4-pa1-poorna-ahuti-2x.jpg","face":(0.50,0.14),"mala":(0.42,0.36),"det":[(0.50,0.62),(0.62,0.60)]},
 "pa2":{"src":"assets/img/sks108-b4-pa2-ahuti-close-2x.jpg","face":(0.50,0.20),"mala":(0.48,0.35),"det":[(0.40,0.58),(0.62,0.55)]},
 "pa3":{"src":"assets/img/sks108-b4-pa3-agni-se-mala-2x.jpg","face":(0.50,0.17),"mala":(0.41,0.44),"det":[(0.45,0.60),(0.45,0.50)]},
 "s18":{"src":"assets/img/sks108-b4-s18-maha-aarti-2x.jpg","face":(0.50,0.17),"mala":(0.39,0.32),"det":[(0.50,0.80),(0.13,0.12)]},
 "s19":{"src":"assets/img/sks108-b4-s19-108-ashirwad-2x.jpg","face":(0.50,0.24),"mala":(0.37,0.41),"det":[(0.37,0.41),(0.50,0.24)]},
 "s13":{"src":"assets/img/sks108-b3-s13-sandhya-aarti-2x.jpg","face":(0.52,0.25),"mala":(0.43,0.42),"det":[(0.85,0.25),(0.15,0.55)]},
}
def pool(t,kind):
    kind='A' if kind=='A' else 'M'
    if t<125: P={"M":["s02","s04","s03","s02"],"A":["s03","s02","s04"],"B":["s02","s04","s03"]}
    elif t<245: P={"M":["s04","s05","s06","s03"],"A":["s05","s04","s06","s03"],"B":["s04","s05","s07"]}
    elif t<363.39: P={"M":["s05","s06","s04","s02"],"A":["s06","s05","s07","s03"],"B":["s07","s05","s06"]}
    elif t<485: P={"M":["s08","s09","s08","s06"],"A":["s08","s09","s10"],"B":["s09"]}
    elif t<605: P={"M":["s10","s11","s09"],"A":["s11","s10","s12","s09"],"B":["s10"]}
    elif t<725.8: P={"M":["s12","s11","s10"],"A":["s13","s12","s11"],"B":["s12"]}
    elif t<850: P={"M":["s14","s15","s14"],"A":["s15","s14","s16"],"B":["s14"]}
    elif t<970: P={"M":["s16","s15","s17"],"A":["s16","s17","s15","s14"],"B":["s16"]}
    else: P={"M":["s17","s16","s14"],"A":["s17","s16","s15"],"B":["s17"]}
    return P[kind]
shots=[]
shots.append(dict(img="s03",clip="hook_s03",t0=0.0,t1=6.4,focus="face",z0=1.0,z1=1.22,anchor=(0.5,0.42)))
shots.append(dict(img="s02",clip="hook_s02",t0=6.4,t1=10.2,focus="face",z0=1.45,z1=1.2,anchor=(0.5,0.42)))
shots.append(dict(img="s04",t0=10.2,t1=round(S[1]+2.6,3),focus="mala",z0=1.05,z1=1.3,anchor=(0.40,0.46)))
cnt={"M":0,"A":0}; last="s04"
n=1
while True:
    b1=S[n]+2.6; b2=S[n]+7.4
    nxt = S[n+1]+2.6 if n+1<=107 else None
    for kind,a,b in [("A",b1,b2),("M",b2,nxt)]:
        if a>=PA0: break
        b=min(b,PA0) if b else PA0
        pk="A" if kind=="A" else "M"
        pl=[p for p in pool(a,"A" if kind=="A" else "M") if p!=last]; img=pl[cnt[kind]%len(pl)]; k=cnt[kind]; cnt[kind]+=1
        if kind=="M" and img in ("s07","s13"): img="s12" if a>600 else "s05"
        if kind=="A":
            v=k%3
            if img in ("s07","s13"): sh=dict(focus="face",z0=1.0,z1=1.25,anchor=((0.6 if img=="s07" else 0.55),0.35))
            elif v==0: sh=dict(focus="face",z0=1.3,z1=1.7,anchor=(0.5,0.40))            # slow push in to the face
            elif v==1: sh=dict(focus="face",z0=1.45,z1=1.05,anchor=(0.5,0.40))          # slow pull out to the full darshan
            else:
                d=IM[img]["det"][k%2]; sh=dict(focus="det",det=d,z0=1.15,z1=1.45,anchor=(0.5,0.45),pan=(-80 if k%2 else 80))
        else:
            sh=dict(focus="mala",z0=(1.05 if k%2 else 1.35),z1=(1.35 if k%2 else 1.08),anchor=(0.40,0.46))
        sh.update(img=img,t0=round(a,3),t1=round(b,3)); shots.append(sh); last=img
    if nxt is None or nxt>=PA0: break
    n+=1
shots[3]["t0"]=shots[2]["t1"]
# keep Part 1's last shot exactly as rendered, then continue the same picture without a dissolve
for i,sh in enumerate(shots):
    if sh["t0"]<P1END<sh["t1"]:
        cont=dict(sh); cont.update(t0=P1END,z0=sh["z1"],z1=round(sh["z1"]-0.04,3),cont=True); sh["t1"]=P1END; shots.insert(i+1,cont); break
for i,sh in enumerate(shots):
    if sh["t0"]<P2END<sh["t1"]:
        cont=dict(sh); cont.update(t0=P2END,z0=sh["z1"],z1=round(sh["z1"]-0.04,3),cont=True); sh["t1"]=P2END; shots.insert(i+1,cont); break
# ending: poorna ahuti -> eyes open -> aarti
E=[dict(img="pa1",clip="pa1",rate=0.9,t0=PA0,t1=1067.0,focus="face",z0=1.0,z1=1.08,anchor=(0.5,0.30)),
   dict(img="pa2",t0=1067.0,t1=1071.6,focus="det",det=(0.40,0.58),z0=1.1,z1=1.35,anchor=(0.45,0.55),pan=60),
   dict(img="pa1",t0=1071.6,t1=1076.3,focus="mala",z0=1.35,z1=1.1,anchor=(0.42,0.40)),
   dict(img="pa2",t0=1076.3,t1=1080.6,focus="face",z0=1.0,z1=1.2,anchor=(0.5,0.30)),
   dict(img="pa3",t0=1080.6,t1=1089.3,focus="mala",z0=1.0,z1=1.3,anchor=(0.42,0.46)),
   dict(img="s19",clip="eyes",rate=1.0,t0=1089.3,t1=1095.3,focus="face",z0=1.0,z1=1.1,anchor=(0.5,0.30)),
   dict(img="s19",t0=1095.3,t1=1099.2,focus="face",z0=1.1,z1=1.3,anchor=(0.5,0.34)),
   dict(img="s18",clip="aarti",rate=1.0,t0=1099.2,t1=END,focus="face",z0=1.0,z1=1.06,anchor=(0.5,0.30))]
shots=[x for x in shots if x["t0"]<PA0]; shots[-1]["t1"]=PA0; shots+=E
for sh in shots:
    if abs(sh["t0"]-(S[51]+2.6))<0.01: sh.update(img="s11",clip="ms51",focus="face",z0=1.0,z1=1.2,anchor=(0.5,0.40)); sh.pop("det",None); sh.pop("pan",None)
data=dict(P1END=P1END,P2END=P2END,END=END,CHANT_END=CHANT_END,OM=OM[1:109],S=[s for s in S[1:109]],C=C[:109],
 IM={k:{"src":v["src"],"face":v["face"],"mala":v["mala"]} for k,v in IM.items()},
 noHavan=["s07","s13","pa1","pa2","pa3","s18","s19"],
 shots=shots, milestones=[{"n":11,"t":round(S[11]+1.3,3),"m2":"अगला पड़ाव: २१ · बाप्पा के साथ बने रहिए"},{"n":21,"t":round(S[21]+1.3,3),"m2":"अगला पड़ाव: ५१ · मन ही मन साथ जपिए"},
   {"n":51,"t":round(S[51]+1.3,3),"m2":"आधी माला बस ३ जाप दूर 🙏"},{"n":54,"t":round(S[54]+1.3,3),"m1":"आधी माला पूर्ण 🙏","m2":"५४ जाप · १०८ पर बाप्पा आशीर्वाद देंगे ✨"},
   {"n":81,"t":round(S[81]+1.3,3),"m2":"अगला पड़ाव: १०० · पूर्णाहुति निकट 🔥"},{"n":100,"t":round(S[100]+1.3,3),"m2":"बस ८ जाप और · पूर्णाहुति आ रही है 🔥"},
   {"n":108,"t":round(S[108]+1.3,3),"cardT":1095.6,"top":690,"m1":"१०८ जाप पूर्ण 🙏","m2":"बाप्पा आपके सब कार्य सिद्ध करें ✨"},
   {"n":0,"t":1100.4,"cardT":1100.4,"dur":4.2,"top":690,"quiet":True,"m1":"गणपति बाप्पा मोरया 🙏","m2":"🔔 Subscribe करें · All about बाप्पा"}],
 teasers=[{"t":478.0,"txt":"१०८ पर बाप्पा आँखें खोलेंगे 🙏"},{"t":598.0,"txt":"अंत तक जपिए · १०८ पर विशेष दर्शन ✨"},
   {"t":842.0,"txt":"अंत में पूर्णाहुति 🔥 और बाप्पा के दर्शन"},{"t":962.0,"txt":"बस कुछ जाप और · बाप्पा आँखें खोलेंगे 🙏"}],
 sweeps=[{"t0":440.0},{"t0":478.4},{"t0":598.4},{"t0":668.0},{"t0":800.0},{"t0":842.4},{"t0":962.4},{"t0":1040.0}],
 cta=[{"t":62.0,"kind":"like"},{"t":272.0,"kind":"sub"},{"t":398.0,"kind":"like"},{"t":640.0,"kind":"comment"},{"t":700.0,"kind":"sub"},
   {"t":760.0,"kind":"like"},{"t":900.0,"kind":"comment"},{"t":1020.0,"kind":"sub"}])
open("data.js","w").write("window.DATA="+json.dumps(data)+";")
print([ (round(x["t1"]-x["t0"],2),x["t0"]) for x in shots if x["t1"]-x["t0"]>5]); print("END",END,"shots",len(shots)); print([ (s['img'],s['t0'],s['t1']) for s in shots[:8]])
L=[s['t1']-s['t0'] for s in shots]; print("shot len min %.2f max %.2f"%(min(L),max(L)))
