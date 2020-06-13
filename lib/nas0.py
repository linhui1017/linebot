# -*- coding:utf-8 -*-
#ftp.py
#    wklken@yeah.net
#this script is used to do some operations more convenient via ftp
  #1.[p]upload many files in the same time,show md5s
  #2.[g]download many files in the same time,show md5s
  #3.[l]list all the files on ftp site
  #4.[f]search a file on ftp site,return True or Flase
  #5.[h]show help info

#add upload and download operations  20111210 version0.1
#add md5sum after ops 20120308 version0.2

import sys,os,ftplib,socket
from lib.utils import logger 
from lib.AESCipher import AESCipher 
from settings import Config 
import io


NIS_TEMP_PATH = Config.NAS0_TEMP_PATH
__const_host = Config.NAS0_IP
__const_username = AESCipher(Config.SYS_AES_KEY).decrypt(Config.NAS0_USER_ID)
__const_pwd = AESCipher(Config.SYS_AES_KEY).decrypt(Config.NAS0_PASSWOED)
__const_buffer_size = 8192



def connect():
    try:
        ftp = ftplib.FTP(__const_host)
        ftp.login(__const_username,__const_pwd)
        return ftp
    except Exception as e:
        logger.error(str(e))
        raise Exception("FTP is unavailable,please check the host,username and password!")

def disconnect(ftp):
    ftp.quit()

def upload(ftp, filepath):
    f = open(filepath, "rb")
    file_name = os.path.split(filepath)[-1]
    try:
        ftp.storbinary('STOR %s'%file_name, f, __const_buffer_size)
    except ftplib.error_perm as e:
        raise e
    return True

def uploadStream(ftp, filepath, filename, stream):
    try:
        ftp.cwd(filepath)  
        stream.seek(0)
        ftp.storbinary('STOR %s'%filename, stream, __const_buffer_size)
    except ftplib.error_perm as e:
        raise e
    return True

def downloadStream(ftp, filepath, filename):
    try:
        ftp.cwd(filepath) 
        stream=io.BytesIO()
        ftp.retrbinary ('RETR %s'%filename, stream.write)   
        stream.seek(0)
        return stream
    except ftplib.error_perm as e:
        raise e
    return True

def download(ftp, filename):
    f = open(filename,"wb").write
    try:
        ftp.retrbinary("RETR %s"%filename, f, __const_buffer_size)
    except ftplib.error_perm as e:
        raise e
    return True

def list(ftp):
    ftp.dir()

def find(ftp,filename):
    ftp_f_list = ftp.nlst()
    if filename in ftp_f_list:
        return True
    else:
        return False

def help():
    print("help info:")
    print("[./ftp.py l]\t show the file list of the ftp site ")
    print("[./ftp.py f filenamA filenameB]\t check if the file is in the ftp site")
    print("[./ftp.py p filenameA filenameB]\t upload file into ftp site")
    print("[./ftp.py g filenameA filenameB]\t get file from ftp site")
    print("[./ftp.py h]\t show help info")
    print("other params are invalid")