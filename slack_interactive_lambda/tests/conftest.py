import sys
from os.path import abspath
from os.path import dirname as d
from os.path import join

root_dir = join(d(d(d(abspath(__file__)))), "slack-interactive-lambda")
sys.path.append(root_dir)
