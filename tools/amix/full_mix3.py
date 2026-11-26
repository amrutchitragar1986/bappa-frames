# Part 3 + outro audio, spliced onto the existing layered master so Parts 1-2 audio stays sample-identical.
import numpy as np, soundfile as sf, json, librosa
from layers import *
C=json.load(open("/home/claude/skm/work/counter108v2.json"))["count_times_sec"]+[1086.42]
S=[C[n]+1.3 for n in range(1,109)]          # स्वाहा 1..108
END=1104.6; SPLICE=725.8
T0=700.0
music,_=librosa.load("/home/claude/skm/work/suno108v2_master.wav",sr=SR,mono=False,offset=T0)
n=int((END-T0)*SR); m=np.zeros((2,n),dtype=np.float32); m[:,:music.shape[1]]=music[:,:n]; del music
lay=np.zeros(n,dtype=np.float32)
def add(sig,t,gain_db):
    i=int((t-T0)*SR)
    if i>=n or i+len(sig)<=0: return
    a=max(0,i); b=min(n,i+len(sig)); lay[a:b]+=sig[a-i:b-i]*10**(gain_db/20)
def sfx(name):
    y,_=librosa.load(f"/home/claude/sfxzip/x/amrut-sfx/{name}.mp3",sr=SR); y=y/np.abs(y).max()
    f=int(0.02*SR); y[-f:]*=np.linspace(1,0,f); return y
bell,shim,shankh,riser,ring=sfx("temple-bell"),sfx("divine-shimmer"),sfx("shankh"),sfx("riser-short"),sfx("bell-ring")
fb=fire_bed(END-T0+1,seed=2)[:n].astype(np.float32); a=int((1099.0-T0)*SR); b=int((1103.5-T0)*SR); fb[a:b]*=np.linspace(1,0.25,b-a); fb[b:]*=0.25
add(fb,T0,-30); del fb
notes1=[554.37,830.61,698.46,1108.73]; notes2=[830.61,1108.73,698.46,830.61]; notes3=[698.46,830.61,1108.73,1396.91]
for k,s in enumerate(S):
    add(whoosh(seed=10+k),s-0.55,-22 if k<107 else -16)
    add(chime((notes1 if s<363.39 else notes2 if s<SPLICE else notes3)[k%4]),s+1.25,-27)
mile={11:S[10]+1.3,21:S[20]+1.3,51:S[50]+1.3,54:S[53]+1.3,81:S[80]+1.3,100:S[99]+1.3,108:S[107]+1.3}
for mm,t in mile.items():
    add(riser,t-2.0,-27)
    if mm==54: add(bell,t,-20); continue
    add(bell,t,-17); add(bell,t+1.1,-21); add(bell,t+2.0,-24); add(shim,t+0.1,-16)
add(shankh,mile[54]+0.6,-22)
for t in (478.0,598.0,842.0,962.0): add(shim,t,-14); add(bell,t+0.15,-24)
for t in (440.0,668.0,800.0,1040.0): add(shim,t,-18)
# poorna ahuti: fire swells when the coconut goes in
add(whoosh(seed=901),1060.6,-17); add(whoosh(seed=902),1062.4,-19)
# ending: shankh naada after the chant, aarti ghanti
add(shankh,1091.0,-8); add(shankh,1096.6,-5)
add(shim,1091.6,-15); add(bell,1099.2,-17)
t=1099.5; k=0
while t<1103.6: add(ring,t,-25-(k%3)); t+=0.55; k+=1
mix=m+lay[None,:]
old,_=sf.read("/home/claude/amix/full_layered.wav",start=int(T0*SR),stop=int(END*SR),dtype="float32"); old=old.T
w=slice(int(5*SR),int(25*SR)); g=float((old[:,w]*m[:,w]).sum()/(m[:,w]**2).sum())
i0=int((SPLICE-T0)*SR); out=mix[:,i0:]*g; del mix
x=int(0.5*SR); r=np.linspace(0,1,x,dtype=np.float32); out[:,:x]=old[:,i0:i0+x]*(1-r)+out[:,:x]*r
print("gain",round(20*np.log10(g),3),"first-sample diff",float(np.abs(out[:,0]-old[:,i0]).max()))
pk=np.abs(out).max(); print("part3 peak dB",round(20*np.log10(pk),2))
if pk>0.95:
    thr=0.85; s_=np.sign(out); a_=np.abs(out); over=a_>thr; a_[over]=thr+(1-thr)*np.tanh((a_[over]-thr)/(1-thr)); out=s_*a_
f=int(1.1*SR); out[:,-f:]*=np.linspace(1,0,f,dtype=np.float32)
sf.write("/home/claude/amix/part3_audio.wav",out.T,SR,subtype="PCM_24")
