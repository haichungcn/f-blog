from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# setup and config flask app
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'my secret key'


# config SQLAlchemy
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# defining models:
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    lead = db.Column(db.String(400), nullable = False)
    body = db.Column(db.String, nullable = False)
    author = db.Column(db.String(100), nullable = False)
    created = db.Column(db.DateTime, server_default = db.func.now())
    updated = db.Column(db.DateTime, server_default = db.func.now(), server_onupdate = db.func.now())

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), nullable = False, unique = True)
    username = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String, nullable = False)

    def generate_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email = request.form['email']).first()
        if not user:
            flash("USER NOT FOUND", 'danger')
            return redirect(url_for('login'))
            
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash("WELCOME BACK {0}".format(current_user.username), 'success')
            return redirect(url_for("postfeed"))
        
        flash("INVALID PASSWORD", 'warning')
        return redirect(url_for('login'))

    return render_template("views/loginForm.html")

@app.route('/createuser', methods=['GET', 'POST'])
def create_user():
    if request.method == "POST":
        user = User.query.filter_by(email = request.form['email']).first()
        if not user:
            new_user = User(email = request.form['email'], username = request.form['username'])
            new_user.generate_password(request.form['password'])
            db.session.add(new_user)
            db.session.commit()
            flash("SUCCESSFULLY CREATED USER {0}".format(newuser.username), 'success')
            return redirect(url_for('postfeed'))
        return redirect(url_for("postfeed"))
    return render_template("views/createUserForm.html")

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