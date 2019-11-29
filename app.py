from datetime import datetime

from flask import Flask
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config.update(
    SECRET_KEY='Bigdata123',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:Bigdata123@localhost:5433/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)


@app.route('/index')
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/new/')
def query_strings(greeting='hello'):
    query_val = request.args.get('greeting', greeting)
    return "<h1>The greeting is: {0}</h1>".format(query_val)


@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='KitKat'):
    return "<h1>The greeting is: {0}</h1>".format(name)


# strings
@app.route('/text/<string:name>')
def working_with_strings(name):
    return '<h1>here is the string: ' + name + '</h1>'


# strings
@app.route('/numbers/<int:num>')
def working_with_numbers(num):
    return '<h1>here is the number: ' + str(num) + '</h1>'


# addition
@app.route('/add/<int:num1>/<int:num2>')
def addition(num1, num2):
    return '<h1> Sum of two numbers {}'.format(num1 + num2) + '</h1>'


# product
@app.route('/product/<float:num1>/<float:num2>')
def product_of_two_numbers(num1, num2):
    return '<h1> Product of two numbers {}'.format(num1 * num2) + '</h1>'


# render html template
@app.route('/temp')
def func_using_template():
    return render_template('hello.html')


# using jinja2 templates
@app.route('/watch')
def top_movies():
    movie_list = ['John Wick 1', 'John Wick 2', 'John Wick 3', 'Pulp Fiction', 'How to Train your Dragon']
    return render_template('movies.html', movies=movie_list, name='John')


# with HTML tables
@app.route('/tables')
def movie_collection_tbl():
    movies_dict = {'John Wick 1': 1.50,
                   'John Wick 2': 2.20,
                   'John Wick 3': 2.17,
                   'Pulp Fiction': 1.47,
                   'How to Train your Dragon': 3.34}

    return render_template('table_data.html', movies=movies_dict, name='Helen')


# with jinja2 filter
@app.route('/filters')
def filter_data():
    movies_dict = {'John Wick 1': 1.50,
                   'John Wick 2': 2.20,
                   'John Wick 3': 2.17,
                   'Pulp Fiction': 1.47,
                   'How to Train your Dragon': 3.34,
                   'Ghost In a Shell': 2.5}

    return render_template('filter_data.html', movies=movies_dict,
                           name='Helen', film='a christmas carol')


# jinja2 macros
@app.route('/macros')
def jinja_macros():
    movies_dict = {'John Wick 1': 1.50,
                   'John Wick 2': 2.20,
                   'John Wick 3': 2.17,
                   'Pulp Fiction': 1.47,
                   'How to Train your Dragon': 3.34,
                   'Ghost In a Shell': 2.5}

    return render_template('using_macros.html', movies=movies_dict)


class Publication(db.Model):
    __tablename__ = 'publication'

    pub_id = db.Column(db.Integer, primary_key=True)
    pub_name = db.Column(db.String(80), nullable=False)

    def __init_(self, pub_name):
        self.pub_name = pub_name

    def __repr__(self):
        return 'The Publisher is {}'.format(self.pub_name)


class Book(db.Model):
    __tablename__ = 'book'

    bk_id = db.Column(db.Integer, primary_key=True)
    bk_title = db.Column(db.String(500), nullable=False, index=True)
    bk_author = db.Column(db.String(350))
    bk_avg_rating = db.Column(db.Float)
    bk_format = db.Column(db.String(50))
    bk_image = db.Column(db.String(100), unique=True)
    bk_num_pages = db.Column(db.Integer)
    bk_pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # Relationship
    bk_pub_id = db.Column(db.Integer, db.ForeignKey('publication.pub_id'))

    def __init__(self, bk_title, bk_author, bk_avg_rating, bk_format,
                 bk_image, bk_num_pages, bk_pub_id):

        self.bk_author = bk_author
        self.bk_avg_rating = bk_avg_rating
        self.bk_format = bk_format
        self.bk_image = bk_image
        self.bk_num_pages = bk_num_pages
        self.bk_title = bk_title
        self.bk_pub_id = bk_pub_id

    def __repr__(self):
        return '{} by {}'.format(self.bk_title, self.bk_author)

if __name__ == '__main__':
    db.create_all()
    app.run()
