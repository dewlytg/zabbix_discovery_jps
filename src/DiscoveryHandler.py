from utils import handler
import traceback,os

_local_ip = handler.getIpAddr()

def getProcessList():
    discovery_key = "".join(["jd.cutt.process.",_local_ip])
    r = cacheHandler()
    if r.get(discovery_key):
        print(r.get(discovery_key))
    else:
        # command_output = subprocess.check_output(["su","-","hadoop","-c","jps"])
        command_output = os.popen("sudo -u hadoop jps |grep -v Jps") # please add 'zabbix ALL = (hadoop) NOPASSWD: ALL'  to visudo
        formated_data = handler.schemaZabbixData(command_output,"{#PROCESS}")
        r.set(discovery_key,formated_data)
        print(formated_data)

def getPortList():
    pass


def purgeProcessList():
    try:
        discovery_key = "".join(["jd.cutt.process.", _local_ip])
        r = cacheHandler()
        r.delete(discovery_key)
    except Exception as e:
        traceback.print_exc()
        exit()

def cacheHandler():
    config = handler.getConfigInfo("./config/cutt.cfg")
    cache_info_list = config.items("cacheserver")
    cache_info_dict = handler.list2dict(cache_info_list)
    cache_connection = handler.formatStr2Int(cache_info_dict)
    r = handler.cache(**cache_connection)
    return r

