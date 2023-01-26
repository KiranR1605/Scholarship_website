from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'scholarship_project'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///scholarship.db'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'home_page'

from Student_Scholarship_Portal.models import User, Applicant, Bank, Current_education, Education,Scholarship , Queries

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id = id).first()

from Student_Scholarship_Portal import routes