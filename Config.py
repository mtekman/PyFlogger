#/usr/bin/env python3

from xdg.BaseDirectory import xdg_config_home
from os.path import join as pjoin, exists, sep


__config_dir = pjoin( xdg_config_home, 'foodlogger')

user_foodlist = pjoin( __config_dir, 'list.txt'  )
user_foodlog  = pjoin( __config_dir, 'log.txt'   )
user_weightlog= pjoin( __config_dir, 'weight.txt')


class Config:


    @staticmethod
    def resolveAllPaths(): # called from main
        Config.resolvePath(user_foodlist)
        Config.resolvePath(user_foodlog)
        Config.resolvePath(user_weightlog)


    @staticmethod
    def resolvePath(filepath):
        Config.__touch(filepath)


    @staticmethod
    def __touch(filename):
        if not exists(filename):

            print("[INFO]", filename, "does not exist -- creating new")

            direc = sep.join(filename.split(sep)[:-1])
            if not exists(direc):
                mkdir( direc )

            # Open file and write blank
            with open(filename,'w') as f:
                f.write("\n")
                f.close()

        return filename
