from flask import Flask, request, jsonify, render_template
app = Flask(__name__)
from json2html import *
import json
import scrap_bot as sb
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search',methods=['POST'])
def search():
    e=request.form['email']
    p=request.form['password']
    s=request.form['search']
    pg=request.form['pages']
    sb.bot.start(email=e,password=p,search=s,pages=int(pg))
    msg="searching is done !!"
    return render_template('profiles.html',msg=msg)

@app.route('/result',methods=['GET'])
def result():
    with open(r"profiles_dataset.json", "r") as read_file:
        profiles_list = json.load(read_file)
    
    # contet=jsonify(profiles_list)
    return render_template('profiles.html', contet=profiles_list)

if __name__ == "__main__":
    app.run(debug=True)