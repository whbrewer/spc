import zipfile
import config
import os, stat

class uploader(object):

    def zip(self,save_path):
        (path,fn) = save_path.split('/')
        # this should be like filename.zip
        fh = open(save_path, 'wb')
        z = zipfile.ZipFile(fh)
        z.extractall(path)
        fh.close()

    def unzip(self,save_path):
        (path,fn) = save_path.split('/')
        # unzip file
        fh = open(save_path, 'rb')
        z = zipfile.ZipFile(fh)
        z.extractall(path)
        fh.close()

    def verify(self,save_path_dir,appname):
        exe_file = os.path.join(save_path_dir,appname)
        in_file  = exe_file + '.in'
        msg = 'File uploaded OK\n'
        # verify that .in file exists
        #if not os.path.exists(in_file):
        #    msg += "\nERROR: .in file does not exist"
        # verify that binary file exists
        if os.path.exists(exe_file):
            # set permissions to read and execute for all
            os.chmod(exe_file, 0755)
            # set permissions to read by owner 
            #os.chmod(exe_file, stat.S_IREAD)
            # set permissions to execute by owner
            #os.chmod(exe_file, stat.S_IEXEC)
        else:
            msg += "\nERROR: executable missing"
        return msg 
