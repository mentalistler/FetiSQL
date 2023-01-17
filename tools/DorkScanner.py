from tools import useragent
from tools import colorprint
import requests
import re
import threading
from tqdm import tqdm
results = []

def search_ask(query,visual):
    global results
    for i in range(1,20):
        try:
            user_agent = {'User-agent': useragent.get_useragent()}
            response = requests.get(f"https://www.ask.com/web?q={query}&{i}",headers=user_agent)
            urls = re.findall(r"target=\"_blank\" href='(.*?)' data-unified=", response.text)
            results += urls
        except:
            pass
        visual.update(1)
        
def search_searchencrypt(query,visual):
    global results
    try:
        for j in range(1,20):
            user_agent = {'User-agent': useragent.get_useragent()}
            response = requests.get(f"https://spapi.searchencrypt.com/api/search?q={query}&types=web&page={j}&limit=20",headers=user_agent)
            res = response.json()["Results"]
            for i in range(len(res)):
                results.append(res[i]["ClickUrl"])
    except:
        pass
    visual.update(1)
def search_neeva(query,visual):
    global results
    for i in range(1,20):
        try:
            user_agent = {'User-agent': useragent.get_useragent()}
            response = requests.get(f"https://neeva.com/search?q={query}&c=All&src=Pagination&page={i}",headers=user_agent)
            urls = re.findall(r'<a[^>]+href="(https?:\/\/[^"]+)"', response.text)
            results += urls
        except:
            pass
        visual.update(1)
def SearchMain(dork,thread,engine):
    threads = []
    ttl = len(dork)
    visual = tqdm(total=ttl*19,desc=f' Scanning Dorks')
    lines = open(dork, "r").read().splitlines()
    i = 0
    while(i < len(lines)):
        for j in range(i,min(i+thread,len(lines))):
            try:
                if(engine=="neeva"):
                    t = threading.Thread(target=search_neeva,args=(lines[j],visual))
                elif(engine=="ask"):
                    t = threading.Thread(target=search_ask,args=(lines[j],visual))
                elif(engine=="searchencrypt"):
                    t = threading.Thread(target=search_searchencrypt,args=(lines[j],visual))
                else:
                    colorprint.colorprint("Engine Error","v")
                    exit()
                threads.append(t)
                t.start()
            except:
                pass
        for t in threads:
            t.join()
        i += thread
        threads = []
    return results
