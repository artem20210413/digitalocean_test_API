from flask import request, Flask, render_template, url_for,  redirect
#from flask import request
from flask_sqlalchemy import  SQLAlchemy
from  datetime import  datetime
import requests
URL = 'https://api.digitalocean.com/v2/droplets'
KEY = '189ca8959a7d2b1357705e359632e4ba33666e088c1d8f3bb833a989b98757c1'


def get_all_digital():
    headers_auth = {'Content-Type': 'application/json','Authorization': 'Bearer  ' + KEY};
    r = requests.get(URL, headers=headers_auth)
    info = r.json()
    try:
        print(r.status_code)
        return info
    except:
        print('ERROR!')


def delete_digital(id):
    headers_auth = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + KEY};
    r = requests.delete(URL + "/" + id, headers=headers_auth)
    info = r.json()
    try:
        print(r.status_code)
        return info['droplets']
    except:
        print('ERROR!')

def post_digital(name):
    headers_auth = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + KEY};

    params = {
     "name": name,
     "region": "nyc3",
     "size": "s-1vcpu-1gb",
     "image": "ubuntu-16-04-x64",
     "ssh_keys": [29963105],
     "backups": False,
     "ipv6": True,
     "user_data": None,
     "private_networking": None,
     "volumes": None,
     "tags": ["web"]
        }
    r = requests.post(URL, headers=headers_auth, params=params)
    info = r.json()
    try:
        print(r.status_code)
        return r.status_code
    except:
        print('ERROR!')


def get_trenslation(text):
    URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'
    URL_TRANSLATE = 'https://developers.lingvolive.com/api/v1/Minicard'
    KEY = 'MWE2ZTUzZDktN2E5OS00YWQ5LTkwZjgtNzFjMmMyZGUzN2U5OjEwYWYyYzU4OTVjMzQ3ZmFhNDJiMmQ3NGM0N2Q0ZmQ1'
    headers_auth = {'Authorization': 'Basic ' + KEY};

    auth = requests.post(URL_AUTH, headers=headers_auth);
    if auth.status_code == 200:
        token = auth.text
        #word = input('Введите слово для перевода: ')
        #if word:
        headers_translate = {'Authorization': 'Bearer  ' + token}
        params = {'text': text, 'srcLang': 1049, 'dstLang': 1033, }
        r = requests.get(URL_TRANSLATE, headers=headers_translate, params=params)
        translate = r.json()
        try:
            print(translate['Translation']['Translation'])
            return translate['Translation']
        except:
            print('Не найдено перевода...')
    else:
        print('Error!')




app = Flask(__name__)
app.config['SQLALCHEMY_DATDBASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
@app.route('/home')
def indwx():
    return render_template("/index.html")




@app.route('/droplets', methods=['POST', 'GET'])
def droplets():
    droplets=get_all_digital()
    return render_template('/droplets.html', droplets=droplets)


@app.route('/create_server', methods=['POST', 'GET'])
def create_server():
    status_code= ""
    if request.method == "POST":
        nameserver = request.form['nameserver']
        status_code= str(post_digital(nameserver))


    return render_template("/create_server.html", status_code=status_code )


@app.route('/droplets/delete/<string:id>')
def user_name(id):
    delete_digital(id)
    return droplets()








@app.route('/text_translation', methods=['POST', 'GET'])
def text_translation():
    translation = " "
    if request.method == "POST":
        title = request.form['title']
       #intro = request.form['intro']
        #text = request.form['text']
        translation = get_trenslation(title)
        return render_template('/text_translation.html', translation=translation)
    else:
        return render_template("/text_translation.html", translation=translation)


#@app.route('/user/<string:name>/<int:id>')
#def user_name(name, id):
    #return "Hello " + name + " you id this is: " + str(id)


if __name__ =="__main__":
    app.run(debug=True)


