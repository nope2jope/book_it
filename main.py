from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()

all_books = db.session.query(Book).all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    total = len(all_books)

    return render_template('index.html', library=all_books, total=total)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Book(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html', list=all_books)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        new_rating = request.form['new-rating']
        to_update = Book.query.get(id)
        print(to_update)
        to_update.rating = new_rating
        db.session.commit()

        return redirect(url_for('home'))

    book = Book.query.get(id)
    return render_template('edit.html', book=book)




if __name__ == "__main__":
    app.run(debug=True)

