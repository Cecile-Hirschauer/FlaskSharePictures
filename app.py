import os
from flask import Flask, g, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import sqlite3

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATABASE = "app.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route("/")
def index():
    db = get_db()
    pictures = db.execute("""SELECT path
                          FROM pictures
                          ORDER BY creation_date DESC""")
    categories = db.execute("SELECT name FROM categories ORDER BY name")
    my_categories = categories.fetchall()
    print("categories:", my_categories[0])
    return render_template('index.html', all_pictures=pictures, all_categories=my_categories)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route("/upload", methods=["POST"])
def upload_img():
    if 'file' not in request.files:
        return redirect("/upload")
    file = request.files['file']
    # print(file)
    if file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename)) 
        db = get_db()
        db.execute("INSERT INTO pictures(path) VALUES (?)", [filename])
        db.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
