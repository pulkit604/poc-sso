from flask import (Flask, redirect, render_template, request, g, json, jsonify)
from flask_cors import CORS, cross_origin
import sqlite3, random, datetime

app = Flask(__name__, template_folder='template')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

DATABASE = 'database/sso_manage.db'

##Database related functions
def get_db():
    try:
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db
    except Exception as e:
        print(e)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Query helper function as stated in flask docs
#https://flask.palletsprojects.com/en/2.2.x/patterns/sqlite3/
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def clientIsValid(clientId, clientSecret, redirectUri):
    try:
        for client in query_db('SELECT * FROM client WHERE clientId = ? AND clientSecret = ? AND redirectUri = ?;', [clientId, clientSecret, redirectUri], True):
            clientValid = client
        return True
    except Exception as e:
        print(e)
        return None


@app.route('/auth')
def authentication():
    clientId     = request.args.get('clientId')
    clientSecret = request.args.get('clientSecret')
    redirectUri  = request.args.get('redirectUri')
    scopes       = request.args.get('scopes')

    if(clientId == None or clientSecret == None or redirectUri == None) or not clientIsValid(clientId, clientSecret, redirectUri):
        return render_template('client_error.html')

    return render_template('login.html', redirectUri=redirectUri)

def generate_token():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

@app.route('/validate_token', methods=['POST'])
def validate_token():
    requestData   = json.loads(request.data)
    token         = requestData['token']

    try:
        for user in query_db('SELECT token FROM USER WHERE token = ?;', [token], True):
            token      = user['token']
            expireTime = user['expires_in']
        return jsonify({ "status": "valid"
                       })
    except Exception as e:
        return jsonify({ "status": "invalid"
                      })

def getTokenFromDatabase(email, password):
    try:
        for user in query_db('SELECT token FROM USER WHERE email = ? AND password = ?;', [email, password], True):
            token = user
        return token
    except Exception as e:
        return None

@app.route('/login', methods=['POST'])
def login():
    try:
        requestData   = json.loads(request.data)
        redirectUri  =  requestData['redirectUri']
        email         = requestData['email']
        password      = requestData['password']
        token         = getTokenFromDatabase(email, password)
        print(token)
        if token == None:
            return render_template('login.html')
        return jsonify({ "redirectUri": redirectUri,
                         "token": token
        })

    except Exception as e:
        print(e)
        return render_template('login.html')
