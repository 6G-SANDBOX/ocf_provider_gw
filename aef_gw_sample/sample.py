import sys
sys.path.append("/Users/IDB0128/git_repos/pesp_aef_gw/")
from aef_gw.aef_gw import aef_gw 

if __name__ == "__main__":
    gw = aef_gw("../config_samples/northbound.yaml", "../config_samples/southbound.yaml")