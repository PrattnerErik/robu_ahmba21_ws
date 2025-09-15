import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/robu/work/ROBU/robu_ahmba21_ws/install/obstacle_avoidence'
