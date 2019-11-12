from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# setup and config flask app
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# config SQLAlchemy
db = SQLAlchemy(app)

# defining models:
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    lead = db.Column(db.String(400), nullable = False)
    body = db.Column(db.String, nullable = False)
    author = db.Column(db.String(100), nullable = False)
    created = db.Column(db.DateTime, server_default = db.func.now())
    updated = db.Column(db.DateTime, server_default = db.func.now(), server_onupdate = db.func.now())

class User():

db.create_all()

@app.route('/login', methods = ['GET, 'POST'])
def login():


@app.route('/', methods=['GET'])
def postfeed():
    posts = Blog.query.all()
    return render_template("views/home.html", posts = posts)

@app.route('/blogs', methods=['GET', 'POST'])
def create_post():
    if request.method == "POST":
        new_blog = Blog(title = request.form['title'],
                        lead = request.form['lead'],
                        body = request.form['body'],
                        author = request.form['author'])
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('postfeed'))

    return render_template("views/post.html")

@app.route('/blogs/<id>', methods=['GET','POST'])
def delete_entry(id):
    if request.method == "POST" :
        post = Blog.query.filter_by(id = id).first()
        if not post:
            return "CAN'T NOT FIND YOUR POST"
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('postfeed'))
    return "404"

@app.route('/about', methods=["GET"])
def about():
    return render_template("views/about.html")


if __name__ == "__main__":
    app.run(debug = True)