#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from gen_mcq import display
import pandas as pd
import time

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/result/', methods=['GET', 'POST'])
def mcq_results():
    # Use these signatures to pass in function
    start = time.time()
    display(request.form['paragraph'], request.form['num'])
    data = pd.read_json('response.json')
    data = data.to_json(orient='records')
    print("Finally returning Response...")
    print("Total time to make MCQ: ", time.time() - start)
    #time.sleep(6)
    return data  # pass JSON as string, will be parsed in JQuery


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
