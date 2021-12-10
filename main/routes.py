from flask import render_template, url_for, flash, redirect, request
from main import app, db, bcrypt
from main.forms import RegistrationForm, LoginForm, UpdateAccForm, SearchStockForm
from main.models import User, Stock, Stockprice
from flask_login import login_user, current_user, logout_user, login_required
from polygon import RESTClient
from datetime import date


# insert new user to database
def add_new_user(user):
    db.session.add(user)
    db.session.commit()
    return


@app.route("/")
@app.route("/home")
def home():
    stocks = Stockprice.query.all()
    return render_template('home.html', stocks=stocks)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


# check register from and add new user
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        add_new_user(user)
        flash(f'Your account has created , You are now able to log in !', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)


#check user mail and passoword from db and hash password
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'logged in Unsuccessful.check email and password  !', 'danger')
    return render_template('login.html', title='login', form=form)


#log out and clear current user
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


#manage user and update fields on his account
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.date_birth = form.date_birth.data
        current_user.company = form.company.data
        db.session.commit()
        flash('your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.date_birth.data = current_user.date_birth
        form.company.data = current_user.company
    return render_template('account.html', title='account', form=form)

#with bug
#search stock and post the price ,
# user Can add the stock to his account
# polygon web , get api connect to nasdaq
# get open/close price of stock
@app.route("/stock/search", methods=['GET', 'POST'])
@login_required
def search_stock():
    form = SearchStockForm()
    if form.validate_on_submit():
        flash('Your Stock', 'success')
        return redirect(url_for('search_stock'))
    elif request.method == 'GET':
        if form.symbol.data != ' ' :
            current_date = date.today()
            key = "E2cEl11rM5MB0WqSKP8QDACoHkiCUZWj"
            with RESTClient(key) as client:
                resp = client.stocks_equities_daily_open_close("AAPL", "2021-12-07")
            form.stockdate.data = resp.from_
            form.stockopen.data = resp.open
            form.stockclose.data = resp.close
    return render_template('search_stock.html', title='Search stock', form=form)
