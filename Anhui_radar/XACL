'''
This is a new method for X-band weather radar attenuation correction.
The model is a trained based on lightGBM called XACL 
9 variables are required:
ZH(X-band radar reflectivity),ZDR(differential reflectivity),
KDP(differential phase shift rate),PHDP(differential phase shift),
ROHV(copolarization correlation coefficient),V(doppler velocity),
W(spectrum width),range(distance from radar antenna),
meanZH(the average reflectivity between range gates and radar antenna).

'''
import joblib
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
def meanz(Z):
    import numpy as np
    MeanZarray = np.zeros_like(Z)
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            try:
                if j == 0:
                    MeanZarray[i][j] = MeanZarray[i][j]
                elif j == Z.shape[1] - 1:
                    MeanZarray[i][j] = np.nanmean(Z[i][:j])
                else:
                    MeanZarray[i][j] = np.nanmean(Z[i][:j + 1])
            except RuntimeWarning:
                MeanZarray[i][j]=np.nan
    return MeanZarray
def x_meanz_1(Z):
    import numpy as np
    MeanZarray = np.zeros_like(Z)
    for m in range(Z.shape[1]):
        if m == 0:
            MeanZarray[:,m] = Z[:,m]
        elif m == Z.shape[1]-1:
            MeanZarray[:,m] = np.nanmean(Z[:,:m],axis=1)
        else:
            MeanZarray[:,m] = np.nanmean(Z[:,:m+1],axis=1)
    return MeanZarray
def x_distamce_gen(Z):
    import numpy as np
    distance = np.zeros_like(Z)
    for k2 in range(Z.shape[1]):
        distance[:,k2] = 0.15*(k2+1)
    return distance
def x_KDP_gen(PHDParray):
    import numpy as np
    KDParray = np.zeros_like(PHDParray)
    number_rays = PHDParray.shape[0]
    ucbinnumber = PHDParray.shape[1]
    for aa in range(number_rays):
        for bb in range(ucbinnumber):
            if (bb != ucbinnumber - 1):
                if(False==np.isnan(PHDParray[aa][bb])and False==np.isnan(PHDParray[aa][bb+1])):
                    KDParray[aa][bb]=(PHDParray[aa][bb+1]-PHDParray[aa][bb])/0.3
            elif(bb==ucbinnumber-1):
                if (False == np.isnan(PHDParray[aa][bb]) and False == np.isnan(PHDParray[aa][bb -1])):
                    KDParray[aa][bb] = (PHDParray[aa][bb] - PHDParray[aa][bb-1]) / 0.3
    KDParray=np.where(KDParray==0,np.nan,KDParray)
    return KDParray
def read_var(filepath):
    import struct
    import numpy as np
    import os
    #filepath = './VTB20210727152352.010'
    size = os.path.getsize(filepath)
    binfile = open(filepath, 'rb')
    find1 = binfile.read()
    ray_size = 24011  # 原始数据块的大小，即一根径向所有的数据所占大小
    nrays = (size - 2060) / ray_size  # 总径向条数
    # 统计仰角及其个数，由此判断PPI的层数
    elevations = []  # 仰角
    Azimuths = []  # 方位角
    x_elevations = dict()
    x_azimuth = dict()
    x_Z = dict()
    x_Distance = dict()
    x_PHDP = dict()
    x_KDP = dict()
    x_V = dict()
    x_W = dict()
    x_ZDR = dict()
    x_meanz = dict()
    x_ROHV = dict()
    for i in range(int(nrays)):
        e1, = struct.unpack('h', find1[2060 + i * ray_size:2062 + i * ray_size])  # 仰角数据
        A1, = struct.unpack('H', find1[2062 + i * ray_size:2064 + i * ray_size])  # 方位角数据
        e1 = e1 / 100  # 换算成实际大小的角度
        A2 = A1 / 100
        Azimuths.append(A2)  # 所有方位角的集合
        elevations.append(e1)  # 所有仰角的集合
    # 读取位于头文件中的径向条数记录
    usRecordNumber = []  # 存放径向条数
    for i in range(10):
        ss, = struct.unpack('H', find1[264 + i * 35:266 + i * 35])
        usRecordNumber.append(ss)
    leijianumber = 0  # 存储前面ppi的径向数
    for num in range(10):
        ucbinnumber = 1000
        number_rays = int(usRecordNumber[num])  # 各层径向数
        ppiazimuth = np.zeros(number_rays)  # 存放各层的径向对应的方位角，数量与该层的径向数相同
        ppielevation = np.zeros(number_rays)  # 存放各层的径向对应的方位角，数量与该层的径向数相同
        for k in range(number_rays):
            ppiazimuth[k] = Azimuths[leijianumber + k]  # 提取出方位角
            ppielevation[k] = elevations[leijianumber + k]  # 提取出仰角
        x_elevations[str(num)] = ppielevation
        x_azimuth[str(num)] = ppiazimuth
        distance = np.zeros((number_rays, ucbinnumber))  # 数组对应的径距
        nZarray = np.zeros((number_rays, ucbinnumber))
        nXarray = np.meshgrid(range(ucbinnumber), range(number_rays))[0]  # z对应的x坐标
        nYarray = np.meshgrid(range(ucbinnumber), range(number_rays))[0]  # z对应的y坐标
        ZDRarray = np.zeros_like(nZarray)
        PHDParray = np.zeros_like(nZarray)  #
        KDParray = np.zeros((number_rays, ucbinnumber))  # KDP
        ROHVarray = np.zeros((number_rays, ucbinnumber))  # 相关系数
        Varray = np.zeros_like(nZarray)  # 速度
        Warray = np.zeros_like(nZarray)  # 谱宽
        MeanZarray = np.zeros_like(nZarray)  # 平均径向反射率
        cornZarray = np.zeros_like(nZarray)
        ZHnZarray = np.zeros_like(nZarray)
        for m in range(number_rays):
            z = np.frombuffer(find1[
                              2071 + m * ray_size + leijianumber * ray_size:2071 + m * ray_size + ucbinnumber + leijianumber * ray_size],
                              dtype='u1')  # 一次性提取出一条径向的z值并输出为数组
            nZarray[m] = np.where(z != 0, (z.astype(float) - 64.0) / 2., np.nan).astype(float)
            w = np.frombuffer(find1[
                              8071 + m * ray_size + leijianumber * ray_size:8071 + m * ray_size + ucbinnumber + leijianumber * ray_size],
                              dtype='u1')  # 一次性提取出一条径向的z值并输出为数组
            Warray[m] = np.where(w != 0, (w.astype(float) * 14.4) / 512, np.nan).astype(float)
            v = np.frombuffer(find1[
                              6071 + m * ray_size + leijianumber * ray_size:6071 + m * ray_size + ucbinnumber + leijianumber * ray_size],
                              dtype='u1')
            Varray[m] = np.where(v != -128, v.astype(float) * 14.4 / 127, np.nan).astype(float)
        for a in range(number_rays):
            for b in range(ucbinnumber):
                phdp, = struct.unpack('h', find1[
                                           14071 + b * 2 + a * ray_size + leijianumber * ray_size:14073 + b * 2 + a * ray_size + leijianumber * ray_size])
                zdr, = struct.unpack('h', find1[
                                          10071 + b * 2 + a * ray_size + leijianumber * ray_size:10073 + b * 2 + a * ray_size + leijianumber * ray_size])
                roh, = struct.unpack('h', find1[
                                          18071 + b * 2 + a * ray_size + leijianumber * ray_size:18073 + b * 2 + a * ray_size + leijianumber * ray_size])
                if (phdp != -0x8000):
                    PHDParray[a][b] = phdp / 100
                    ZDRarray[a][b] = zdr / 100
                else:
                    PHDParray[a][b] = np.nan
                    ZDRarray[a][b] = np.nan
                if (roh != 0):
                    ROHVarray[a][b] = roh / 1000
                else:
                    ROHVarray[a][b] = np.nan
                try:
                    if b == 0:
                        MeanZarray[a][b] = MeanZarray[a][b]
                    elif b == ucbinnumber - 1:
                        MeanZarray[a][b] = np.nanmean(nZarray[a][:b])
                    else:
                        MeanZarray[a][b] = np.nanmean(nZarray[a][:b + 1])
                except RuntimeWarning:
                    MeanZarray[a][b] = np.nan

        # kdp
        PHDParray = np.where(PHDParray < 0, PHDParray + 360, PHDParray)
        for aa in range(number_rays):
            for bb in range(ucbinnumber):
                if (bb != ucbinnumber - 1):
                    if (False == np.isnan(PHDParray[aa][bb]) and False == np.isnan(PHDParray[aa][bb + 1])):
                        KDParray[aa][bb] = (PHDParray[aa][bb + 1] - PHDParray[aa][bb]) / 0.3
                elif (bb == ucbinnumber - 1):
                    if (False == np.isnan(PHDParray[aa][bb]) and False == np.isnan(PHDParray[aa][bb - 1])):
                        KDParray[aa][bb] = (PHDParray[aa][bb] - PHDParray[aa][bb - 1]) / 0.3
        KDParray = np.where(KDParray == 0, np.nan, KDParray)
        for k2 in range(number_rays):
            for n in range(1000):
                distance[k2][n] = 0.15 * (n + 1)  # 库的距离
        x_Z[str(num)] = nZarray
        x_PHDP[str(num)] = PHDParray
        x_KDP[str(num)] = KDParray
        x_ZDR[str(num)] = ZDRarray
        x_meanz[str(num)] = MeanZarray
        x_V[str(num)] = Varray
        x_W[str(num)] = Warray
        x_Distance[str(num)] = distance
        x_ROHV[str(num)] = ROHVarray
        leijianumber += number_rays
    binfile.close()
    return x_elevations,x_azimuth,x_KDP,x_PHDP,x_ROHV,x_V,x_W,x_meanz,x_Distance,x_ZDR,x_Z
def colormaps_1():
    import matplotlib.colors as colors
    cdict=[(0,1,1),
           (0,157/255,1),
           (0,0,1),
           (9/255,130/255,175/255),
           'palegreen',
           (0,1,0),
           (8/255,175/255,20/255),
           (1,214/255,0),
           (1,152/255,0),
           (1,0,0),
           (221/255,0,27/255),
           (188/255,0,54/255),
           (121/255,0,109/255),
           (121/255,51/255,160/255),
           (195/255,163/255,212/255)]
    return (colors.ListedColormap(cdict,"indexed"))
import time
from x_radar_io import read_vw,read_xz,read_zdr,read_rohv,read_phdp
start = time.time()
file = r'E:\有效数据\20210708\150\VTB20210708104642.010'
#model=joblib.load('./x雷达订正处理\XACL_MODEL.h5')
model=joblib.load(r'路径+模型文件名')
test_0=np.zeros((1,9))
pre_0=model.predict(test_0)
x_Z,x_azi,x_ele = read_xz(file)
V,W = read_vw(file)
PHDP = read_phdp(file)
ROHV = read_rohv(file)
ZDR = read_zdr(file)
end1 = time.time()
print('读取用时',end1-start)
x_meanz = dict()
x_distance = dict()
x_KDP = dict()
for i in range(10):
    x_meanz[str(i)] = x_meanz_1(x_Z[str(i)])
    x_distance[str(i)] = x_distamce_gen(x_Z[str(i)])
    x_KDP[str(i)] = x_KDP_gen(PHDP[str(i)])
cor_z = dict()
for m in tqdm(range(10),ncols=50):
    ucbinnumber = 1000
    number_rays = x_Z[str(m)].shape[0]
    nXarray = np.meshgrid(range(ucbinnumber), range(number_rays))[0]  # z对应的x坐标
    nYarray = np.meshgrid(range(ucbinnumber), range(number_rays))[0]  # z对应的y坐标
    x_test = np.stack([x_KDP[str(m)],
              PHDP[str(m)],
              ROHV[str(m)],
              V[str(m)],
              W[str(m)],
              x_meanz[str(m)],
              x_distance[str(m)],
              ZDR[str(m)],x_Z[str(m)]])
    #x_test=np.stack([KDParray,PHDParray,ROHVarray,Varray,Warray,MeanZarray,distance,ZDRarray,nZarray])
    x_test=np.transpose(x_test,[1,2,0])
    x_test = x_test.reshape(-1,9)
    mask = np.where(np.isnan(x_test))
    x_test[mask[0]] = 0
    cornZarray = model.predict(x_test)
    cornZarray = cornZarray.reshape(x_Z[str(m)].shape[0],1000)
    cornZarray=np.where(cornZarray==pre_0,x_Z[str(m)],cornZarray)
    cor_z[str(m)] = cornZarray
    for i1 in range(number_rays):
        for j1 in range(1000):
            nXarray[i1][j1] = np.sin(x_azi[str(m)][i1]/180*np.pi)*0.15*j1*np.cos(x_ele[str(m)][i1]/180*np.pi)
            nYarray[i1][j1] = np.cos(x_azi[str(m)][i1]/180*np.pi)*0.15*j1*np.cos(x_ele[str(m)][i1]/180*np.pi)
    #plt.title(observer_year+'年'+observer_month+'月'+observer_day+'日'+observer_hour+'时'+observer_minute+'分'+observer_second+'秒起测'+'%.1f度仰角RFR订正雷达反射率PPI'%t[num])
    plt.contourf(nXarray, nYarray, cornZarray, np.arange(-5, 75, 5), cmap=colormaps_1(),zorder=2)
    plt.grid(zorder=1)
    plt.xlabel('X(km)')
    plt.ylabel('Y(km)')
    plt.xlim(-150, 150)
    plt.ylim(-150, 150)
    plt.colorbar(label='dBZ', )
    plt.show()
#m = read_var('./VTB20210727152352.010')
end2 = time.time()
print('全过程用时',end2-start)
