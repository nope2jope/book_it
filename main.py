from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book-collection.db'
# spares some pesky console messages
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# applies sqlalchemy class to flask app (enables easy database interaction)
db = SQLAlchemy(app)


# model class allows for quick templating of database entries
class Book(db.Model):
    # ids autogenerate unless otherwise specified
    # nullable = false to necessitate input
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)


# if database doesn't exist, create it
if not os.path.exists('my_folder'):
    db.create_all()

# references library in database
all_books = db.session.query(Book).all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()

    # if statement in index.html checks to see if library is empty
    total = len(all_books)

    return render_template('index.html', library=all_books, total=total)


# this route never displays in browswer window thanks to the redirect
# needs variables passed to the route and function though
@app.route('/delete/<int:id>')
def delete(id):
    target_book = Book.query.get(id)
    db.session.delete(target_book)
    db.session.commit()

    return redirect(url_for('home'))


@app.route("/add", methods=['GET', 'POST'])
def add():
    all_books = db.session.query(Book).all()
    if request.method == 'POST':
        # generates book according to model class, pulling from the named form fields
        new_book = Book(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    # this code runs upon landing at page (i.e. 'get')
    return render_template('add.html', list=all_books)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        # variable not passed to function but instead reached through request.form
        new_rating = request.form['new-rating']
        to_update = Book.query.get(id)
        to_update.rating = new_rating
        db.session.commit()

        return redirect(url_for('home'))

    # request.get portion, as w/ add()
    book = Book.query.get(id)
    return render_template('edit.html', book=book)


if __name__ == "__main__":
    app.run(debug=True)
