#utf-8
#file compress and extract 
'''
本程序实现文件批量压缩和解压缩(zip格式)
本程序经过测试，压缩的源文件目录与压缩的目标目录不能在同一个目录下，否则会陷入死循环

'''
import gzip
import os
import shutil
import zipfile
def mkdir(dirpath):
    '''
    创建文件夹
    :param path:
    :return:
    '''
    folder = os.path.exists(dirpath)
    if not folder:
        os.makedirs(dirpath)
    else:
        pass
def del_dir(rootdir):
    filelist = os.listdir(rootdir)
    for f in filelist:
        filepath = os.path.join(rootdir,f)
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath,True)
    shutil.rmtree(rootdir,True)

def zipDir(dirpath,outFullName):
    zip_ = zipfile.ZipFile(outFullName,'w',zipfile.ZIP_DEFLATED)
    for path,dirnames,filenames in os.walk(dirpath):
        fpath = path.replace(dirpath,'')
        for filename in filenames:
            zip_.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip_.close()


def unzip_folder(source_file,destinate_dir):
    mkdir(destinate_dir)
    with zipfile.ZipFile(source_file,'r') as zipobj:
        zipobj.extractall(destinate_dir)
    # print('done')
