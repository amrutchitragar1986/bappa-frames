import numpy as np, soundfile as sf, json, librosa
from scipy import signal
SR=48000
def fire_bed(dur,seed=1):
    rng=np.random.default_rng(seed); n=int(dur*SR)
    roar=rng.standard_normal(n); roar=signal.sosfilt(signal.butter(2,[60,700],'bp',fs=SR,output='sos'),roar)
    mod=1+0.35*signal.sosfilt(signal.butter(1,1.5,'lp',fs=SR,output='sos'),rng.standard_normal(n))*6
    roar*=np.clip(mod,0.3,2.0)
    cr=np.zeros(n); k=0
    while k<n:
        k+=int(rng.exponential(SR/14)); 
        if k>=n: break
        L=int(SR*rng.uniform(0.002,0.012)); amp=rng.uniform(0.2,1.0)**2
        burst=rng.standard_normal(L)*np.exp(-np.linspace(0,6,L))*amp
        cr[k:k+L]+=burst[:max(0,min(L,n-k))]
    cr=signal.sosfilt(signal.butter(2,[1200,9000],'bp',fs=SR,output='sos'),cr)
    x=roar/np.abs(roar).max()*0.5+cr/np.abs(cr).max()*0.6
    return x/np.abs(x).max()
def whoosh(dur=2.2,seed=3):
    rng=np.random.default_rng(seed); n=int(dur*SR); t=np.arange(n)/SR
    x=rng.standard_normal(n); env=np.exp(-((t-0.55)/0.35)**2)*(t<0.55)+np.exp(-(t-0.55)/0.6)*(t>=0.55)
    out=np.zeros(n); 
    for i in range(0,n,2400):  # sweeping band
        fc=300+2500*np.exp(-((i/SR-0.5)/0.4)**2); seg=x[i:i+2400]
        out[i:i+2400]=signal.sosfilt(signal.butter(2,[max(80,fc*0.4),min(12000,fc*2.2)],'bp',fs=SR,output='sos'),seg)
    low=signal.sosfilt(signal.butter(2,120,'lp',fs=SR,output='sos'),x)*3
    y=(out+low)*env; return y/np.abs(y).max()
def chime(f0,dur=2.5):
    t=np.arange(int(dur*SR))/SR; y=np.zeros_like(t)
    for k,(m,a,d) in enumerate([(1,1,1.6),(2.0,.35,1.0),(3.0,.2,.6),(4.2,.12,.4),(5.4,.08,.3)]):
        y+=a*np.sin(2*np.pi*f0*m*t)*np.exp(-t/d)
    y*=np.minimum(1,t/0.004); return y/np.abs(y).max()
def load(path):
    y,sr=librosa.load(path,sr=SR,mono=True); return y/np.abs(y).max()
