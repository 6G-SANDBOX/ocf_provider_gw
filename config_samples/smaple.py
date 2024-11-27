import sys
sys.path.append("/Users/IDB0128/git_repos/pesp_aef_gw/")
from aef_gw.aef_gw import aef_gw 

if __name__ == "__main__":
    aef = aef_gw("./northbound.yaml", "./southbound.yaml", True)
    aef.remove()