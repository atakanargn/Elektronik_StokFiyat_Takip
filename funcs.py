from bs4 import BeautifulSoup
import requests
import pymongo

mClient = pymongo.MongoClient("mongodb://root:t1npets32@37.148.208.233:27017/?authSource=admin")
# Veritabanları
# print(mClient.list_database_names())
mDB = mClient['urun-toplama']
mCol = mDB['urunler']

def veriKaydet(site, baslik, fiyat, resim, stok):
    olustur = mCol.insert_one({
        "site":site,
        "baslik":baslik,
        "fiyat":fiyat,
        "resim":resim,
        "stok":stok
    })

    for x in mCol.find({},{ "_id": olustur.inserted_id}):
        print(x['baslik'])

def veriOku(mID):
    for x in mCol.find({},{ "_id": mID}):
        print(x)

def direncCek_Kaydet(kategori,stok,dosya):
    mFile = open(dosya,"w+")
    # SAYFA SAYISI BULDURMA
    url = "https://www.direnc.net/{}".format(kategori)
    r = requests.get(url)
    source = BeautifulSoup(r.content, "html.parser")
    sayfaSayac = source.findAll("div", attrs={"class", "box-border productPager"})
    sayfalar = sayfaSayac[0].findAll("a")
    sayfa=len(sayfalar)-3
    
    metin = ""
    for i in range(1,sayfa+1):
        print("SAYFA "+str(i)+" ############################\n")
        url = "https://www.direnc.net/{}?pg={}".format(kategori,i)

        r = requests.get(url)
        # BeautifulSoup ile kaynak kodu, html.parser modunda inceleyeceğiz
        source = BeautifulSoup(r.content, "html.parser")

        urunler = source.findAll("div", attrs={"class", "productItem"})

        for urun in urunler:
            baslik = urun.findAll("a", attrs={"class":"productDescription"})[0]
            fiyat  = urun.findAll("span", attrs={"class":"currentPrice"})[0]
            resim  = urun.findAll("img")
            resim = (str(resim[0]).split("data-src=\"")[1]).split("\"")[0]

            if(stok==0):
                if(len(urun.findAll("span",attrs={"class":"out-of-stock"}))>0):
                    metin += baslik.text.strip() + "<:>" + resim.strip() + "<:>" + fiyat.text + "\n"
            else:
                if(len(urun.findAll("span",attrs={"class":"out-of-stock"}))>0):
                    break
                metin += baslik.text.strip() + "<:>" + resim.strip() + "<:>" + fiyat.text + "\n" 
    mFile.write(metin)
    mFile.close()

def f1depoCek(kategori,stok,dosya):
    mFile = open(dosya,"w+")
    # SAYFA SAYISI BULDURMA
    url = "https://www.f1depo.com/kategori/{}".format(kategori)
    r = requests.get(url)
    source = BeautifulSoup(r.content, "html.parser")
    sayfaSayac = source.findAll("div", attrs={"class", "_paginateContent"})
    sayfalar = sayfaSayac[0].findAll("a")
    sayfa=len(sayfalar)

    metin=""
    for i in range(1,sayfa+1):
        print("SAYFA "+str(i)+" ############################\n")
        url = "https://www.f1depo.com/kategori/{}?tp={}".format(kategori,i)

        r = requests.get(url)
        # BeautifulSoup ile kaynak kodu, html.parser modunda inceleyeceğiz
        source = BeautifulSoup(r.content, "html.parser")
        urunler = source.findAll("div","_productItem")

        for urun in urunler:
            baslik = urun.findAll("div", attrs={"class":"showcaseTitle"})[0]
            fiyat  = urun.findAll("div", attrs={"class":"showcasePriceTwo showcasePriceOnly"})[0]
            resim  = urun.findAll("div",attrs={"class":"showcasePicture"})[0]
            resim = resim.findAll("img")
            resim = (str(resim[0]).split("src=\"")[1]).split("\"")[0]
            stokDurumu = urun.findAll("div", attrs={"class":"showcaseAdttocart"})
            stokDurumu = stokDurumu[0].findAll("img",attrs={"src":"//st3.myideasoft.com/shop/dt/63/themes/selfbtn_1/nostock.gif"})

            if(stok==0):
                if(len(stokDurumu)>0):
                    metin += baslik.text.strip() + "<:>" + "http://"+resim[2:] + "<:>" + fiyat.text.strip() + "\n"
            else:
                if(len(stokDurumu)>0):
                    break
                metin += baslik.text.strip() + "<:>" + "http://"+resim[2:] + "<:>" + fiyat.text.strip() + "\n" 
    mFile.write(metin)
    mFile.close()

def robolinkCek(kategori,stok,dosya):
    mFile = open(dosya,"w+")
    # SAYFA SAYISI BULDURMA
    url = "https://www.robolinkmarket.com/{}".format(kategori)
    r = requests.get(url)
    source = BeautifulSoup(r.content, "html.parser")
    sayfaSayac = source.findAll("div", attrs={"class", "productPager"})
    sayfalar = sayfaSayac[0].findAll("a")
    sayfa=len(sayfalar)-3
    
    metin = ""
    for i in range(1,sayfa+1):
        print("SAYFA "+str(i)+" ############################\n")
        url = "https://www.robolinkmarket.com/{}?pg={}".format(kategori,i)

        r = requests.get(url)
        # BeautifulSoup ile kaynak kodu, html.parser modunda inceleyeceğiz
        source = BeautifulSoup(r.content, "html.parser")

        urunler = source.findAll("div", attrs={"class", "productItem"})

        for urun in urunler:
            baslik = urun.findAll("a", attrs={"class":"urunismi"})[0]
            fiyat  = urun.findAll("div", attrs={"class":"productPrice"})[0]
            resim  = urun.findAll("img", attrs={"class":"stImage"})
            resim = (str(resim[0]).split("src=\"")[1]).split("\"")[0]

            if(stok==0):
                if(len(urun.findAll("span",attrs={"class":"out-of-stock"}))>0):
                    metin += baslik.text.strip() + "<:>" + resim.strip() + "<:>" + fiyat.text.strip() + "\n"
            else:
                if(len(urun.findAll("span",attrs={"class":"out-of-stock"}))>0):
                    break
                metin += baslik.text.strip() + "<:>" + resim.strip() + "<:>" + fiyat.text.strip() + "\n" 
    mFile.write(metin)
    mFile.close()