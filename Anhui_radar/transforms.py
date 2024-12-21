def PoleToPole(lonA,latA,hA,lonB,latB,hB,ap,ep,Lp):
    from math import cos,sin,acos,asin,atan2,pi,radians
    '''
    :param lonA: A雷达的经度
    :param latA: A雷达的纬度
    :param hA: A雷达的海拔高度，单位千米
    :param lonB: B雷达的经度
    :param latB: B雷达的纬度
    :param hB: B雷达的海拔高度，单位千米
    :param ap: 具体库相对于A的方位角
    :param ep: 具体库相对于A的仰角
    :param Lp: 具体库相对于A斜距
    :return: 该库相对于B的方位角、仰角和斜距
    所有参与运算的角度的单位均为弧度
    输出的结果均为角度单位
    '''
    #参数准备以及单位统一
    ap=radians(ap)
    ep=radians(ep)
    Re=6371.393#地球半径
    Rm=4/3*Re#等效地球半径
    lonA=radians(lonA)
    latA=radians(latA)
    lonB=radians(lonB)
    latB=radians(latB)
    #求出探测点的经纬度和高度
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',RuntimeWarning)
        H = hA + Lp * sin(ep) + (Lp * Lp * cos(ep) * cos(ep)) / (2 * Re)  # 此处求出H
        s = Rm * asin((Lp * cos(ep)) / (Rm + H))  # 两点地表距离
        lat = asin(cos(s / Re) * sin(latA) + sin(s / Re) * cos(latA) * cos(ap))

        lon = asin((sin(ap) * sin(s / Re)) / cos(lat)) + lonA  # 单位统一
        # 求测点相对于B点的方位角仰角和斜距
        ss = Re * acos(sin(lat) * sin(latB) + cos(lat) * cos(latB) * cos(lon - lonB))
    ed=atan2((cos(ss/Rm)-Rm/(Rm+H-hB)),sin(ss/Rm))
    ld=(Rm+H-hB)*sin(ss/Rm)/cos(ed)
    aa=asin(cos(lat)*sin(lon-lonB)/sin(ss/Re))
    if lon>=lonB:
        if lat>=latB:
            ad=aa
            ad=ad*180/pi
        else:
            ad=pi-aa
            ad = ad * 180 / pi
    else:
        if lat>=latB:
            ad=2*pi+aa
            ad = ad * 180 / pi
        else:
            ad=pi-aa
            ad = ad * 180 / pi
    ed=ed*180/pi
    return ad,ed,ld
  
 def arrayround(arr,n=0):
    flag = np.where(arr>=0,1,-1)
    arr = np.abs(arr)
    arr10 = arr*10**(n+1)
    arr20 = np.floor(arr10)
    arr30 = np.where(arr20%10==5,(arr20+1)/10**(n+1),arr20/10**(n+1))
    result = np.around(arr30,n)
    return result*flag
     
#极坐标雷达的求经纬度
def antenna_to_geographic( lon_0, lat_0,h,ranges, azimuths, elevations):
    '''
    计算雷达库的经纬度
    :param lon_0: 雷达经度
    :param lat_0: 雷达纬度
    :param h: 雷达海拔高度
    :param ranges: 径距
    :param azimuths: 雷达库方位角
    :param elevations: 雷达库方位角仰角
    :return: 经纬度
    '''
    import warnings
    theta_e = np.deg2rad(elevations)  # elevation angle in radians.
    theta_a = np.deg2rad(azimuths)  # azimuth angle in radians.
    R = 6370997.0  * 4.0 / 3.0  # effective radius of earth in meters.
    r = ranges * 1000  # distances to gates in meters.
    R0 = 6370997.#radius of earth

    # z = (r ** 2 + R ** 2 + 2.0 * r * R * np.sin(theta_e)) ** 0.5 - R #位于0海拔高度
    z = ((r * np.cos(theta_e)) ** 2 + (R + h + r * np.sin(theta_e)) ** 2) ** 0.5 - R
    s = R * np.arcsin(r * np.cos(theta_e) / (R + z))  # arc length in m.
    x = s * np.sin(theta_a)
    y = s * np.cos(theta_a)

    x = np.atleast_1d(np.asarray(x))
    y = np.atleast_1d(np.asarray(y))

    lat_0_rad = np.deg2rad(lat_0)
    lon_0_rad = np.deg2rad(lon_0)

    rho = np.sqrt(x*x + y*y)
    c = rho / R0

    with warnings.catch_warnings():
        # division by zero may occur here but is properly addressed below so
        # the warnings can be ignored
        warnings.simplefilter("ignore", RuntimeWarning)
        lat_rad = np.arcsin(np.cos(c) * np.sin(lat_0_rad) +
                            y * np.sin(c) * np.cos(lat_0_rad) / rho)
    lat_deg = np.rad2deg(lat_rad)
    # fix cases where the distance from the center of the projection is zero
    lat_deg[rho == 0] = lat_0

    x1 = x * np.sin(c)
    x2 = rho*np.cos(lat_0_rad)*np.cos(c) - y*np.sin(lat_0_rad)*np.sin(c)
    lon_rad = lon_0_rad + np.arctan2(x1, x2)
    lon_deg = np.rad2deg(lon_rad)
    # Longitudes should be from -180 to 180 degrees
    lon_deg[lon_deg > 180] -= 360.
    lon_deg[lon_deg < -180] += 360.
    return lon_deg, lat_deg
