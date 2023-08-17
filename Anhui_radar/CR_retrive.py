import numpy as np
def find_nearest(array,value):
    array=np.asarray(array)
    idx = (np.abs(array-value)).argmin()
    return idx
def CR_gen(ref,azimuth,n):
    CR_ref = dict()
    for i in range(n):
        ref_n = ref[str(i)]
        ref_azimuth = azimuth[str(i)]
        cir_ref = np.ones_like(720,ref_n.shape[1])*(-999)
        for azi in range(720):
            azimuth = 0.5*azi
            index_azi = find_nearest(ref_azimuth,azimuth)
            cir_ref[azi] = ref_n[index_azi]
        CR_ref[str(i)] = cir_ref
    trans_0 = CR_ref['0']
    trans_0 = np.where(trans_0 > -999, trans_0, -999)
    for m in range(len(CR_ref)):
        if m == 0:
            pass
        else:
            trans_ = CR_ref[str(m)]
            trans_ = np.where(trans_ > -999, trans_, -999)
            trans_0 = np.maximum(trans_, trans_0)
    trans_0 = np.where(trans_0 == -999, np.nan, trans_0)
    return trans_0
