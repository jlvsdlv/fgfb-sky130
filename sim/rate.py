import numpy as np
def rate_from(d, frac=0.3, minswing=0.4):
    t,v=d[:,0],d[:,1]; T=t[-1]; m=t>T*frac
    tt,vv=t[m],v[m]; sw=vv.max()-vv.min()
    if sw<minswing: return 0.0, sw, None, None
    mid=(vv.max()+vv.min())/2
    k=np.where((vv[:-1]<mid)&(vv[1:]>=mid))[0]
    if len(k)<3: return 0.0, sw, vv.max(), vv.min()
    return 1/np.median(np.diff(tt[k])), sw, vv.max(), vv.min()
