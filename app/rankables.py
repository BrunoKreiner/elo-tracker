from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.rankables import Rankables


from flask import Blueprint
bp = Blueprint('rankables', __name__)


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Rankables.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('rankables.login'))
        
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home.home')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    about = StringField(_l('About'), validators=[DataRequired()])
    category = SelectField('Category', choices=[('People', 'People'), ('Restaurant', 'Restaurant'), ('School','School')])
    submit = SubmitField(_l('Register'))

    def validate_email(self, email):
        if Rankables.email_exists(email.data):
            raise ValidationError(_('Already a user with this email.'))

class UpdateEmailForm(FlaskForm):
    email = StringField(_l('New Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Confirm'))

    def validate_email(self, email):
        if Rankables.email_exists(email.data):
            raise ValidationError(_('Already a user with this email.'))

class UpdateAboutForm(FlaskForm):
    about = StringField(_l('New About'), validators=[DataRequired()])
    submit = SubmitField(_l('Confirm'))

class UpdateCategoryForm(FlaskForm):
    category = SelectField('Category', choices=[('People', 'People'), ('Restaurant', 'Restaurant'), ('School','School')])
    submit = SubmitField(_l('Confirm'))

class UpdateNameForm(FlaskForm):
    name = StringField(_l('New Name'), validators=[DataRequired()])
    submit = SubmitField(_l('Confirm'))

class UpdatePasswordForm(FlaskForm):
    password = PasswordField(_l('New Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat New Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Confirm'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    print("test")
    if form.validate_on_submit():
        print("test2")
        if Rankables.register(form.email.data,
                         form.password.data,
                         form.name.data,
                         form.category.data,
                         form.about.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('rankables.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/updateEmail', methods=['GET', 'POST'])
def updateEmail():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    form = UpdateEmailForm()
    if form.validate_on_submit():
            if Rankables.updateEmail(current_user.rankable_id, form.email.data):
                return redirect(url_for('home.home'))
    return render_template('updateEmail.html', form=form)

@bp.route('/updateName', methods=['GET', 'POST'])
def updateName():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    form = UpdateNameForm()
    if form.validate_on_submit():
            if Rankables.updateName(current_user.rankable_id, form.name.data):
                return redirect(url_for('home.home'))
    return render_template('updateName.html', form=form)

@bp.route('/updateCategory', methods=['GET', 'POST'])
def updateCategory():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    form = UpdateCategoryForm()
    if form.validate_on_submit():
            if Rankables.updateCategory(current_user.rankable_id, form.category.data):
                return redirect(url_for('home.home'))
    return render_template('updateCategory.html', form=form)

@bp.route('/updateAbout', methods=['GET', 'POST'])
def updateAbout():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    form = UpdateAboutForm()
    if form.validate_on_submit():
            if Rankables.updateAbout(current_user.rankable_id, form.about.data):
                return redirect(url_for('home.home'))
    return render_template('updateAbout.html', form=form)

@bp.route('/updatePassword', methods=['GET', 'POST'])
def updatePassword():
    if not current_user.is_authenticated:
        return redirect(url_for('rankables.login'))
    form = UpdatePasswordForm()
    if form.validate_on_submit():
            if Rankables.updatePassword(current_user.rankable_id, form.password.data):
                return redirect(url_for('home.home'))
    return render_template('updatePassword.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('rankables.login'))
