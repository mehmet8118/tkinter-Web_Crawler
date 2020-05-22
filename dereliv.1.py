# -*- coding: utf-8 -*-
__author__ = 'mehmet şerif paşa'

from tkinter import *
from tkinter import PhotoImage
from urllib.parse import unquote
import re
import socket
import random
import requests

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")



class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title('DERELI v.1') #pencere başlığı
        self.geometry('1100x800+150+150') #enini boyunu, pencere konumu (nerde dursun açıldığında)
        self.resizable(FALSE, FALSE) #pencere boyut yasağı
        self.GOOGLE_URL_LIST = set() #google'dan aldığımız linkleri burda tutuyoruz
        self.CONTENT_URL_LIST = set()
        self.GOOGLE_AND_CONTENT_URL_LIST_KNIT = set()
        self.DIRECTORY = set()
        self.DIRECTORY_2 = set()
        self.TOTAL_URL = set()
        self.say = 0
        self.NOT_CONTENT_URL_LIST = set()  # farklı domain'e ait siteleri tutar
        self.USERAGENT = [agent.strip() for agent in open('PAYLOADS/useragent.txt')]
        self.Random_Useragent = random.choice(self.USERAGENT)

    def Request(self):
        self.host = str(self.veri_al.get())
        # İstek burda yapılıyor ve bunun üzerinden işlem yapılıyor.
        self.req = requests.get(self.host)  # Siteye GET isteği yapılmıştır
        self.req_content = self.req.content  # Sitenin kaynak bilgisi
        self.req_headers = self.req.headers  # Sitenin Headers bilgisi
        self.req_status_code = self.req.status_code  # Sitenin durum kodu (200,301 vs.)
        self.req_history = self.req.history  # Sitedeki yönlendirmeleri gösteriyor
        self.req_text = self.req.text  # Düzenli bir şekilde kaynak kodu
        for value,keys in self.req_headers.items():
            self.text1.insert(END, str(value)+": "+str(keys) +"\n")

    def Host_Look(self):
        # Düzenli gözükmesi için verilen site url'sini,  split işlemine sokarak temiz bir host elde ediyoruz.
        self.host_strip = self.host.split("://")[1]

    def Ip_Look(self):
        # Verdiğimiz sitenin ip bilgisini veriyor
        self.host_ip = socket.gethostbyname(self.host_strip)
        if self.host_ip:
            self.label_ip_text.insert(END, str(self.host_ip))
        else:
            self.label_ip_text.insert(END, "İp bulunamadı...")

    def Port_Scanner(self):
        self.port_scanner_say = 0
        self.portlist = [21, 22, 23, 25, 53, 69, 80, 110, 137, 139, 443, 445, 3306, 3389, 5432, 5900, 8080, 1433]
        self.Codes = {
            0: 'Port acik',
            1: 'İşlem izni verilmedi',
            2: 'Böyle bir dosya veya dizin yok',
            6: 'Böyle bir cihaz veya adres yok',
            11: 'Kaynak geçici olarak kullanılamıyor',
            13: 'İzin reddedildi',
            14: 'Hatalı adres',
            61: 'Veri yok',
            67: 'Bağlantı koptu',
            71: 'Protokol hatası',
            87: 'Çok fazla kullanıcı',
            100: 'Ağ kapalı',
            101: 'Ağa erişilemiyor',
            110: 'Bağlantı zaman aşımına uğradı',
            111: 'Bağlantı reddedildi',
            112: 'Ana makine çalışmıyor',
        }
        for i in self.portlist:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                ver = sock.connect_ex((self.host_ip, int(self.portlist[self.port_scanner_say])))
                self.text3.insert(END, str(self.portlist[self.port_scanner_say]) + ' | ' + self.Codes[ver] + "\n")
                sock.close()

            except:
                self.text3.insert(END, str(self.portlist[self.port_scanner_say]) +  " | Port Kapalı" + "\n")
            self.port_scanner_say += 1

    def Host_Strip_www(self):
        if 'www' in self.host_strip:
            self.host_strip_control = str(self.host_strip).split('www.')[1]
        else:
            self.host_strip_control = str(self.host_strip)

    def Google_Search_Path_Crawler(self):  # Google yardımıyla ek olarak url aldık
        query = "site:" + str(self.host_strip)

        for j in search(query, num=50, stop=50, pause=2):
            self.text2.insert(END, str(j))
            self.GOOGLE_URL_LIST.add(str(j))
            for k in self.GOOGLE_URL_LIST:
                self.GOOGLE_AND_CONTENT_URL_LIST_KNIT.add(k)

    def Url_Crawler_SECTION_2_(self): # DİZİN AYIRMA İŞLEMİ
        for i in self.GOOGLE_AND_CONTENT_URL_LIST_KNIT:
            if self.host_strip_control in i.split('/')[2]: #[2] = domain
                try:
                    if i.split('/')[3]: # Neden 12 tane derseniz en son ihtimale kadar parçalama yapmaya çalıştım. Arttırılabilir
                        self.DIRECTORY_2.add(str(  i.split('/')[3]  ))
                    if i.split('/')[4]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4]))
                    if i.split('/')[5]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4]) + '/' + i.split('/')[5])
                    if i.split('/')[6]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4]) + '/' + i.split('/')[5] + '/' + i.split('/')[6])
                    if i.split('/')[7]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6]) + '/' + i.split('/')[7])
                    if i.split('/')[8]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5]) + '/' + i.split('/')[6] + '/' + i.split('/')[7] + '/' + i.split('/')[8])
                    if i.split('/')[9]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6]) + '/' + i.split('/')[7] + '/' + i.split('/')[8] + '/' + i.split('/')[9])
                    if i.split('/')[10]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6] + '/' +i.split('/')[7] + '/' +i.split('/')[8] + '/' + i.split('/')[9] + '/' + i.split('/')[10]))
                    if i.split('/')[11]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6] + '/' +i.split('/')[7] + '/' +i.split('/')[8] + '/' + i.split('/')[9] + '/' + i.split('/')[10] + '/' + i.split('/')[11]))
                    if i.split('/')[11]:
                        self.DIRECTORY_2.add(str( i.split('/')[3] + '/' + i.split('/')[4] + '/' + i.split('/')[5] + '/' + i.split('/')[6] + '/' +i.split('/')[7] + '/' +i.split('/')[8] + '/' + i.split('/')[9] + '/' + i.split('/')[10] + '/' + i.split('/')[11] + '/' + i.split('/')[11]))
                    """
                    test/test1/test2
                    |
                    |_______test1
                    |_________test1/test2
                    |____________test1/test2/test3
                    |_______________test1/test2/test3/test4 ...
                    """
                except:
                    continue
        for l in self.DIRECTORY_2:
            self.text2.insert(END, str(l) + "\n")

    def Url_Crawler_SECTION_3(self):
        """
        Parçalama yaptığımız URl'lere tekrar istek yollayarak yeni urller elde edicez
        """
        path = [path.strip() for path in self.DIRECTORY_2]
        def Section_3_Crawl():
            self.say += 1
            try:
                for i in self.DIRECTORY_2:
                    self.Section_3_Request = requests.get(self.host + '/' + i , timeout=2, headers= {'User-Agent':self.Random_Useragent})
                    self.Section_3_Content = self.Section_3_Request.content
                    links = re.findall('"((http|ftp)s?://.*?)"', self.Section_3_Content)
                    for t in links:
                        if self.host_strip_control in t[0]:
                            self.TOTAL_URL.add(t[0])
                            self.text2.insert(END, str(t[0]) +"\n")
                        else:
                            self.NOT_CONTENT_URL_LIST.add(t[0])
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.SSLError:
                pass
            except:
                pass

    def List_Pars(self): #Topladığımız bütün linkleri birleştiriyoruz
        for g in self.DIRECTORY_2:
            self.TOTAL_URL.add(str(g))
        for h in self.GOOGLE_AND_CONTENT_URL_LIST_KNIT:
            self.TOTAL_URL.add(str(h))
        for j in self.CONTENT_URL_LIST:
            self.TOTAL_URL.add(str(j))
        for t in self.GOOGLE_URL_LIST:
            self.TOTAL_URL.add(str(t))

    def Total(self):
        for k in self.TOTAL_URL:
            self.text2.insert(END, str(k) +"\n")

    def archive_web(self):
        url = "http://web.archive.org/cdx/search/cdx?url=*."+ str(self.host_strip) +"/*&output=text&fl=original&collapse=urlkey"
        archive_req = requests.get(url)
        for k in archive_req:
            urll = k.decode('utf-8')
            self.text2.insert(END, unquote(urll) +"\n")

    def gövde(self):

        self.label_ip = Label(
            text = "İp Adresi: ",
            font = ('open sans', 15, "bold")
        )
        self.label_ip_text = Text(
            bg="#E7E2E2",
            font = ("open sans", 15, "bold"),
            relief = SUNKEN,
            bd=1,
            width = 13,
            height = 1
        )

        self.baslik = Label(
        text="Site",
        font=('open sans', 30, "bold"))

        self.veri_al = Entry()

        self.buton1 = Button(
            text="Tara",
            command = lambda:[self.Request(), self.Host_Look(), self.Ip_Look(), self.Port_Scanner(),
                              self.Host_Strip_www(),self.Url_Crawler_SECTION_2_,
                              self.Url_Crawler_SECTION_3(),
                              self.List_Pars(), self.Total(), self.archive_web()],
            bg="red")

        self.text_yazı = Label(
            text="Headers",
            font=('open sans', 15, "bold"),
            justify="center")

        self.text1 = Text(
            bg="#E7E2E2",
            height=10,
            width=45,
            font=("open sans", 15, "bold"),
            relief=SUNKEN,  # çerçeve
            bd=2  # çerçeve genişliği
        )

        self.text_yazı2 = Label(
            text="Url List",
            font=('open sans', 15, "bold"),
            justify="center")

        self.text2 = Text(
            bg="#E7E2E2",
            height=32,
            width=50,
            font=("open sans", 15, "bold"),
            relief = SUNKEN, #çerçeve
            bd = 2# çerçeve genişliği
        )

        self.text_yazı3 = Label(
            text="Port Scanner",
            font=('open sans', 15, "bold")
        )

        self.text3 = Text(
            bg="#E7E2E2",
            height=10,
            width=45,
            font=("open sans", 15, "bold"),
            relief=SUNKEN,  # çerçeve
            bd=2  # çerçeve genişliği
        )

        self.label_ip.place(x=10, y=20)
        self.label_ip_text.place(x=90, y=20)

        self.baslik.pack()
        self.veri_al.pack()
        self.buton1.pack()

        self.text_yazı.pack()
        self.text_yazı.place(x=200, y=130) #pozisyonlarını ayarlıyoruz
        self.text1.pack()
        self.text1.place(x=0, y=150)

        self.text_yazı2.pack()
        self.text_yazı2.place(x=800, y=130)
        self.text2.place(x=520, y=150)  # 150 yukardan 200 soldan

        self.text3.pack()
        self.text3.place(x=0, y=370)
        self.text_yazı3.place(x=200, y=350)



if __name__ == "__main__":
    w = Window()
    w.gövde()
    w.mainloop()




