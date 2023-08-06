import logging
import os

import bbcloud_python_sdk as utils

from .OssFileCache import OssFileCache

from .SynologyFileCache import SynologyFileCache


class FileCache():
    def __init__(self, available_area, using_area):
        self.namespace = ''
        self.using_area = using_area
        self.available_area = available_area

    def getDefaultEngine(self, using_area=None):
        if not using_area:
            using_area = self.using_area
        engine = self.available_area[using_area]['engine']
        config = self.available_area[using_area]['config']
        if engine == 'OssFileCache':
            return OssFileCache(access_key_id=config['access_key_id'],
                                access_key_secret=config['access_key_secret'],
                                endpoint=config['endpoint'],
                                bucket_name=config['bucket_name'],
                                cache_path_root=config['cache_path_root'])
        elif engine == 'SynologyFileCache':
            return SynologyFileCache(
                ip_address=config['ip_address'],
                port=config['port'],
                username=config['username'],
                password=config['password'],
                cache_path_root=config['cache_path_root'])

    def set_namespace(self, namespace):
        self.namespace = namespace
        return self

    def set(self, key, file_path, del_local=True, set_all_area=False):
        if set_all_area:
            logging.info('setting all area file cache')
            for area in self.available_area:
                logging.info('setting file cache to %s' % area)
                self.getDefaultEngine(using_area=area).set_namespace(namespace=self.namespace).set(key=key,
                                                                                                   file_path=file_path,
                                                                                                   del_local=del_local)
        else:
            logging.info('setting file cache')
            return self.getDefaultEngine().set_namespace(namespace=self.namespace).set(key=key, file_path=file_path,
                                                                                       del_local=del_local)

    def get(self, key, local_file, default=None, auto_unzip=False, auto_delete_local_zip=True, auto_untar=False,
            auto_delete_local_tar=True):

        if not os.path.exists(os.path.dirname(local_file)):
            utils.make_dir(os.path.dirname(local_file))

        is_get = self.getDefaultEngine().set_namespace(namespace=self.namespace).get(key=key, local_file=local_file)
        if not is_get:
            if default:
                logging.info('set default file cache')
                self.set(key=key, file_path=default, del_local=True)
                is_get = self.get(key=key, local_file=local_file)
            else:
                logging.info('missing file cache and not set default')
                return False

        if is_get:
            logging.info('get file cache')
            if os.path.splitext(local_file)[-1] == '.zip' and auto_unzip:
                unzip_dir = os.path.dirname(local_file)
                if os.path.exists(local_file):
                    logging.info('auto unzip from %s to %s' % (local_file, unzip_dir))
                    utils.unzip(file_name=local_file, dst_dir=unzip_dir)
                    if auto_delete_local_zip:
                        logging.info('auto delete zip')
                        os.remove(local_file)
            elif os.path.splitext(local_file)[-1] == '.gz' and auto_untar:
                untar_dir = os.path.dirname(local_file)
                if os.path.exists(local_file):
                    logging.info('auto untar from %s to %s' % (local_file, untar_dir))
                    utils.untar(file_name=local_file, dst_dir=untar_dir)
                    if auto_delete_local_tar:
                        logging.info('auto delete tar')
                        os.remove(local_file)
            return True
        else:
            logging.info('missing file cache')
            return False

    def delete(self, key, delete_all_area=False):
        if delete_all_area:
            logging.info('deleting all area file cache')
            for area in self.available_area:
                self.getDefaultEngine(using_area=area).set_namespace(namespace=self.namespace).delete(key=key)
        else:
            logging.info('deleting file cache')
            return self.getDefaultEngine().set_namespace(namespace=self.namespace).delete(key=key)
