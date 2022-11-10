def read_scaninfo(file):
    import struct
    from xradarheader import Header_file,_prepare_for_read
    fid = _prepare_for_read(file)
    file_header, site_config, task_config = Header_file(file)
    cut_num = task_config['Cut_number']  # 扫描层数
    fid.seek(416)
    # 扫描配置
    Angle_clutter = []  # 角度数据块
    Resolution = []  #分辨率数组(库长...)
    SIGN_threshold = [] #信号门限
    MOMENT_mask = [] #测量数据的种类及大小
    VAL_mask = []#各测量掩码
    for i in range(cut_num):
        Process_mode, = struct.unpack('i', fid.read(4))
        Wave_form, = struct.unpack('i', fid.read(4))
        PRF_1, = struct.unpack('f', fid.read(4))
        PRF_2, = struct.unpack('f', fid.read(4))
        Dealiasing_mode, = struct.unpack('i', fid.read(4))
        Azimuth, = struct.unpack('f', fid.read(4))
        Elevation, = struct.unpack('f', fid.read(4))
        Start_angle, = struct.unpack('f', fid.read(4))
        End_angle, = struct.unpack('f', fid.read(4))
        Angular_resolution, = struct.unpack('f', fid.read(4))
        Scan_speed, = struct.unpack('f', fid.read(4))
        Log_resolution, = struct.unpack('i', fid.read(4))  # 强度数据的距离分辨率
        Doppler_resolution, = struct.unpack('i', fid.read(4))
        Maximum_range1, = struct.unpack('i', fid.read(4))
        Maximum_range2, = struct.unpack('i', fid.read(4))
        Start_range, = struct.unpack('i', fid.read(4))
        Sample_1, = struct.unpack('i', fid.read(4))
        Sample_2, = struct.unpack('i', fid.read(4))
        Phase_mode, = struct.unpack('i', fid.read(4))
        Atmosphereric_loss, = struct.unpack('f', fid.read(4))
        Nyquist_speed, = struct.unpack('f', fid.read(4))
        Moments_mask, = struct.unpack('q', fid.read(8))
        Moments_size_mask, = struct.unpack('q', fid.read(8))
        Misc_filter_mask, = struct.unpack('i', fid.read(4))
        SQI_threshold, = struct.unpack('f', fid.read(4))
        SIG_threshold, = struct.unpack('f', fid.read(4))
        CSR_threshold, = struct.unpack('f', fid.read(4))
        LOG_threshold, = struct.unpack('f', fid.read(4))
        CPA_threshold, = struct.unpack('f', fid.read(4))
        PMI_threshold, = struct.unpack('f', fid.read(4))
        DPLOG_threshold, = struct.unpack('f', fid.read(4))
        fid.read(4)
        dBT_mask, = struct.unpack('i', fid.read(4))
        dBZ_mask, = struct.unpack('i', fid.read(4))
        Velocity_mask, = struct.unpack('i', fid.read(4))
        Spectrum_width_mask, = struct.unpack('i', fid.read(4))
        DP_mask, = struct.unpack('i', fid.read(4))
        fid.read(16)
        Direction, = struct.unpack('i', fid.read(4))
        Ground_clutter_classifier_type, = struct.unpack('h', fid.read(2))
        Ground_clutter_filter_type, = struct.unpack('h', fid.read(2))
        Ground_clutter_filter_NW, = struct.unpack('h', fid.read(2))
        Ground_clutter_filter_window, = struct.unpack('h', fid.read(2))
        fid.read(72)

        angle_clutter = [Azimuth, Elevation, Start_angle, End_angle, Angular_resolution, Scan_speed]
        Angle_clutter.append(angle_clutter)
        resolution = [Log_resolution, Doppler_resolution,
                      Maximum_range1, Maximum_range2, Start_range]
        Resolution.append(resolution)
        sign_threshold = [SQI_threshold,SIG_threshold,CSR_threshold,
                         LOG_threshold,CPA_threshold,PMI_threshold,DPLOG_threshold]
        SIGN_threshold.append(sign_threshold)
        val_moment = [Moments_mask,Moments_size_mask]
        MOMENT_mask.append(val_moment)
        val_mask = [dBT_mask,dBZ_mask,Velocity_mask,Spectrum_width_mask,DP_mask]
        VAL_mask.append(val_mask)
    SCANINFO = {'Angle_clutter':Angle_clutter,'Resolution':Resolution,
                'SIGN_threshold':SIGN_threshold,'MOMENT_mask':MOMENT_mask,
                'VAL_mask':VAL_mask}
    fid.close()
    return SCANINFO
