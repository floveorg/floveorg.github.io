import numpy as np, wave
sr=22050
N={'C4':261.63,'E4':329.63,'G4':392.00,'C5':523.25,'F4':349.23,'A4':440.00,
   'D5':587.33,'B4':493.88,'G5':783.99,'E5':659.25,'C6':1046.50}
def tone(f,dur,harm):
    t=np.linspace(0,dur,int(sr*dur),False)
    w=np.zeros_like(t)
    for i,a in enumerate(harm,1): w+=a*np.sin(2*np.pi*f*i*t)
    return w
def envr(n,attack,release):
    e=np.ones(n); a=int(sr*attack); r=int(sr*release)
    if a>0: e[:a]=np.linspace(0,1,a)
    if r>0: e[-r:]*=np.linspace(1,0,r)
    return e
def chord(freqs,dur,attack,release,harm):
    n=int(sr*dur); w=np.zeros(n)
    for f in freqs: w+=tone(f,dur,harm)
    return w*envr(n,attack,release)/len(freqs)
def reverb(x):
    out=x.copy()
    for d,a in [(0.05,0.28),(0.11,0.18),(0.19,0.10)]:
        k=int(sr*d); out[k:]+=a*x[:len(x)-k]
    return out
def render(events,total,attack,release,harm):
    buf=np.zeros(int(sr*total))
    for t0,freqs,dur in events:
        c=chord(freqs,dur,attack,release,harm); s=int(sr*t0)
        buf[s:s+len(c)]+=c[:len(buf)-s]
    buf=reverb(buf)
    buf/=np.max(np.abs(buf))+1e-9; buf*=0.9
    f=int(sr*0.03); buf[:f]*=np.linspace(0,1,f)
    return buf
def save(name,buf):
    d=(np.clip(buf,-1,1)*32767).astype('<i2')
    with wave.open(name,'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(d.tobytes())

# A — apertura cálida: I-IV-V-I, pads con armónicos suaves
warm=(1,0.5,0.28,0.14)
A=[(0.0,[N['C4'],N['E4'],N['G4']],1.7),
   (1.4,[N['F4'],N['A4'],N['C5']],1.7),
   (2.8,[N['G4'],N['B4'],N['D5']],1.5),
   (4.0,[N['C4'],N['E4'],N['G4'],N['C5']],2.6)]
save('musicA.wav',render(A,6.7,0.05,0.9,warm))

# B — separador: campanita brillante, arpegio agudo y acorde corto
bell=(1,0.6,0.4,0.25,0.15)
B=[(0.00,[N['C5']],0.5),(0.16,[N['E5']],0.5),(0.32,[N['G5']],0.5),
   (0.48,[N['C6']],0.6),(0.72,[N['C5'],N['E5'],N['G5']],1.3)]
save('musicB.wav',render(B,2.3,0.005,0.5,bell))
print('A',round(6.7,2),'s  B',round(2.3,2),'s')
