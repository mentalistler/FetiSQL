import re
import requests
from urllib.parse import urlparse, urlsplit, urlunsplit
from tools import useragent
from tools import colorprint
import threading
vulnerable = []
class vulndetector:
    def __init__(self):
        self.MySQL = ["SQL syntax.*MySQL", "Warning.*mysql_.*", "valid MySQL result", "MySqlClient\."]
        self.PostgreSQL = ["PostgreSQL.*ERROR", "Warning.*\Wpg_.*", "valid PostgreSQL result", "Npgsql\."]
        self.MicrosoftSQLServer = ["Driver.* SQL[\-\_\ ]*Server", "OLE DB.* SQL Server", "(\W|\A)SQL Server.*Driver", "Warning.*mssql_.*", "(\W|\A)SQL Server.*[0-9a-fA-F]{8}", "(?s)Exception.*\WSystem\.Data\.SqlClient\.", "(?s)Exception.*\WRoadhouse\.Cms\."]
        self.MicrosoftAccess = ["Microsoft Access Driver", "JET Database Engine", "Access Database Engine"]
        self.Oracle = ["\bORA-[0-9][0-9][0-9][0-9]", "Oracle error", "Oracle.*Driver", "Warning.*\Woci_.*", "Warning.*\Wora_.*"]
        self.IBMDB2 = ["CLI Driver.*DB2", "DB2 SQL error", "\bdb2_\w+\("]
        self.SQLite = ["SQLite/JDBCDriver", "SQLite.Exception", "System.Data.SQLite.SQLiteException", "Warning.*sqlite_.*", "Warning.*SQLite3::", "\[SQLITE_ERROR\]"]
        self.Sybase = ["(?i)Warning.*sybase.*", "Sybase message", "Sybase.*Server message.*"]
        self.AllVulns = self.MySQL+self.PostgreSQL+self.MicrosoftSQLServer+self.MicrosoftAccess+self.Oracle+self.IBMDB2+self.SQLite+self.Sybase
        
    def content_check(self,content):
        for vuln in self.AllVulns:
            if(re.search(vuln, content)):
                vulnIndex = self.AllVulns.index(vuln)
                if(vulnIndex < 3):
                    sql = "MySQL"
                elif(vulnIndex < 7):
                    sql = "PostgreSQL"
                elif(vulnIndex < 14):
                    sql = "MicrosoftSQLServer"
                elif(vulnIndex < 17):
                    sql = "MicrosoftAccess"
                elif(vulnIndex < 22):
                    sql = "Oracle"
                elif(vulnIndex <25):
                    sql = "IBDMDB2"
                elif(vulnIndex <31):
                    sql = "SQLite"
                else:
                    sql = "Sybase"
                return True,sql
        return False,None
    

def VulnCheck(url):
    try:
        parsed_url = urlsplit(url)
        if(parsed_url.query.find("'")>-1):
            new_url = url
        else:
            query = parsed_url.query.replace('=', "='")
            new_url = urlunsplit((parsed_url.scheme, parsed_url.netloc, parsed_url.path, query, parsed_url.fragment))
        user_agent = {'User-agent': useragent.get_useragent()}
        response = requests.get(new_url,headers=user_agent,timeout=15)
        vulner = vulndetector()
        isVulnerable = vulner.content_check(response.text)
        if(isVulnerable[0]):
            vulnerable.append(f"{url} - {isVulnerable[1]}")
            colorprint.colorprint(f"Vulnerable: {url} - {isVulnerable[1]}","v")
    except:
        pass

def VulnMain(url_list,thread):
    global vulnerable
    
    unique_urls = []
    unique_domains = set()
    for url in url_list:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain not in unique_domains:
            unique_domains.add(domain)
            unique_urls.append(url)
    url_list = unique_urls
    threads = []
    i = 0
    while(i < len(url_list)):
        for j in range(i,min(i+thread,len(url_list))):
            try:
                t = threading.Thread(target=VulnCheck,args=(url_list[j],))
                threads.append(t)
                t.start()
            except:
                pass
        for t in threads:
            t.join()
        i += thread
        threads = []
    return vulnerable
