import numpy as np

def ZH_gen(Z, a=1.37e-4, b=0.779, binlength=0.15):
    '''
    :param Z: reflectivity, numpy array (nrays,nbins) such as (360,920)
    :param a: parameters to calculate AH
    :param b: parameters to calculate AH
    :param binlength: bin length, such as 250m
    :return: corrected reflectivity array.
    '''
    AH = 0
    pia = np.zeros_like(Z)
    for i in range(Z.shape[1] - 1):
        # k = a * (10.0 ** ((Z[:, i] + AH) / 10.0)) ** b * 2.0 * binlength
        k = a * (10.0 ** ((Z[:, i]) / 10.0)) ** b * 2.0 * binlength
        k = np.where(np.isnan(k), 0, k)
        AH += k
        pia[:, i + 1] = AH
    Zc = np.where(np.isnan(Z), np.nan, pia + Z)
    return Zc


def ZH_KDP_gen(Z, KDP, binlength=0.15):
    '''
    :param Z: reflectivity,numpy array (nrays,nbins) such as (360,920)
    :param KDP: specific differential phase
    :param binlength:bin length, such as 250m
    :return: corrected reflectivity array.
    '''
    ZHnarray = np.zeros_like(Z)
    z_part_1 = np.where(Z[:, 0:400] > 34, -5, Z[:, 0:400])  # 去除靠近天线的异常值
    z_part_2 = Z[:, 400:]
    Z = np.hstack([z_part_1, z_part_2])
    for i in range(Z.shape[0]):
        AH = 0
        for j in range(Z.shape[1]):
            if False == np.isnan(Z[i, j]):
                z1 = Z[i, j]
                if 0.1 <= KDP[i, j] <= 3:
                    AH += 0.22 * binlength * 2 * KDP[i, j] / 2
                    ZHnarray[i, j] = z1 + AH
                else:
                    zh = pow(10, z1 / 10)
                    AH += 2 * pow(10, -4) * pow(zh, 0.779) * binlength * 1.37
                    ZHnarray[i, j] = z1 + AH
            else:
                ZHnarray[i, j] = Z[i, j]
    return ZHnarray
