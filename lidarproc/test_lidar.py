
import time

import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))

from lidarproc.main.data_retrieval import LidarThread

t = LidarThread('', "127.0.0.1")
t.start()

while True:

    print(t.get_measures())
    time.sleep(1)
