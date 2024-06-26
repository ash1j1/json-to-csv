#!/usr/bin/python3

import os
import time
import paramiko
#import configparser

#config = configparser.ConfigParser()
#config.read('config.ini')

local_dir = ''
remote_dir = ''
sftp_host = ''
sftp_port = 
sftp_user = ''
sftp_password = ''
#private_key_path =
def connect_to_sftp():
    #Creates an RSAKey object which gets loaded with the private key
    #private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
    transport = paramiko.Transport((sftp_host, sftp_port))
    transport.connect(username=sftp_user, password=sftp_password) #pkey=private_key
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp

def monitor_directory():
    sftp = connect_to_sftp()
    
    while True:
        with os.scandir(local_dir) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith('.csv'):
                    local_file_path = os.path.join(local_dir, entry.name)
                    remote_file_path = os.path.join(remote_dir, entry.name)
                
                if entry.name not in sftp.listdir(remote_dir):
                    print(f'Uploading {entry.name} to {remote_dir}')
                    sftp.put(local_file_path, remote_file_path)
                    print(f'{entry.name} uploaded successfully')
        
        time.sleep(20) 

if __name__ == "__main__":
    monitor_directory()
