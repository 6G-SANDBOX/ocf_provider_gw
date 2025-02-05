import sys
sys.path.append("/Users/IDB0128/git_repos/pesp_aef_gw/")
from provider_gw.provider_gw import provider_gw 

if __name__ == "__main__":
    provider = provider_gw("./northbound.yaml", "./southbound.yaml", True)
    provider.start()