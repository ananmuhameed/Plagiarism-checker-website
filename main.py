from flask import Flask, render_template, request
from difflib import SequenceMatcher
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOADS'] = 'uploads/'
app.config['FILE_FORMAT'] = ['.txt']
app.config['MAIN'] = 'mainFile/'


@app.route('/')
def home():
    return render_template('Home-page.html')


@app.route('/results')
def results():
    return render_template("results-page.html")


@app.route('/detection')
def detection():
    return render_template("Detection-page.html")


@app.route('/about')
def about():
    return render_template("About-page.html")


@app.route('/upload', methods=['POST'])
def upload():
    files = []
    list = []
    WORDS = []
    similars = []
    dic = {}
    for f in request.files.getlist('main'):
        f.save(os.path.join(
            app.config['MAIN'],
            secure_filename(f.filename)
        ))
        with open(os.path.join(app.config['MAIN'], f.filename), "r") as file:
            s = file.read()
        main_file = s

    # search for input with name file in array of files
    for f in request.files.getlist('file'):
        if f:
            extension = os.path.splitext(f.filename)[1]
            if extension not in app.config['FILE_FORMAT']:
                return 'wrong format'
            f.save(os.path.join(
                app.config['UPLOADS'],
                secure_filename(f.filename)
            ))
            with open(os.path.join(app.config['UPLOADS'], f.filename), "r") as file:
                x = file.read()
            list.append(x)
            print('l', list)

    files = os.listdir(app.config['UPLOADS'])
    for i in range(len(list)):
        similarity = SequenceMatcher(None, main_file, list[i]).ratio()
        similars.append(similarity*100)

    dic = {
        'all': [['file1.txt', 200.0]]
    }

    for num in range(len(files)):
        dic['all'].append([files[num], similars[num]])

    length = len(dic['all'])
    print(dic)

    return render_template('results-page.html', dic=dic['all'], len=length)


if __name__ == '__main__':
    app.run(debug=True, port=5555)
