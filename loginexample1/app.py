from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.login import LoginManager
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#creating app instance of flask
app = Flask(__name__)
#defining sql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userss.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#need a secret key for user session authentication
app.config['SECRET_KEY'] = 'thisissecret'

#initialize the database
db = SQLAlchemy(app)
#create a required loginmanager class and object
login_manager = LoginManager()
#configure application object for login
login_manager.init_app(app)

#create a user class acting as db model for users table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)

#callback is used to reload the user object from the 
# user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    user = User.query.filter_by(username='joss').first()
    login_user(user)
    return 'logged in woo'

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return 'you are now logged out'

@app.route("/home")
@login_required
def home():
    return 'The current user is definitely' + current_user.username

if __name__ == '__main__':
    app.run(debug=True)

