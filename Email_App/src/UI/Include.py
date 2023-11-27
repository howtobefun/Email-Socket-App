import sys
import os 

UI_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT = UI_PATH + "/../../"
os.chdir(ROOT)
sys.path.append('src/client')
sys.path.append('src/UI')
 