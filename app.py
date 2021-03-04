import os
from flask import Flask, g, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import sqlite3

UPLOAD_FOLDER = 'uploads'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = ("JPEG", "JPG", "PNG", "GIF")

DATABASE = "app.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route("/")
def index():
    
    """ show all the pictures order by creation_date desc and all categiries"""
    
    db = get_db()
    pictures = db.execute("""SELECT id, path, title
                          FROM pictures
                          ORDER BY creation_date DESC""")
    categories = db.execute("SELECT name FROM categories ORDER BY name")
    my_categories = categories.fetchall()
    # print("categories:", my_categories[0])
    return render_template('index.html', all_pictures=pictures, all_categories=my_categories)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join("static",app.config['UPLOAD_FOLDER']),
                               filename)


@app.route('/pictures/uploads/<name>')
def downoload_img(name):
    return send_from_directory(os.path.join("static", app.config['UPLOAD_FOLDER']), name)


@app.route('/categories/<name_cat>/pictures/uploads/<name>')
def img_by_cat(name):
    return send_from_directory(os.path.join("static", app.config['UPLOAD_FOLDER']), name)


    
    
@app.route('/categories/<name_cat>/pictures')
def pictures_by_cat(name_cat):
    db=get_db()
    pictures = db.execute("""SELECT pictures.id, path, title
                          FROM pictures
                          LEFT JOIN categories ON pictures.category_id = categories.id
                          WHERE categories.name = ?
                          ORDER BY creation_date DESC""", [name_cat])
    categories = db.execute("SELECT name FROM categories ORDER BY name")
    #cat_pictures = pictures.fetchall()
    my_categories = categories.fetchall()
    # print("categories:", my_categories[0])
    return render_template('index.html', all_pictures=pictures, all_categories=my_categories)
    
    


@app.route('/upload')
def upload():
    db = get_db()
    categories = db.execute("SELECT name FROM categories ORDER BY name")
    my_categories = categories.fetchall()
    all_categories = []
    for category in categories:
        all_categories.append({'name': category[0]})
    if categories != []:
        print(all_categories)
    print("oupsss")
    return render_template('upload.html', all_categories=my_categories)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_img():
    if 'file' not in request.files:
        return redirect("/upload")
    file = request.files['file']
    # print(file)
    if file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename)) 
        title = request.form['title']
        category = request.form['category']
        description = request.form['description']
        db = get_db()
        all_category_id = db.execute("SELECT id FROM categories WHERE name = ?", [category])
        category_id = all_category_id.fetchone()
        print(category_id[0])
        db.execute("INSERT INTO pictures(path, title, category_id, description) VALUES (?, ?, ?, ?)",
                   [filename, title, category_id[0], description])
        db.commit()
    return redirect("/")


# pictures

@app.route('/pictures')
def all_pictures():
    db=get_db()
    cursor = db.execute("""SELECT id, path, title, description from pictures""")
    return render_template('picture.html')


@app.route('/pictures/<int:id>')
def show_picture(id):
    db = get_db()
    cursor = db.execute("SELECT id, path, title, description from pictures where id = ?", [id])
    picture = cursor.fetchone()
    return render_template('picture.html', id=picture[0], path=picture[1], title=picture[2], description=picture[3])


if __name__ == '__main__':
    app.run(debug=True)
