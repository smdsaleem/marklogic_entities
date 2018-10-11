# -*- coding: utf-8 -*-
"""
Created on Wed May 30 12:05:18 2018

@author: mohsheik
"""
from flask import Flask, abort, request 
import json
#from mlconnect import getEntity 
app = Flask(__name__)      

@app.route('/getmlEntity', methods=['POST'])
def getMLEntity():
    if not request.json:
        abort(400)

    return "HERE"


if __name__ == '__main__':
    app.run(host= '0.0.0.0',port=6006)
    app.run(debug=True)