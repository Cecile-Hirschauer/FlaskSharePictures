import sqlite3


DATABASE = 'app.db'
db = sqlite3.connect(DATABASE)

cursor = db.cursor()

# Creation of table "users".
# If it existed already, we delete the table and create a new one
# cursor.execute('DROP TABLE IF EXISTS users')
# cursor.execute(""" CREATE TABLE users
#                (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                login VARCHAR(250) NOT NULL,
#                password VARCHAR(250) NOT NULL)""")

# Creation of table "categories".
# If it existed already, we delete the table and create a new one
cursor.execute('DROP TABLE IF EXISTS categories')
cursor.execute("""CREATE TABLE categories
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL)""")

# We seed the table with initial values.
# Here we insert categories: "Sport", "Artistique", "Gaming", "Animé", "Film"
for name in ["Sport", "Artistique", "Gaming", "Animé", "Film"]:
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))

# Creation of table "pictures"
cursor.execute("DROP TABLE IF EXISTS pictures")
cursor.execute("""CREATE TABLE pictures
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                path VARCHAR(250),
                title VARCHAR(200),
                description VARCHAR(200),
                creation_date datetime default (datetime(current_timestamp)),
                category_id INTEGER,
                CONSTRAINT fk_categories
                FOREIGN KEY (category_id)
                REFERENCES categories(category_id))""")

# creation table "comments"
cursor.execute("DROP TABLE IF EXISTS comments")
cursor.execute("""CREATE TABLE comments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment VARCHAR(255),
                picture_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                date_published datetime default (datetime(current_timestamp)),
                CONSTRAINT fk_pictures
                FOREIGN KEY (picture_id)
                REFERENCES pictures(picture_id))""")



# We save our changes into the database file
db.commit()

# We close the connection to the database
db.close()
