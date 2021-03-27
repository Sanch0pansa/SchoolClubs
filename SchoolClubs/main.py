from flask import Flask, render_template, url_for, request, redirect
from db.classes2 import *
import random
from datetime import datetime

app = Flask(__name__)


def main():
    app.run()


@app.route('/')
@app.route('/index/')
def index():
    params = dict()
    params["clubs"] = []
    clubs = manager.get_items("club", "1")
    for club in clubs:
        params["clubs"].append({"id": club.get('id'), "name": club.get('name')})
    return render_template('index.html', params=params)


@app.route('/tutors')
def index():
    params = dict()
    params["clubs"] = []
    clubs = manager.get_items("club", "1")
    for club in clubs:
        params["clubs"].append({"id": club.get('id'), "name": club.get('name')})
    return render_template('index.html', params=params)


@app.route('/statement_handler/', methods=['POST', 'GET'])
def statement_handler():
    if request.method == 'POST':
        args = dict()
        for key in request.form:
            args[key] = request.form[key]
        args['track_code'] = random.choice(['a', 'b', 'c', 'd', 'e']) + \
                             random.choice(['a', 'b', 'c', 'd', 'e']) + \
                             random.choice(['a', 'b', 'c', 'd', 'e']) + str(random.randint(1000, 10000))
        args['statement_ip'] = request.remote_addr
        args['statement_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_statement = Statement(manager, **args)
        users_statements = manager.get_items('statement', f"`statement_ip` = '{request.remote_addr}'")
        if users_statements is None:
            new_statement.add_to_db()
            db.commit()
        else:
            if len(users_statements) < 10:
                new_statement.add_to_db()
        return redirect("http://yandex.ru/maps", code=302)
    return ''


if __name__ == '__main__':
    main()