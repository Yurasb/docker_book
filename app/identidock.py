import hashlib
import html

import redis
import requests
from flask import Flask, Response, request

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0)
salt = u'Unique Salt'
default_name = u'Default Name'


@app.route('/', methods=['GET', 'POST'])
def main_page():
    name = default_name
    if request.method == 'POST':
        name = html.escape(request.form['name'], quote=True)

    salted_name = u'{}{}'.format(salt, name)
    name_hash = hashlib.sha256(salted_name.encode()).hexdigest()
    header = u'<html><head><title>Identodock</title></head><body>'
    body = u'''<form method="POST">
            Hello <input type="text" name="name" value="{0}">
            <input type="submit" value="submit">
            </form>
            <p>You look like a:
            <img src="/monster/{1}"/>'''.format(name, name_hash)
    footer = u'</body></html>'
    return u'{0}{1}{2}'.format(header, body, footer)


@app.route('/monster/<name>')
def get_identickon(name):
    name = html.escape(name, quote=True)
    image = cache.get(name)
    if image is None:
        print('Cache miss', flush=True)
        r = requests.get('http://dnmonster:8080/monster/{0}?size=80'
                         .format(name))
        image = r.content
        cache.set(name, image)
    return Response(image, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
