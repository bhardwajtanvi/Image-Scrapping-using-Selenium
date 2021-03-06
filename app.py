from flask import Flask,redirect,url_for,render_template,request,send_file,send_from_directory, safe_join, abort
import img_scrapper
from img_scrapper import search_and_download
from img_scrapper import makezip
from img_scrapper import delunwantedzip
import os
from os import path
import time
import requests
from selenium import webdriver
import shutil
import glob





app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/result.html",methods=['POST','GET'])
def display():
    try:
        if request.method == 'POST':

            name = request.form['Item-Name']
            num= request.form['Item-Number']
            nums= int(num)
            # print(type(nums))
            search_and_download(search_term=name,number_images=nums) # method to download images
            output=makezip(search_term=name,number_images=nums)
            return render_template("result.html",value=output)
        
    except Exception as e:
        return render_template("handler.html", error = str(e))


@app.route('/delete/<file>',methods=['POST'])
def delete(file):
    t=30
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1
    os.remove("static/"+file)
    return True


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
    