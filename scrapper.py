from bs4 import BeautifulSoup
import nmap
import requests
import subprocess

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
"Accept":"text/html,application/xhtlm+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

class Botnet:
    def __init__(self, date, url, ip, family):
        self.date = date
        self.url = url
        self.ip = ip
        self.family = family
        self.online = False
        self.tor = False
        self.ports = []
        self.country = None
        self.server = None
        self.so = None

    def setOnlineStatus(self):
        try:
            r = requests.get("http://" + self.url, headers = headers)
            if r.status_code == 200:
                self.online = True
            else:
                self.online = False

        except requests.exceptions.ConnectionError:
            self.online = False

    def getServer(self):
        try:
            r = requests.get("http://" + self.url, headers = headers)
            if r.headers['server'] != None:
                self.server = r.headers['server']

        except:
            return

    def setCountry(self):
        u = self.url.find('/')
        p = subprocess.Popen(["geoiplookup", self.url[:u]], stdout=subprocess.PIPE)
        output, err = p.communicate()
        self.country = output.decode(encoding='UTF-8')[23:]

    def getOpenPorts(self):
        nm = nmap.PortScanner()
        u = self.url.find('/')
        host = self.url[:u]
        nm.scan(host, '1-1000')
        self.ports = nm[nm.all_hosts()[0]]['tcp'].keys()



r = requests.get('http://cybercrime-tracker.net/index.php?s=0&m=10').text

soup = BeautifulSoup(r, 'html.parser')

botnets_list = soup.find('tbody').find_all('tr')

botnets = []

for server in botnets_list:
    data = server.find_all('td')
    bot_info = []
    for d in data:
        bot_info.append(d.text)

    botnets.append(Botnet(bot_info[0], bot_info[1], bot_info[2], bot_info[3]))

for bot in botnets:
    print(bot.family, end=" ")
    bot.setOnlineStatus()
    bot.setCountry()
    bot.getServer()
    bot.getOpenPorts()
    print(bot.ports)
