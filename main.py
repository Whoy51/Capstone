from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import sqlite3

con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS user(id, studentid, name, teacher, timesAttended)")
con.commit()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'arandomstring'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.String(15), unique=True)
    name = db.Column(db.String(16))
    teacher = db.Column(db.String(15))
    timesAttended = db.Column(db.Integer)


class RegisterForm(FlaskForm):
    studentid = StringField('studentid', validators=[InputRequired(), Length(min=7, max=7)])
    name = StringField('name', validators=[InputRequired(), Length(min=5, max=16)])
    teacher = SelectField('teacher', choices=[('Unselected', 'Unselected'),
                                              ('Mr. Jacoby', 'Mr. Jacoby'), ('Ms. Guo', 'Ms. Guo'),
                                              ('Mr Coster', 'Mr. Coster')])
    submit = SubmitField('Sign Up')

    def validate_studentid(self, studentid):
        user = User.query.filter_by(studentid=studentid.data).first()
        if user:
            raise ValidationError('That studentid is already. Please login.')




class LoginForm(FlaskForm):
    studentid = StringField('studentid', validators=[InputRequired(), Length(min=7, max=7)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')


password = "thisistodayspassword"


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(studentid=form.studentid.data).first()
        if user:
            if user.password.data == password:
                login_user(user)
                return redirect(url_for('student'))
        return render_template('index.html', form=form, error="Invalid studentid or password")
    return render_template('index.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(studentid=form.studentid.data, name=form.name.data, teacher=form.teacher.data, timesAttended=0)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/admin')

def admin():
    return render_template('admin.html')


@app.route('/student')
@login_required
def student():
    return render_template('student.html', timesAttended=current_user.timesAttended)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(port=5000, debug=False)
