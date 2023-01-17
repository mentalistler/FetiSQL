import argparse
from tools import DorkScanner
from tools import SQLVulnDetector
from tools import colorprint
from datetime import datetime
import time
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dork", help="Dork file")
parser.add_argument("-e", "--engine",default="neeva", help="Dork engine neeva,ask,searchencrypt, default:neeva")
parser.add_argument("-v","--vuln", help="Just Vulnerability websites", action="store_true")
parser.add_argument("-t", "--thread",help="Thread count")
parser.add_argument("-o", "--output",help="Output directory")
args = parser.parse_args()

output_path = args.output

if(args.thread):
    thread_count = int(args.thread)
else:
    thread_count = 5


if(args.dork):
    DorkPath = args.dork
    engine = args.engine
    print(engine)
    colorprint.colorprint("Dorks Scanning...")
    UrlList = DorkScanner.SearchMain(DorkPath,thread_count,engine)
    colorprint.colorprint("Dork Scanning Proccess Completed.")
    if(args.vuln):
        colorprint.colorprint("SQL Scanning...")
        results = SQLVulnDetector.VulnMain(UrlList,thread_count)
        colorprint.colorprint("SQL Scanning Proccess Completed.")
    else:
        results = UrlList
    if output_path:
        if output_path.count('/') > 0:
            with open(output_path, "w") as file:
                file.writelines("%s\n" % url for url in results)
        else:
            with open(f"{output_path}/unique_urls.txt", "w") as file:
                file.writelines("%s\n" % url for url in results)
    else:
        current_time = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d-%H-%M-%S")
        with open("FetiSQL-{}.txt".format(current_time), "w") as file:
            file.writelines("%s\n" % url for url in results)
else:
    colorprint.colorprint("Invalid dork file.","v")
