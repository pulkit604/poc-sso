from flask import (Flask, redirect, render_template, request, g, json, jsonify)
from flask_cors import CORS, cross_origin
import sqlite3, random, datetime

app = Flask(__name__, template_folder='template')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
