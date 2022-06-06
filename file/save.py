import hashlib
import logging
import os
import datetime
from typing import Tuple

class FileManager:
    def __init__(self, base_dir: str) -> None:
        self.base_dir = base_dir
        self.logger = logging.getLogger(__name__)

    def save_file(self, b: bytes) -> Tuple[str, str, str]:
        hash_str = hashlib.md5(b).hexdigest()
        topdir, subdir = hash_str[:8], hash_str[8:]
        dir = os.path.join(self.base_dir, topdir, subdir)

        if not os.path.exists(dir):
            self.logger.info(f"creating {dir=}")
            os.makedirs(dir)

        filename = datetime.datetime.now().strftime("%Y%m%d-%H-%M-%S.%f")
        fullpath = os.path.join(self.base_dir, topdir, subdir, filename)
        url = "/".join([topdir, subdir, filename])
        
        self.logger.info(f"saving to {url=}, {fullpath=}")
        
        with open(fullpath, 'wb') as f:
            f.write(b)

        return fullpath, hash_str, url
        
    def delete_file(self, url: str) -> bool:
        fullpath = os.path.join(self.base_dir, *url.split('/'))
        
        if not os.path.exists(fullpath):
            return False

        self.logger.info(f"deleting {fullpath=}")
        os.remove(fullpath)

        return True

    def read_file(self, url: str) -> bytes:
        fullpath = os.path.join(self.base_dir, *url.split('/'))
        
        if not os.path.exists(fullpath):
            return b''

        self.logger.info(f"reading {fullpath=}")
        
        with open(fullpath, 'rb') as f:
            return f.read()





