from tools import useragent
from tools import colorprint
import requests
import re
import threading
from tqdm import tqdm
results = []
def search_duckduckgo(query,visual):
    try:
        global results
        user_agent = {'User-agent': useragent.get_useragent()}
        response = requests.get(f"https://html.duckduckgo.com/html/?q={query}",headers=user_agent,timeout=10)
        urls = re.findall(r'<a class="result__url" href="(.+?)">', response.text)
        for i in range(len(urls)):
            if urls[i].startswith('//duckduckgo.com/l/?uddg='):
                real_url = re.search(r'uddg=(.+?)&', urls[i]).group(1)
                urls[i] = real_url
        results += urls
    except:
        pass
    visual.update(1)

def search_ask(query,visual):
    global results
    search_duckduckgo(query,visual)
    for i in range(1,20):
        try:
            user_agent = {'User-agent': useragent.get_useragent()}
            response = requests.get(f"https://www.ask.com/web?q={query}&{i}",headers=user_agent)
            urls = re.findall(r"target=\"_blank\" href='(.*?)' data-unified=", response.text)
            results += urls
        except:
            pass
        visual.update(1)

def SearchMain(dork,thread):
    threads = []
    ttl = len(dork)
    visual = tqdm(total=ttl*20,desc=f' Scanning Dorks')
    lines = open(dork, "r").read().splitlines()
    i = 0
    while(i < len(lines)):
        for j in range(i,min(i+thread,len(lines))):
            try:
                t = threading.Thread(target=search_ask,args=(lines[j],visual))
                threads.append(t)
                t.start()
            except:
                pass
        for t in threads:
            t.join()
        i += thread
        threads = []
    return results
