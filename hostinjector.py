import argparse,requests,sys
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ap = argparse.ArgumentParser()
ap.add_argument("--list", required=True,help="Set Domain List")
ap.add_argument("--threads",required=True,help="Threads")
ap.add_argument("--timeout",required=True,help="Request Timeout")
ap.add_argument("--clear",action="store_true",required=False)
args = vars(ap.parse_args())

threadPool = ThreadPoolExecutor(max_workers=int(args["threads"]))

def prBanner():
	print(colored("""
                               /$$          
                              | $$          
 /$$   /$$ /$$   /$$  /$$$$$$ | $$  /$$$$$$ 
|  $$ /$$/| $$  | $$ /$$__  $$| $$ /$$__  $$
 \  $$$$/ | $$  | $$| $$$$$$$$| $$| $$$$$$$$
  >$$  $$ | $$  | $$| $$_____/| $$| $$_____/
 /$$/\  $$|  $$$$$$$|  $$$$$$$| $$|  $$$$$$$
|__/  \__/ \____  $$ \_______/|__/ \_______/
           /$$  | $$                        
          |  $$$$$$/                        
           \______/                                             
           ""","blue"))
	pass

def testIt(url):
	headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0","X-Forwarded-Host":"xyele.com"}
	r = requests.head(url,allow_redirects = False,verify=False,headers=headers,timeout = int(args["timeout"]))
	try:
		if r.headers["Location"].replace("https://","").replace("http://","").startswith("xyele.com"):
			print(url) if args["clear"] else print(colored("[+] {} redirects to {}".format(url,r.headers["Location"]),"green")+"\n\n"+r.text+"\n\n")
			pass
		else:
			not args["clear"] and print(colored("[-] {}".format(url),"red"))
			pass
		pass
	except Exception as e:
			not args["clear"] and print(colored("[-] {}".format(url),"red"))
			pass
prBanner()
hostList = open(args["list"], "r").read().split("\n")
for host in hostList:
	host = host.replace("https://","").replace("http://","")
	if "/" in host:
		host = host.split("/")[0]
		pass
	threadPool.submit(testIt,"http://{}/".format(host))
	threadPool.submit(testIt,"https://{}/".format(host))
	pass
threadPool.shutdown(wait=True)
