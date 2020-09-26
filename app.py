from flask import Flask,redirect,url_for,render_template,request
import img_scrapper
from img_scrapper import search_and_download
from img_scrapper import makezip
import os
from os import path
import time
import requests
from selenium import webdriver
import shutil


DRIVER_PATH = './chromedriver'


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/result.html',methods=['POST','GET'])
def display():
    if request.method == 'POST':
        name = request.form['Item-Name']
        num= request.form['Item-Number']
        nums=int(num)
        print(type(nums))
        search_and_download(search_term=name, driver_path=DRIVER_PATH,number_images=nums) # method to download images
        makezip()
        return render_template("result.html")
        

if __name__ == "__main__":
    
    app.run(debug=False)
