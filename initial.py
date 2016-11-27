from flask import Flask, render_template, request,  redirect
import hashlib
import urlparse
import string
import json

app = Flask(__name__)
application = app
# our hosting requires application in passenger_wsgi
@app.route("/", methods=['GET'])
def hello():
    return render_template('index.html')

@app.route("/shorten",methods=['POST'])
def shorten_URL():
    url_to_shorten = request.form['input_url']
    parts = urlparse.urlparse(url_to_shorten)
    if not parts.scheme in ('http', 'https'):
        error = "Please enter valid url"
    else:
        shorten_id = shorten(url_to_shorten)
    return render_template('result.html', short_id=shorten_id)

def shorten(url_to_short):
    with open('url_container.json','r') as json_data:
        url_json = json.load(json_data)
    new_url_id = url_json['urls'][-1]['id'] + 1
    encoded_url = url_to_base62(new_url_id)
    url_json['urls'].append({})
    url_json['urls'][-1]['id'] = new_url_id
    url_json['urls'][-1]['original_url'] = url_to_short
    url_json['urls'][-1]['shorten_url'] =  encoded_url
    with open('url_container.json','w') as json_data:
        json.dump(url_json, json_data)
    return encoded_url

def url_to_base62(number):
    base_num = 62
    base = string.lowercase + string.uppercase + string.digits
    url_encode = []
    while number != 0:
        number, i = divmod(number, base_num) #fix it
        url_encode.append(base[i])
    return "".join(url_encode)

@app.route("/<short_id>")
def to_long_url(short_id):
    my_url = "http://127.0.0.1:8081/"
    with open('url_container.json','r') as json_data:
        url_json = json.load(json_data)
    for url_struct in url_json['urls']:
        if(short_id == url_struct['shorten_url']):
            real_url = url_struct['original_url']
            return redirect(real_url)
            break
    return
if __name__ == "__main__":
    app.run(port=8081)
