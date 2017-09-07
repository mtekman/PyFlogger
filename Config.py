#/usr/bin/env python3

from xdg.BaseDirectory import xdg_config_home
from os.path import join as pjoin, exists, sep


__config_dir = pjoin( xdg_config_home, 'foodlogger')

_Config__paths = {
    'foodlist'  : [ pjoin( __config_dir, 'list.txt' ) , False],  # [ path, has_been_resolved]
    'foodlog'   : [ pjoin( __config_dir, 'log.txt'  ) , False],
    'weightlog' : [ pjoin( __config_dir, 'weight.txt'), False]
}

user_foodlist = ""
user_foodlog  = ""
user_weightlog= ""


class Config:


    @staticmethod
    def resolveAllPaths(): # called from main
        user_foodlist = Config.__resolvePath('foodlist')
        user_foodlog  = Config.__resolvePath('foodlog')
        user_weightlog= Config.__resolvePath('weightlog')


    @staticmethod
    def __resolvePath(key):
        filepath = __paths[key][0]

        if not __paths[key][1]:
            Config.__touch(filepath)
            __paths[key][1] = True

        # already resolved
        return filepath


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
