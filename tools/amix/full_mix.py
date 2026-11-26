# Layered master for the whole 108 video: chant stays on top, layers sit 11-20 dB under it.
import numpy as np, soundfile as sf, json, librosa, pyloudnorm as pyln
from layers import *
C=json.load(open("/home/claude/skm/work/counter108v2.json"))["count_times_sec"]
S=[C[n]+1.3 for n in range(1,108)]
music,_=librosa.load("/home/claude/skm/work/suno108v2_master.wav",sr=SR,mono=False)
n=music.shape[1]; T=n/SR; lay=np.zeros(n)
def add(sig,t,gain_db):
    i=int(t*SR)
    if i>=n or i+len(sig)<=0: return
    a=max(0,i); b=min(n,i+len(sig)); lay[a:b]+=sig[a-i:b-i]*10**(gain_db/20)
def sfx(name):
    y,_=librosa.load(f"/home/claude/sfxzip/x/amrut-sfx/{name}.mp3",sr=SR); y=y/np.abs(y).max()
    f=int(0.02*SR); y[-f:]*=np.linspace(1,0,f); return y
bell,shim,shankh,riser=sfx("temple-bell"),sfx("divine-shimmer"),sfx("shankh"),sfx("riser-short")
add(fire_bed(T+1)[:n],0,-30)
notes1=[554.37,830.61,698.46,1108.73]; notes2=[830.61,1108.73,698.46,830.61]
for k,s in enumerate(S):
    add(whoosh(seed=10+k),s-0.55,-22)
    add(chime((notes1 if s<363.39 else notes2)[k%4]),s+1.25,-27)
mile={11:S[10]+1.3,21:S[20]+1.3,51:S[50]+1.3,54:S[53]+1.3}
for m,t in mile.items():
    add(riser,t-2.0,-27)
    if m==54: add(bell,t,-20); continue_sh=True
    else: add(bell,t,-17); add(bell,t+1.1,-21); add(bell,t+2.0,-24)
    add(shim,t+0.1,-16)
add(shankh,mile[54]+0.6,-22)                 # half mala: soft shankh
for t in (478.0,598.0): add(shim,t,-14); add(bell,t+0.15,-24)   # teaser cards
for t in (440.0,668.0): add(shim,t,-18)                          # light sweeps
mix=music+lay[None,:]
meter=pyln.Meter(SR); L=meter.integrated_loudness(mix.T); mix*=10**((-14.0-L)/20)
pk=np.abs(mix).max()
if pk>0.89: mix*=0.89/pk
print("LUFS before",round(L,2),"peak",round(20*np.log10(pk),2))
sf.write("/home/claude/amix/full_layered.wav",mix.T,SR,subtype="PCM_24")
