def _prepare_for_read(filename):
    import gzip
    import bz2
    """
    Return a file like object read for reading.
    Open a file for reading in binary mode with transparent decompression of
    Gzip and BZip2 files.  The resulting file-like object should be closed.
    Parameters
    ----------
    filename : str or file-like object
        Filename or file-like object which will be opened.  File-like objects
        will not be examined for compressed data.
    Returns
    -------
    file_like : file-like object
        File like object from which data can be read.
    """
    # if a file-like object was provided, return
    if hasattr(filename, 'read'):  # file-like object
        return filename
    # look for compressed data by examining the first few bytes
    fh = open(filename, 'rb')
    magic = fh.read(3)
    fh.close()
    if magic.startswith(b'\x1f\x8b'):
        f = gzip.GzipFile(filename, 'rb')
    elif magic.startswith(b'BZh'):
        f = bz2.BZ2File(filename, 'rb')
    else:
        f = open(filename, 'rb')
    return f
def Header_file(filename):
    import numpy as np
    import struct
    import gzip
    import pprint
    fid = _prepare_for_read(filename)

    # 通用头块32
    Magic_number, = struct.unpack('i', fid.read(4))
    Major_Ver, = struct.unpack('H', fid.read(2))
    Minor_Ver, = struct.unpack('H', fid.read(2))
    Generic_Type, = struct.unpack('i', fid.read(4))
    Product_type, = struct.unpack('i', fid.read(4))
    fid.read(16)
    FILE_HEADER = {}
    fh = {'Magic_number': Magic_number, 'Major_Ver': Major_Ver,
          'Minor_Ver': Minor_Ver, 'Generic_Type': Generic_Type, 'Product_type': Product_type}
    FILE_HEADER.update(fh)

    # 站点配置128
    Site_code, = struct.unpack('8s', fid.read(8))
    Site_name, = struct.unpack('32s', fid.read(32))
    Latitude, = struct.unpack('f', fid.read(4))
    Longitude, = struct.unpack('f', fid.read(4))
    # print(Latitude,Longitude)
    Antenna_Height, = struct.unpack('i', fid.read(4))
    Ground_height, = struct.unpack('i', fid.read(4))
    Frequency, = struct.unpack('f', fid.read(4))
    Beam_w_h, = struct.unpack('f', fid.read(4))
    Beam_w_w, = struct.unpack('f', fid.read(4))
    RDA_Ver, = struct.unpack('i', fid.read(4))
    Radar_type, = struct.unpack('h', fid.read(2))
    # print(Radar_type)
    Antenna_gain, = struct.unpack('h', fid.read(2))
    Trans_fl, = struct.unpack('h', fid.read(2))
    Trans_rl, = struct.unpack('h', fid.read(2))
    Other_l, = struct.unpack('h', fid.read(2))
    fid.read(46)
    SITE_CONFIG = {'Site_code': Site_code, 'Site_name': Site_name,
                   'Latitude': Latitude, 'Longitude': Longitude,
                   'Antenna_Height': Antenna_Height, 'Ground_height': Ground_height,
                   'Frequency': Frequency, 'Beam_w_h': Beam_w_h,
                   'Beam_w_w': Beam_w_w, 'RDA_Ver': RDA_Ver,
                   'Radar_type': Radar_type, 'Antenna_gain': Antenna_gain,
                   'Trans_fl': Trans_fl, 'Trans_rl': Trans_rl,
                   'Other_l': Other_l}
    # 任务配置256
    Task_name, = struct.unpack('32s', fid.read(32))
    Task_descp, = struct.unpack('128s', fid.read(128))
    # print(Task_name)
    Polar_type, = struct.unpack('i', fid.read(4))
    Scan_type, = struct.unpack('i', fid.read(4))
    Pause_width, = struct.unpack('i', fid.read(4))
    Scan_start_time, = struct.unpack('i', fid.read(4))
    Cut_number, = struct.unpack('i', fid.read(4))
    Hori_noise, = struct.unpack('f', fid.read(4))
    Vert_noise, = struct.unpack('f', fid.read(4))
    Hori_calib, = struct.unpack('f', fid.read(4))
    Vert_calib, = struct.unpack('f', fid.read(4))
    Hori_noise_temp, = struct.unpack('f', fid.read(4))
    Vert_noise_temp, = struct.unpack('f', fid.read(4))
    ZDR_calib, = struct.unpack('f', fid.read(4))
    PHIDP_calib, = struct.unpack('f', fid.read(4))
    LDR_calib, = struct.unpack('f', fid.read(4))
    fid.read(40)
    TASK_CONFIG = {'Task_name': Task_name, 'Task_descp': Task_descp,
                   'Polar_type': Polar_type, 'Scan_type': Scan_type,
                   'Pause_width': Pause_width, 'Scan_start_time': Scan_start_time,
                   'Cut_number': Cut_number, 'Hori_noise': Hori_noise,
                   'Vert_noise': Vert_noise, 'Hori_calib': Hori_calib,
                   'Vert_calib': Vert_calib, 'Hori_noise_temp': Hori_noise_temp,
                   'Vert_noise_temp': Vert_noise_temp, 'ZDR_calib': ZDR_calib,
                   'PHIDP_calib': PHIDP_calib, 'LDR_calib': LDR_calib}
    fid.close()
    return FILE_HEADER,SITE_CONFIG,TASK_CONFIG
