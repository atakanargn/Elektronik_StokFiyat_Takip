from flask import Flask, render_template, request
# from funcs import *
from os import getcwd
app = Flask(__name__)

@app.route("/urunler", methods=['GET', 'POST'])
def urunler():
    liste = []
    if(request.method=="GET"):
        site = request.args.get('site')
        kategori = request.args.get('kategori')
        with open("D:/Piton/UrunToplama/siteler/{}/{}.txt".format(site,kategori)) as f:
            metin = f.readlines()
            for satir in metin:
                baslik,resim,fiyat = satir.split("<:>")[0],satir.split("<:>")[1],satir.split("<:>")[2][:-1]
                liste.append({"baslik":baslik,"resim":resim,"fiyat":fiyat})
        return render_template("urunler.html",gelen=liste)


if __name__ == '__main__':
    app.run()