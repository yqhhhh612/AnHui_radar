import numpy as np
def HCA_cal(Z,ZDR,ROHV):
    def f1(ZH):
        return -0.5 + 2.5 * 0.001 * ZH + 7.5 * 0.0001 * np.power(ZH, 2)

    def f2(ZH):
        return 0.68 - 4.81 * 0.01 * ZH + 2.92 * 0.001 * np.power(ZH, 2)

    def f3(ZH):
        return 1.42 + 6.67 * 0.01 * ZH + 4.85 * 0.0001 * np.power(ZH, 2)

    start_ = time.time()
    ZH_class = [[15, 20, 70, 80], [5, 10, 20, 30],
                [5, 10, 35, 40], [25, 30, 40, 50],
                [0, 5, 20, 25], [25, 35, 50, 55],
                [20, 25, 45, 50], [5, 10, 45, 50],
                [40, 45, 55, 60], [45, 50, 75, 80]]
    ZH_class = np.array(ZH_class)

    ZDR_class = [[-4, -2, 1, 2], [0, 2, 10, 12], [-0.3, 0.0, 0.3, 0.6],
                 [0.5, 1.0, 2.0, 3.0], [0.1, 0.4, 3.0, 3.3],
                 [-0.3, 0.0, f1(50), f1(55) + 0.3],
                 [f2(20) - 0.3, f2(25), f3(45), f3(50) + 0.1],
                 [f1(5) - 0.3, f1(10), f2(45), f2(50) + 0.5],
                 [f1(40) - 0.3, f1(45), f2(55), f2(60) + 0.5],
                 [-0.3, 0.0, f1(75), f1(80) + 0.5]]
    ZDR_class = np.array(ZDR_class)

    ROHV_class = [[0.5, 0.6, 0.9, 0.95], [0.3, 0.5, 0.8, 0.83],
                  [0.95, 0.98, 1, 1.01], [0.88, 0.92, 0.95, 0.985],
                  [0.95, 0.98, 1.00, 1.01], [0.9, 0.97, 1, 1.01],
                  [0.92, 0.95, 1, 1.01], [0.95, 0.97, 1, 1.01],
                  [0.92, 0.95, 1, 1.01], [0.85, 0.9, 1, 1.01]]
    ROHV_class = np.array(ROHV_class)

    p_ZH = [0.2, 0.4, 1, 0.6, 1, 0.8, 0.8, 1, 1, 1]
    p_ZH = np.array(p_ZH)

    p_ZDR = [0.4, 0.6, 0.8, 0.8, 0.6, 1, 1, 0.8, 0.8, 0.8]
    p_ZDR = np.array(p_ZDR)

    p_ROHV = [1, 1, 0.6, 1, 0.4, 0.4, 0.6, 0.6, 0.6, 0.6]
    p_ROHV = np.array(p_ROHV)

    def func_x1x2(x1, x2):
        k = 1 / (x2 - x1)
        b = -x1 / (x2 - x1)
        return k, b

    def func_x2x3(x2, x3):
        k = 0
        b = 1
        return k, b

    def func_x3x4(x3, x4):
        k = -(1 / (x4 - x3))
        b = x4 / (x4 - x3)
        return k, b

    # 系数,按照斜率和截距为一组保存三条线
    record_zh = []

    record_zdr = []

    record_rohv = []

    for i in range(10):
        zh1, zh2 = func_x1x2(ZH_class[i][0], ZH_class[i][1])
        zh3, zh4 = func_x3x4(ZH_class[i][2], ZH_class[i][3])
        aa_1 = [zh1, zh2, 0, 1, zh3, zh4]
        record_zh.append(aa_1)  # ZH系数

        zdr1, zdr2 = func_x1x2(ZDR_class[i][0], ZDR_class[i][1])
        zdr3, zdr4 = func_x3x4(ZDR_class[i][2], ZDR_class[i][3])
        aa_2 = [zdr1, zdr2, 0, 1, zdr3, zdr4]
        record_zdr.append(aa_2)  # ZDR系数

        rohv1, rohv2 = func_x1x2(ROHV_class[i][0], ROHV_class[i][1])
        rohv3, rohv4 = func_x3x4(ROHV_class[i][2], ROHV_class[i][3])
        aa_3 = [rohv1, rohv2, 0, 1, rohv3, rohv4]
        record_rohv.append(aa_3)  # ROHV系数
    record_zh = np.array(record_zh)
    record_zdr = np.array(record_zdr)
    record_rohv = np.array(record_rohv)
    Classfi_arr = np.zeros_like(Z)
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            A_coll = []
            if (np.isnan(Z[i][j]) == False) and (np.isnan(ZDR[i][j]) == False) and np.isnan(ROHV[i][j]) == False:
                for m in range(10):
                    A2 = p_ZH[m] + p_ZDR[m] + p_ROHV[m]
                    if ZH_class[m][0] <= Z[i][j] < ZH_class[m][1]:
                        if ZDR_class[m][0] <= ZDR[i][j] < ZDR_class[m][1]:
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + \
                                     (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m] + \
                                     (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:  # 概率为1
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + \
                                     (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m] + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + \
                                     (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m] + \
                                     (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + \
                                     (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m]
                                A_coll.append(A1 / A2)
                        elif ZDR_class[m][1] <= ZDR[i][j] < ZDR_class[m][2]:  # ZDR概率为1
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:  # 第一段
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + p_ZDR[m] + \
                                     (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:  # 概率为第二段
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + p_ZDR[m] + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:  # 第三段
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + p_ZDR[m] + \
                                     (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + p_ZDR[m]
                                A_coll.append(A1 / A2)
                        elif ZDR_class[m][2] <= ZDR[i][j] < ZDR_class[m][3]:  # ZDR第三段
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + \
                                     (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m] + \
                                     (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:  # 概率为1
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + \
                                     (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m] + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + \
                                     (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m] + \
                                     (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + \
                                     (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m]
                                A_coll.append(A1 / A2)
                        else:
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + \
                                     (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m]) + \
                                     (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = (record_zh[m][0] * Z[i][j] + record_zh[m][1]) * (p_ZH[m])
                                A_coll.append(A1 / A2)
                    elif ZH_class[m][1] <= Z[i][j] < ZH_class[m][2]:
                        if ZDR_class[m][0] <= ZDR[i][j] < ZDR_class[m][1]:
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = p_ZH[m] + (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m] + \
                                     (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:
                                A1 = p_ZH[m] + (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m] + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:
                                A1 = p_ZH[m] + (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m] + \
                                     (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = p_ZH[m] + (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m]
                                A_coll.append(A1 / A2)
                        elif ZDR_class[m][1] <= ZDR[i][j] < ZDR_class[m][2]:  # 第二段
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = p_ZH[m] + p_ZDR[m] + (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[
                                    m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:  # 第二段
                                A1 = p_ZH[m] + p_ZDR[m] + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:  # 第二段
                                A1 = p_ZH[m] + p_ZDR[m] + (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[
                                    m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = p_ZH[m] + p_ZDR[m]
                                A_coll.append(A1 / A2)
                        elif ZDR_class[m][2] <= ZDR[i][j] < ZDR_class[m][3]:  # 第三段
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = p_ZH[m] + (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m] + \
                                     (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:  # 第二段
                                A1 = p_ZH[m] + (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m] + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:  # 第二段
                                A1 = p_ZH[m] + (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m] + \
                                     (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = p_ZH[m] + (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m]
                                A_coll.append(A1 / A2)
                        else:
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = p_ZH[m] + (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:  # 第二段
                                A1 = p_ZH[m] + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:  # 第二段
                                A1 = p_ZH[m] + (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = p_ZH[m]
                                A_coll.append(A1 / A2)
                    elif ZH_class[m][2] <= Z[i][j] < ZH_class[m][3]:
                        if ZDR_class[m][0] <= ZDR[i][j] < ZDR_class[m][1]:
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + \
                                     (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m] + \
                                     (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + \
                                     (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m] + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + \
                                     (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m] + \
                                     (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + \
                                     (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m]
                                A_coll.append(A1 / A2)
                        elif ZDR_class[m][1] <= ZDR[i][j] < ZDR_class[m][2]:
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + \
                                     p_ZDR[m] + (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + \
                                     p_ZDR[m] + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + \
                                     p_ZDR[m] + (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + p_ZDR[m]
                                A_coll.append(A1 / A2)
                        elif ZDR_class[m][2] <= ZDR[i][j] < ZDR_class[m][3]:
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + \
                                     (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m] + \
                                     (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + \
                                     (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m] + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + \
                                     (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m] + \
                                     (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + \
                                     (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m]
                                A_coll.append(A1 / A2)
                        else:
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + \
                                     (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m]) + \
                                     (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = (record_zh[m][4] * Z[i][j] + record_zh[m][5]) * (p_ZH[m])
                                A_coll.append(A1 / A2)
                    else:
                        if ZDR_class[m][0] <= ZDR[i][j] < ZDR_class[m][1]:
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m] + \
                                     (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:
                                A1 = (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m] + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:
                                A1 = (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m] + \
                                     (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = (record_zdr[m][0] * ZDR[i][j] + record_zdr[m][1]) * p_ZDR[m]
                                A_coll.append(A1 / A2)
                        elif ZDR_class[m][1] <= ZDR[i][j] < ZDR_class[m][2]:
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = p_ZDR[m] + (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:
                                A1 = p_ZDR[m] + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:
                                A1 = p_ZDR[m] + (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = p_ZDR[m]
                                A_coll.append(A1 / A2)
                        elif ZDR_class[m][2] <= ZDR[i][j] < ZDR_class[m][3]:
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m] + \
                                     (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:
                                A1 = (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m] + p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:
                                A1 = (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m] + \
                                     (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A1 = (record_zdr[m][4] * ZDR[i][j] + record_zdr[m][5]) * p_ZDR[m]
                                A_coll.append(A1 / A2)
                        else:
                            if ROHV_class[m][0] <= ROHV[i][j] < ROHV_class[m][1]:
                                A1 = (record_rohv[m][0] * ROHV[i][j] + record_rohv[m][1]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][1] <= ROHV[i][j] < ROHV_class[m][2]:
                                A1 = p_ROHV[m]
                                A_coll.append(A1 / A2)
                            elif ROHV_class[m][2] <= ROHV[i][j] < ROHV_class[m][3]:
                                A1 = (record_rohv[m][4] * ROHV[i][j] + record_rohv[m][5]) * p_ROHV[m]
                                A_coll.append(A1 / A2)
                            else:
                                A_coll.append(0)
            A_coll = np.array(A_coll)
            try:
                ma = np.argmax(A_coll)
                Classfi_arr[i][j] = ma + 1
            except ValueError:
                Classfi_arr[i][j] = 0
                continue
    Classfi_arr = np.where(Classfi_arr == 0, np.nan, Classfi_arr)
    return Classfi_arr
