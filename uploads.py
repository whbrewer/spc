import zipfile
import os

class uploader(object):

    def __init__(self):
        pass

    def unzip(self,save_path):
        (path,fn) = save_path.split('/')
        # unzip file
        fh = open(save_path, 'rb')
        z = zipfile.ZipFile(fh)
        z.extractall(path)
        fh.close()

    def create_infrastructure(self):
        pass

