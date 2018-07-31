import redis,configparser
import traceback
import socket,struct,fcntl
import json,os,collections

def cache(*args,**kwargs):
    r = redis.Redis(**kwargs)
    return r

def formatStr2Int(obj):
    if isinstance(obj,dict) and obj.get("port"):
        try:
            obj["port"] = int(obj.get("port"))
        except Exception as e:
            traceback.print_exc()
        finally:
            return obj

def getConfigInfo(configfile):
    config = configparser.ConfigParser()
    config.read(configfile)
    return config

def list2dict(listobj,dictobj={}):
    if isinstance(listobj,list):
        for i in listobj:
            try:
                key,value = i
                dictobj[key] = value
            except Exception as e:
                traceback.print_exc()
        else:
            return dictobj

def getIpAddr():
    ifname = getSystemEth()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def schemaZabbixData(dataobj,itemName,data=[],ret={}):
    if isinstance(dataobj,collections.Iterable):
        for line in dataobj:
            pid,pname = line.split()
            data.append({itemName:pname.strip()})
        ret["data"] = data
        return json.dumps(ret,sort_keys=True, indent=4)
    else:
        exit()

def getSystemEth():
    networkdir = "/sys/class/net"
    interface_list = os.listdir(networkdir)
    for i in interface_list:
        if i.startswith("eth"):
            return i
    else:
        print("have not interface which named eth staring on this machine!")
        exit()