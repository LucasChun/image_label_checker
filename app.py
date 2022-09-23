import csv
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from pager import Pager
import glob
import json
import time

def read_table(url):
    """Return a list of dict"""
    # r = requests.get(url)
    with open(url) as f:
        return [row for row in csv.DictReader(f.readlines())]

SELECT_DIR = 'eye_glasses'
APPNAME = "Checker"
STATIC_FOLDER = 'dataset'
images = glob.glob(f'./dataset/Eye/{SELECT_DIR}/vis/*.jpg')
pager = Pager(len(images))


app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config.update(
    APPNAME=APPNAME,
    )


@app.route('/')
def index():
    return redirect('/0')


@app.route('/<int:ind>/')
def image_view(ind=None):
    if ind >= pager.count:
        return render_template("404.html"), 404
    else:
        x_list, y_list = [], []
        pager.current = ind
        image = images[ind].split('/')[-1]
        with open('./dataset/Eye/eye_glasses/gt/'+image[:-4]+'.json', 'r') as file:
            data = json.load(file)
            for i in list(map(lambda x:x["points"], data["points"])):
                x_list.append(int(float(i['x'])))
                y_list.append(int(float(i['y'])))
        return render_template(
            'imageview.html',
            index=[min(x_list)-50, min(y_list)-50, max(x_list) - min(x_list) + 100, max(y_list) - min(y_list) + 100],
            pager=pager,
            data=images[ind].split('/')[-1])


@app.route('/goto', methods=['POST', 'GET'])    
def goto():
    return redirect('/'+request.form['index'])

@app.route('/test', methods=['POST'])
def test():
    data = request.get_json()
    with open("./dataset/Eye/eye_glasses/dump.csv",'a+', newline="") as f:
         wr = csv.writer(f)
         wr.writerow([time.strftime('%c', time.localtime(time.time())), SELECT_DIR, data])
    return data
    
if __name__ == '__main__':
    app.run(debug=True)
