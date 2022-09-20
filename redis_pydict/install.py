"""
Written by Phani Pavan k <kphanipavan@gmail.com>.
use this code as per gplv3 guidelines.
"""
import pgrep
import re
import shutil
import os
import tarfile
import subprocess as sp
from tqdm.auto import tqdm
import requests as req
from .ui import *
import sys
from threading import Thread
from multiprocessing import Process
import asyncio
import time
REDIS_STABLE_URL = "http://download.redis.io/redis-stable.tar.gz"


class RedisServer:
    def __init__(self) -> None:
        self.proc = None
        self.procID = None

    @staticmethod
    def _makeLogFolder():
        os.makedirs('redis_server/installLogs', exist_ok=True)
        # ? Implement saving logs to this folder.

    @staticmethod
    def _downloadRedis():
        os.makedirs('redis_server', exist_ok=True)
        lst = os.listdir('./redis_server')
        if 'redis-stable.tar.gz' in lst:
            debug('Redis Source already found, skipping download', Log.WRN)
        else:
            debug('Downloading Redis Stable Source')
            with req.get(REDIS_STABLE_URL, stream=True) as r:
                size = int(r.headers.get('Content-Length'))
                with tqdm.wrapattr(r.raw, 'read', total=size, desc='') as data:
                    with open('redis_server/redis-stable.tar.gz', 'wb') as fil:
                        shutil.copyfileobj(data, fil)
            debug('Download Done', Log.SUC)

    @staticmethod
    def _findSource():
        lst = os.listdir('./redis_server')
        if 'redis-stable' in lst:
            debug('Redis Already Extracted', Log.WRN)
        else:
            debug('Extracting Source')
            tarfile.open(
                'redis_server/redis-stable.tar.gz').extractall('./redis_server/')
            debug('Done Extracting Source', Log.SUC)

    @staticmethod
    def _build():
        if 'src' in os.listdir('redis_server/redis-stable') and 'redis-server' in os.listdir('./redis_server/redis-stable/src'):
            # os.chdir('redis_server/redis-stable')
            debug('Redis Already Built', Log.WRN)
        else:
            debug('Running Redis Build On ' +
                  str((os.cpu_count()//3)+1 if type(os.cpu_count()) is int else 1)+' Cores')
            anim = Loader(desc='Building ').start()
            os.chdir('redis_server/redis-stable')
            x = sp.run(['make -j'+str((os.cpu_count()//3)+1 if type(os.cpu_count()) is int else 1)],
                       capture_output=True, text=True, shell=True)
            anim.stop()
            os.chdir('../../')
            debug('Done Building', Log.SUC)

    @staticmethod
    def _setupLink():
        if 'redis-server' in os.listdir('./redis_server'):
            debug('Redis Already setup', Log.WRN)
        else:
            debug('Setting up Redis Server')
            y = sp.run(['chmod +x ./redis_server/redis-stable/src/redis-server'],
                       shell=True, text=True, capture_output=True)
            # sp.run(['ls'])
            y = sp.run(['ln -s ./redis-stable/src/redis-server ./redis_server/redis-server'],
                       shell=True, text=True, capture_output=True)
            y = sp.run(['chmod +x ./redis_server/redis-server'],
                       shell=True, text=True, capture_output=True)
            debug('Redis Set', Log.SUC)

    @staticmethod
    def _verify():
        debug('Veryfying Redis Install')
        # sp.run(['ls', '-l'])
        # sp.run(['pwd'])
        z = sp.run(['./redis_server/redis-server --version'],
                   shell=True, capture_output=True, text=True)
        regexp = re.search('Redis server v=(.*) sha', z.stdout)
        if regexp.group(0):
            debug('Redis Version '+regexp.group(1)+' Found')
            debug('Redis working fine', Log.SUC)
            return 1
        else:
            return 0

    def install(self, saveLogs: bool = False, ):
        if sys.platform.lower() != 'linux':
            debug('OS not Linux, install redis manually', Log.ERR)
            debug(
                'Support for intalling on other OSs will be implemented in the future.', Log.WRN)
            return
        if saveLogs:
            RedisServer._makeLogFolder()
        RedisServer._downloadRedis()
        RedisServer._findSource()
        RedisServer._build()
        RedisServer._setupLink()
        return RedisServer._verify()

    async def _startServer(self, threading: bool = False):
        def runServer():
            sp.run('./redis_server/redis-server',
                   capture_output=True, text=True, shell=False)

        if threading:
            self.proc = Thread(target=runServer)
        else:
            self.proc = Process(target=runServer)
        self.proc.start()
        self.procID = pgrep.pgrep(
            r"-f 'redis_server\/redis-server \*\:6379'")[0]

    def startServer(self):
        if self.proc is None:
            asyncio.run(self._startServer())
        else:
            debug('Redis Server already running manually', Log.WRN)

    def stopServer(self):
        if self.proc is None:
            debug('Redis Server not running', Log.WRN)
        else:
            # self.proc.kill()
            os.kill(self.procID, 15)
            debug('Redis Server stopped', Log.SUC)
            anim = Loader(desc='Stopping Redis Server ').start()
            while self.proc.is_alive():
                pass
            anim.stop()
            print('\n')
            self.proc = None
            self.procID = None


if __name__ == "__main__":
    a = RedisServer()
    a.install()
    a.startServer()
    print(a.procID)
    time.sleep(5)
    a.stopServer()
