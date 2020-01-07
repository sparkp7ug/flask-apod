from flask import Flask, flash, redirect, render_template, request, session, abort, send_file
import urllib3
import json
import pdfkit
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/apod/<string:date>")
def apod(date):
    if(datetime.datetime.today() > datetime.datetime.strptime(date,'%Y-%m-%d')):
        api_response = urllib3.PoolManager().request('GET','https://api.nasa.gov/planetary/apod?api_key=x7qyRICNLMzDbFt14kL4I3SUeBMWKpziBecV6u07&date='+date)
        result_json = json.loads(api_response.data.decode('utf-8'))
        return render_template('apod.html',imgsrc=result_json['url'],date=date,title=result_json['title'])
    else:
        return '<html><body><h1>Error 404</h1><p>Given date is in future.</p></body></html>'

@app.route("/download/<string:date>")
def download(date):
    if(datetime.datetime.today() > datetime.datetime.strptime(date,'%Y-%m-%d')):
        api_response = urllib3.PoolManager().request('GET','https://api.nasa.gov/planetary/apod?api_key=x7qyRICNLMzDbFt14kL4I3SUeBMWKpziBecV6u07&date='+date)
        result_json = json.loads(api_response.data.decode('utf-8'))
        return render_template('download.html',imgsrc=result_json['url'],date=date,title=result_json['title'])

@app.route("/pdf/<string:date>/")
def downloadPdf(date):
    pdfkit.from_url('http://127.0.0.1/download/'+date,'out.pdf')
    try:
        return send_file('out.pdf', attachment_filename='out.pdf')
    except Exception as e:
        return str(e)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)