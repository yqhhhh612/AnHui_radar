import numpy as np
import matplotlib.pyplot as plt
from x_radar_scaninfo import read_scaninfo
import gzip
import struct
from xradarheader import Header_file, _prepare_for_read
def colormaps():
    import matplotlib.colors as colors
    cdict=[(1,1,1),
           (0,1,1),
           (0,157/255,1),
           (0,0,1),
           (9/255,130/255,175/255),
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
def read_dolp_vcp21(file):
    #四量读取
    fid = _prepare_for_read(file)
    file_header, site_config, task_config = Header_file(file)
    cut_num = task_config['Cut_number']  # 扫描层数
    #print('扫描层数：',cut_num)
    fid.seek(416 + 256 * cut_num)
    # 径向数据头
    flag = 1
    dBT_arr = []
    dBZ_arr = []
    V_arr = []
    W_arr = []
    AZIMUTH = []
    ELEVATION = []
    KEY = 0
    Radial_NO = []
    SEQUENCE_number=[]
    while (flag):
        # 径向头
        try:
            Radial_state, = struct.unpack('i', fid.read(4))
            if (Radial_state == 2):
                #print(Radial_state)
                KEY += 1
                if KEY == 11:
                    flag = Radial_state - 2
            Spot_blank, = struct.unpack('i', fid.read(4))
            Sequence_number, = struct.unpack('i', fid.read(4))
            SEQUENCE_number.append(Sequence_number)
            Radial_number, = struct.unpack('i', fid.read(4))
            Radial_NO.append(Radial_number)
            Elevation_number, = struct.unpack('i', fid.read(4))
            Azimuth, = struct.unpack('f', fid.read(4))
            AZIMUTH.append(Azimuth)

            Elevation, = struct.unpack('f', fid.read(4))
            ELEVATION.append(Elevation)
            Seconds, = struct.unpack('i', fid.read(4))
            Microseconds, = struct.unpack('i', fid.read(4))
            Length_of_data, = struct.unpack('i', fid.read(4))
            Moment_number, = struct.unpack('i', fid.read(4))
            fid.read(2)
            Hori_est_noise, = struct.unpack('h', fid.read(2))
            Vert_est_noise, = struct.unpack('h', fid.read(2))
            fid.read(14)
            # #径向数据块
            # #径向数据头
            # 数据类型1
            Data_type_dbt, = struct.unpack('i', fid.read(4))
            Scale_dbt, = struct.unpack('i', fid.read(4))
            Offset_dbt, = struct.unpack('i', fid.read(4))
            Bin_length_dbt, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_dbt, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_dbt = int(Length_dbt / Bin_length_dbt)
            dBT = np.frombuffer(fid.read(Length_dbt), 'H')
            dBT = np.where(dBT >= 5, (dBT - Offset_dbt) / Scale_dbt, np.nan)
            dBT = np.where(dBT > 80, np.nan, dBT)
            dBT = np.where(dBT<-5 ,np.nan,dBT)
            dBT_arr.append(dBT)
            # 数据类型2
            Data_type_dbz, = struct.unpack('i', fid.read(4))
            Scale_dbz, = struct.unpack('i', fid.read(4))
            Offset_dbz, = struct.unpack('i', fid.read(4))
            Bin_length_dbz, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_dbz, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_dbz = int(Length_dbz / Bin_length_dbz)
            dBZ = np.frombuffer(fid.read(Length_dbz), '<H')
            dBZ = np.where(dBZ >= 5, (dBZ - Offset_dbz) / Scale_dbz, np.nan)
            dBZ = np.where(dBZ > 80, np.nan, dBZ)
            dBZ = np.where(dBZ <-5, np.nan, dBZ)
            dBZ_arr.append(dBZ)
            # 数据类型3
            Data_type_v, = struct.unpack('i', fid.read(4))
            Scale_v, = struct.unpack('i', fid.read(4))
            Offset_v, = struct.unpack('i', fid.read(4))
            Bin_length_v, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_v, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_v = int(Length_v / Bin_length_v)
            V = np.frombuffer(fid.read(Length_v), 'H')
            V = np.where(V >= 5, (V - Offset_v) / Scale_v, np.nan)
            V_arr.append(V)
            # 数据类型4
            Data_type_w, = struct.unpack('i', fid.read(4))
            Scale_w, = struct.unpack('i', fid.read(4))
            Offset_w, = struct.unpack('i', fid.read(4))
            Bin_length_w, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_w, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_w = int(Length_w / Bin_length_w)
            W = np.frombuffer(fid.read(Length_w), '<H')
            W = np.where(W >= 5, (W - Offset_w) / Scale_w, np.nan)
            W_arr.append(W)
        except struct.error:
            break
    radial_number_ = np.array(Radial_NO)
    index_of = np.array(np.where(radial_number_==1))
    ppi_number = []
    for i in range(len(index_of[0][:])):
        ppi_number.append(index_of[0][i])
    ppi_number.append(SEQUENCE_number[-1])
    fid.close()
    VAL_ARR = {'dBT': dBT_arr, 'dBZ': dBZ_arr, 'V': V_arr, 'W': W_arr, 'azimuth': AZIMUTH,
               'elevation': ELEVATION,'ppi_number':ppi_number}
    return VAL_ARR
def read_dolp_vcp21_NO(file):
    fid = _prepare_for_read(file)
    file_header, site_config, task_config = Header_file(file)
    cut_num = task_config['Cut_number']  # 扫描层数
    print('扫描层数：',cut_num)
    fid.seek(416 + 256 * cut_num)
    # 径向数据头
    flag = 1
    dBT_arr = []
    dBZ_arr = []
    V_arr = []
    W_arr = []
    AZIMUTH = []
    ELEVATION = []
    KEY = 0
    RAYNUM = 0
    RAY_RECORD = [0]
    radial_num_set = []
    while (flag):
        # 径向头
        Radial_state, = struct.unpack('i', fid.read(4))
        RAYNUM+=1
        #print(RAYNUM)
        if (Radial_state==2):
            KEY+=1
            RAY_RECORD.append(RAYNUM)
            if KEY ==11:
                flag =  Radial_state-2

        Spot_blank, = struct.unpack('i', fid.read(4))
        Sequence_number, = struct.unpack('i', fid.read(4))
        Radial_number, = struct.unpack('i', fid.read(4))
        Elevation_number, = struct.unpack('i', fid.read(4))
        radial_num_set.append(Radial_number)
        Azimuth, = struct.unpack('f', fid.read(4))
        AZIMUTH.append(Azimuth)

        Elevation, = struct.unpack('f', fid.read(4))
        ELEVATION.append(Elevation)
        Seconds, = struct.unpack('i', fid.read(4))
        Microseconds, = struct.unpack('i', fid.read(4))
        Length_of_data, = struct.unpack('i', fid.read(4))
        Moment_number, = struct.unpack('i', fid.read(4))
        fid.read(2)
        Hori_est_noise, = struct.unpack('h', fid.read(2))
        Vert_est_noise, = struct.unpack('h', fid.read(2))
        fid.read(14)
        # print('径向数据状态:',Radial_state)
        # print( '消隐标志:',Spot_blank)
        # print('序号:',Sequence_number)
        # print('径向数:',Radial_number)
        # print('仰角编号:',Elevation_number)
        # print('方位角:',Azimuth)
        # print('仰角:',Elevation)
        # print('秒:',Seconds)
        # print('微秒:',Microseconds)
        # print('本径向块（径向数据头加数据）的数据长度:',Length_of_data)
        # print('数据类别数量:',Moment_number)
        # #径向数据块
        # #径向数据头
        # 数据类型1
        Data_type, = struct.unpack('i', fid.read(4))
        Scale, = struct.unpack('i', fid.read(4))
        Offset, = struct.unpack('i', fid.read(4))
        #print(Offset)
        Bin_length, = struct.unpack('h', fid.read(2))
        fid.read(2)
        Length, = struct.unpack('i', fid.read(4))
        fid.read(12)
        BINNUMBER = int(Length / Bin_length)
        dBT = np.frombuffer(fid.read(Length), 'H')
        dBT = np.where(dBT >= 5, (dBT - Offset) / Scale, np.nan)
        dBT = np.where(dBT > 80, np.nan,dBT)
        dBT_arr.append(dBT)

        # dBT = (dBT-Offset)/Scale
        # print('数据类型:',Data_type)
        # print('数据比例：',Scale)
        #print('偏移:',Offset)
        # print('库字节长度:',Bin_length)
        # print('距离库数据的长度:',Length)
        # print('库数：', BINNUMBER)
        #print(np.nanmax(dBT), np.nanmean(dBT), np.nanmin(dBT))
        # 数据类型2
        Data_type2, = struct.unpack('i', fid.read(4))
        Scale2, = struct.unpack('i', fid.read(4))
        Offset2, = struct.unpack('i', fid.read(4))
        Bin_length2, = struct.unpack('h', fid.read(2))
        fid.read(2)
        Length2, = struct.unpack('i', fid.read(4))
        fid.read(12)
        BINNUMBER2 = int(Length2 / Bin_length2)
        dBZ = np.frombuffer(fid.read(Length2), '<H')
        dBZ = np.where(dBZ >= 5, (dBZ - Offset2) / Scale2, np.nan)

        dBZ = np.where(dBZ > 80, np.nan, dBZ)
        dBZ_arr.append(dBZ)
        # 数据类型3
        Data_type3, = struct.unpack('i', fid.read(4))
        Scale3, = struct.unpack('i', fid.read(4))
        Offset3, = struct.unpack('i', fid.read(4))
        Bin_length3, = struct.unpack('h', fid.read(2))
        fid.read(2)
        Length3, = struct.unpack('i', fid.read(4))
        fid.read(12)
        BINNUMBER3 = int(Length3 / Bin_length3)
        V = np.frombuffer(fid.read(Length3), 'H')
        V = np.where(V >= 5, (V - Offset3) / Scale3, np.nan)
        #print(BINNUMBER3)
        V_arr.append(V)
        # 数据类型4
        Data_type4, = struct.unpack('i', fid.read(4))
        Scale4, = struct.unpack('i', fid.read(4))
        Offset4, = struct.unpack('i', fid.read(4))
        Bin_length4, = struct.unpack('h', fid.read(2))
        fid.read(2)
        Length4, = struct.unpack('i', fid.read(4))
        fid.read(12)
        BINNUMBER4 = int(Length4 / Bin_length4)
        W = np.frombuffer(fid.read(Length3), '<H')
        W = np.where(W >= 5, (W - Offset4) / Scale4, np.nan)
        W_arr.append(W)
    RAY_RECORD_ = np.zeros(len(RAY_RECORD))
    for i in range(len(RAY_RECORD)):
        if i <len(RAY_RECORD)-1:
            RAY_RECORD_[i] = RAY_RECORD[i+1]-RAY_RECORD[i]
    RAY_RECORD_ = RAY_RECORD_[:-1]
    fid.close()
    VAL_ARR = {'dBT': dBT_arr, 'dBZ': dBZ_arr, 'V': V_arr, 'W': W_arr, 'azimuth': AZIMUTH,
               'elevation': ELEVATION,'ray_num':RAY_RECORD_,'cal_ray_num':RAY_RECORD,'Radial_NO':radial_num_set}
    return VAL_ARR
def read_pol_vcp21D(file):
    import struct
    from xradarheader import Header_file, _prepare_for_read
    import numpy as np
    #数据类型编号[2, 3, 4, 1, 7, 11, 9, 10]
    #dBZ,V,W,dBT,ZDR,KDP,CC,PHDP

    fid = _prepare_for_read(file)
    file_header, site_config, task_config = Header_file(file)
    cut_num = task_config['Cut_number']  # 扫描层数
    #print('扫描层数：',cut_num)
    fid.seek(416 + 256 * cut_num)
    # 径向数据头
    dBT_arr = []
    dBZ_arr = []
    V_arr = []
    W_arr = []
    ZDR_arr = []
    KDP_arr = []
    CC_arr = []
    PHDP_arr = []

    AZIMUTH = []
    ELEVATION = []
    Radial_NO = []#层径向编号
    SEQUENCE_number=[]#文件径向编号
    while (True):
        # 径向头
        try:
            Radial_state, = struct.unpack('i', fid.read(4))
            Spot_blank, = struct.unpack('i', fid.read(4))
            Sequence_number, = struct.unpack('i', fid.read(4))
            SEQUENCE_number.append(Sequence_number)
            Radial_number, = struct.unpack('i', fid.read(4))
            Radial_NO.append(Radial_number)
            Elevation_number, = struct.unpack('i', fid.read(4))
            Azimuth, = struct.unpack('f', fid.read(4))
            AZIMUTH.append(Azimuth)
            Elevation, = struct.unpack('f', fid.read(4))
            ELEVATION.append(Elevation)
            Seconds, = struct.unpack('i', fid.read(4))
            Microseconds, = struct.unpack('i', fid.read(4))
            Length_of_data, = struct.unpack('i', fid.read(4))
            Moment_number, = struct.unpack('i', fid.read(4))
            fid.read(2)
            Hori_est_noise, = struct.unpack('h', fid.read(2))
            Vert_est_noise, = struct.unpack('h', fid.read(2))
            fid.read(14)
            # #径向数据块
            # #径向数据头
            # 数据类型1 dbz
            Data_type_dbz, = struct.unpack('i', fid.read(4))
            Scale_dbz, = struct.unpack('i', fid.read(4))
            Offset_dbz, = struct.unpack('i', fid.read(4))
            Bin_length_dbz, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_dbz, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_dbz = int(Length_dbz / Bin_length_dbz)
            dBZ = np.frombuffer(fid.read(Length_dbz), dtype='u1')
            dBZ = np.where(dBZ >= 5, (dBZ - Offset_dbz) / Scale_dbz, np.nan)
            dBZ = np.where(dBZ > 80, np.nan, dBZ)
            dBZ = np.where(dBZ <-5, np.nan, dBZ)
            dBZ_arr.append(dBZ)
            # 数据类型2 v
            Data_type_v, = struct.unpack('i', fid.read(4))
            Scale_v, = struct.unpack('i', fid.read(4))
            Offset_v, = struct.unpack('i', fid.read(4))
            Bin_length_v, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_v, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_v = int(Length_v / Bin_length_v)
            V = np.frombuffer(fid.read(Length_v), dtype='u1')
            V = np.where(V >= 5, (V - Offset_v) / Scale_v, np.nan)
            V_arr.append(V)
            # 数据类型3 w
            Data_type_w, = struct.unpack('i', fid.read(4))
            Scale_w, = struct.unpack('i', fid.read(4))
            Offset_w, = struct.unpack('i', fid.read(4))
            Bin_length_w, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_w, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_w = int(Length_w / Bin_length_w)
            W = np.frombuffer(fid.read(Length_w), dtype='u1')
            W = np.where(W >= 5, (W - Offset_w) / Scale_w, np.nan)
            W_arr.append(W)
            # 数据类型4 dbt
            Data_type_dbt, = struct.unpack('i', fid.read(4))
            Scale_dbt, = struct.unpack('i', fid.read(4))
            Offset_dbt, = struct.unpack('i', fid.read(4))
            Bin_length_dbt, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_dbt, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_dbt = int(Length_dbt / Bin_length_dbt)
            dBT = np.frombuffer(fid.read(Length_dbt), dtype='u1')
            dBT = np.where(dBT >= 5, (dBT - Offset_dbt) / Scale_dbt, np.nan)
            dBT = np.where(dBT > 80, np.nan, dBT)
            dBT = np.where(dBT<-5 ,np.nan,dBT)
            dBT_arr.append(dBT)
            #数据类型5 zdr
            Data_type_zdr, = struct.unpack('i', fid.read(4))
            Scale_zdr, = struct.unpack('i', fid.read(4))
            Offset_zdr, = struct.unpack('i', fid.read(4))
            Bin_length_zdr, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_zdr, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_zdr = int(Length_zdr / Bin_length_zdr)
            ZDR = np.frombuffer(fid.read(Length_zdr), dtype='u1')
            ZDR = np.where(ZDR >= 5, (ZDR - Offset_zdr) / Scale_zdr, np.nan)
            ZDR_arr.append(ZDR)
            #数据类型6 kdp
            Data_type_kdp, = struct.unpack('i', fid.read(4))
            Scale_kdp, = struct.unpack('i', fid.read(4))
            Offset_kdp, = struct.unpack('i', fid.read(4))
            Bin_length_kdp, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_kdp, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_kdp = int(Length_kdp / Bin_length_kdp)
            KDP = np.frombuffer(fid.read(Length_kdp), dtype='u1')
            KDP = np.where(KDP >= 5, (KDP - Offset_kdp) / Scale_kdp, np.nan)
            KDP_arr.append(KDP)
            #数据类型7 cc
            Data_type_cc, = struct.unpack('i', fid.read(4))
            Scale_cc, = struct.unpack('i', fid.read(4))
            Offset_cc, = struct.unpack('i', fid.read(4))
            Bin_length_cc, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_cc, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_cc = int(Length_cc / Bin_length_cc)
            CC = np.frombuffer(fid.read(Length_cc), dtype='u1')
            CC = np.where(CC >= 5, (CC - Offset_cc) / Scale_cc, np.nan)
            CC_arr.append(CC)
            #数据类型8 phdp
            Data_type_phdp, = struct.unpack('i', fid.read(4))
            Scale_phdp, = struct.unpack('i', fid.read(4))
            Offset_phdp, = struct.unpack('i', fid.read(4))
            Bin_length_phdp, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_phdp, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_phdp = int(Length_phdp / Bin_length_phdp)
            PHDP = np.frombuffer(fid.read(Length_phdp), dtype='H')
            PHDP = np.where(PHDP >= 5, (PHDP - Offset_phdp) / Scale_phdp, np.nan)
            PHDP_arr.append(PHDP)
        except struct.error:
            break
    radial_number_ = np.array(Radial_NO)
    index_of = np.array(np.where(radial_number_==1))
    ppi_number = []
    for i in range(len(index_of[0][:])):
        ppi_number.append(index_of[0][i])
    ppi_number.append(SEQUENCE_number[-1])
    fid.close()
    VAL_ARR = {'dBT': dBT_arr, 'dBZ': dBZ_arr, 'V': V_arr,
               'W': W_arr,'ZDR':ZDR_arr,'KDP':KDP_arr,
               'CC':CC_arr,'PHDP':PHDP_arr,'azimuth': AZIMUTH,
               'elevation': ELEVATION,'ppi_number':ppi_number}
    return VAL_ARR
def read_ppi(file):
    fid = _prepare_for_read(file)
    file_header, site_config, task_config = Header_file(file)
    cut_num = task_config['Cut_number']  # 扫描层数
    #print('扫描层数：',cut_num)
    fid.seek(416 + 256 * cut_num)
    # 径向数据头
    dBT_arr = []
    dBZ_arr = []
    V_arr = []
    W_arr = []
    ZDR_arr = []
    CC_arr = []
    AZIMUTH = []
    ELEVATION = []
    RAYNUM = 0
    Radial_NO = []
    SEQUENCE_number=[]
    while (True):
        try:
            Radial_state, = struct.unpack('i', fid.read(4))
            Spot_blank, = struct.unpack('i', fid.read(4))
            Sequence_number, = struct.unpack('i', fid.read(4))
            SEQUENCE_number.append(Sequence_number)
            Radial_number, = struct.unpack('i', fid.read(4))
            Radial_NO.append(Radial_number)
            Elevation_number, = struct.unpack('i', fid.read(4))
            Azimuth, = struct.unpack('f', fid.read(4))
            AZIMUTH.append(Azimuth)
            Elevation, = struct.unpack('f', fid.read(4))
            ELEVATION.append(Elevation)
            Seconds, = struct.unpack('i', fid.read(4))
            Microseconds, = struct.unpack('i', fid.read(4))
            Length_of_data, = struct.unpack('i', fid.read(4))
            Moment_number, = struct.unpack('i', fid.read(4))
            fid.read(2)
            Hori_est_noise, = struct.unpack('h', fid.read(2))
            Vert_est_noise, = struct.unpack('h', fid.read(2))
            fid.read(14)
            # 数据类型1 dBT
            Data_type_dbt, = struct.unpack('i', fid.read(4))
            Scale_dbt, = struct.unpack('i', fid.read(4))
            Offset_dbt, = struct.unpack('i', fid.read(4))
            # print(Offset)
            Bin_length_dbt, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_dbt, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_dbt = int(Length_dbt / Bin_length_dbt)
            dBT = np.frombuffer(fid.read(Length_dbt), 'H')
            dBT = np.where(dBT >= 5, (dBT - Offset_dbt) / Scale_dbt, np.nan)
            dBT = np.where(dBT > 80, np.nan, dBT)
            dBT_arr.append(dBT)
            # 数据类型2 dBZ
            Data_type_dbz, = struct.unpack('i', fid.read(4))
            Scale_dbz, = struct.unpack('i', fid.read(4))
            Offset_dbz, = struct.unpack('i', fid.read(4))
            Bin_length_dbz, = struct.unpack('h', fid.read(2))
            # print('库字节长度:',Bin_length2)
            fid.read(2)
            Length_dbz, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_dbz = int(Length_dbz / Bin_length_dbz)
            dBZ = np.frombuffer(fid.read(Length_dbz), 'H')
            dBZ = np.where(dBZ >= 5, (dBZ - Offset_dbz) / Scale_dbz, np.nan)
            # print(np.nanmean(dBZ),np.nanmedian(dBZ),np.nanmax(dBZ),np.nanmin(dBZ))
            # dBZ = np.where(dBZ > 80, np.nan, dBZ)
            dBZ_arr.append(dBZ)

            # 数据类型3 V
            Data_type_v, = struct.unpack('i', fid.read(4))
            Scale_v, = struct.unpack('i', fid.read(4))
            Offset_v, = struct.unpack('i', fid.read(4))
            Bin_length_v, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_v, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_v = int(Length_v / Bin_length_v)
            V = np.frombuffer(fid.read(Length_v), 'H')
            V = np.where(V >= 5, (V - Offset_v) / Scale_v, np.nan)
            # print(BINNUMBER3)
            V_arr.append(V)
            # 数据类型4 W
            Data_type_w, = struct.unpack('i', fid.read(4))
            Scale_w, = struct.unpack('i', fid.read(4))
            Offset_w, = struct.unpack('i', fid.read(4))
            Bin_length_w, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_w, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_w = int(Length_w / Bin_length_w)
            W = np.frombuffer(fid.read(Length_w), '<H')
            W = np.where(W >= 5, (W - Offset_w) / Scale_w, np.nan)
            W_arr.append(W)
            # 数据类型5 ZDR
            Data_type_zdr, = struct.unpack('i', fid.read(4))
            Scale_zdr, = struct.unpack('i', fid.read(4))
            Offset_zdr, = struct.unpack('i', fid.read(4))
            Bin_length_zdr, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_zdr, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_zdr = int(Length_zdr / Bin_length_zdr)
            ZDR = np.frombuffer(fid.read(Length_zdr), '<H')
            ZDR = np.where(ZDR >= 5, (ZDR - Offset_zdr) / Scale_zdr, np.nan)
            ZDR_arr.append(ZDR)
            for m in range(2):
                Data_type, = struct.unpack('i', fid.read(4))
                # print('数据类型：',Data_type)
                Scale, = struct.unpack('i', fid.read(4))
                Offset, = struct.unpack('i', fid.read(4))
                # print(Offset)
                Bin_length, = struct.unpack('h', fid.read(2))
                # print()
                fid.read(2)
                Length, = struct.unpack('i', fid.read(4))
                fid.read(12)
                # print('数据长度:',Length)
                fid.read(Length)
            # 数据类型8 CC
            Data_type_cc, = struct.unpack('i', fid.read(4))
            Scale_cc, = struct.unpack('i', fid.read(4))
            Offset_cc, = struct.unpack('i', fid.read(4))
            Bin_length_cc, = struct.unpack('h', fid.read(2))
            fid.read(2)
            Length_cc, = struct.unpack('i', fid.read(4))
            fid.read(12)
            BINNUMBER_cc = int(Length_cc / Bin_length_cc)
            CC = np.frombuffer(fid.read(Length_cc), '<H')
            CC = np.where(CC >= 5, (CC - Offset_cc) / Scale_cc, np.nan)
            CC_arr.append(CC)
        except struct.error:
            break
    radial_number_ = np.array(Radial_NO)
    index_of = np.array(np.where(radial_number_==1))
    ppi_number = []
    for i in range(len(index_of[0][:])):
        ppi_number.append(index_of[0][i])
    ppi_number.append(SEQUENCE_number[-1])
    fid.close()
    VAL_ARR = {'dBT': dBT_arr, 'dBZ': dBZ_arr, 'V': V_arr, 'W': W_arr, 'azimuth': AZIMUTH,
               'elevation': ELEVATION,'ray_num':SEQUENCE_number,'ppi_number':ppi_number}
    return VAL_ARR

def plot_data(file,binlength=0.075):
    #六变量读取
    VAL = read_dolp_vcp21(file)
    cal_record = VAL['ppi_number']
    dBZ = VAL['dBZ']
    print(cal_record)
    for m in range(len(cal_record)-1):
        dBZ_1 = dBZ[cal_record[m]:cal_record[m + 1]]
        dBZ_1 = np.array(dBZ_1)
        # print(dBZ_1.shape)
        # azimuth_1 = VAL['azimuth'][0:cal_record[0]-1]
        azimuth_1 = VAL['azimuth'][cal_record[m]:cal_record[m + 1]]
        nXarray = np.meshgrid(range(dBZ_1.shape[1]), range(dBZ_1.shape[0]))[0]  # z对应的x坐标
        nYarray = np.meshgrid(range(dBZ_1.shape[1]), range(dBZ_1.shape[0]))[0]
        for i in range(dBZ_1.shape[0]):
            for j in range(dBZ_1.shape[1]):
                nXarray[i][j] = np.sin(azimuth_1[i] / 180 * np.pi) * binlength * j
                nYarray[i][j] = np.cos(azimuth_1[i] / 180 * np.pi) * binlength * j
        plt.contourf(nXarray, nYarray, dBZ_1, np.arange(-5, 70, 5), cmap=colormaps())
        plt.xlabel('X(km)')
        plt.ylabel('Y(km)')
        plt.xlim(-180, 180)
        plt.ylim(-180, 180)
        plt.colorbar(label='dBZ', )
        plt.show()
def plot_cor_ref(file,binlength=0.075):
    VAL = read_dolp_vcp21(file)
    cal_record = VAL['ppi_number']
    dBZ = VAL['dBZ']
    print(cal_record)
    for m in range(len(cal_record)-1):
        dBZ_1 = dBZ[cal_record[m]:cal_record[m + 1]]
        dBZ_1 = np.array(dBZ_1)
        cor_zarray = np.zeros_like(dBZ_1)
        # print(dBZ_1.shape)
        # azimuth_1 = VAL['azimuth'][0:cal_record[0]-1]
        for i in range(dBZ_1.shape[0]):
            AH = 0
            for j in range(dBZ_1.shape[1]):
                if (False == np.isnan(dBZ_1[i][j])):
                    z1 = dBZ_1[i][j]
                    zh = pow(10, z1 / 10)
                    AH += 2 * pow(10, -4) * pow(zh, 0.779) * 0.15 * 1.37
                    cor_zarray[i][j] = z1 + AH
                else:
                    cor_zarray[i][j] = np.nan
        azimuth_1 = VAL['azimuth'][cal_record[m]:cal_record[m + 1]]
        nXarray = np.meshgrid(range(dBZ_1.shape[1]), range(dBZ_1.shape[0]))[0]  # z对应的x坐标
        nYarray = np.meshgrid(range(dBZ_1.shape[1]), range(dBZ_1.shape[0]))[0]
        for i in range(dBZ_1.shape[0]):
            for j in range(dBZ_1.shape[1]):
                nXarray[i][j] = np.sin(azimuth_1[i] / 180 * np.pi) * binlength * j
                nYarray[i][j] = np.cos(azimuth_1[i] / 180 * np.pi) * binlength * j
        plt.contourf(nXarray, nYarray, cor_zarray, np.arange(-5, 70, 5), cmap=colormaps())
        plt.xlabel('X(km)')
        plt.ylabel('Y(km)')
        plt.xlim(-180, 180)
        plt.ylim(-180, 180)
        plt.colorbar(label='dBZ', )
        plt.show()
