from flask import Flask, url_for, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort

from data.loginform import LoginForm
from data.register_form import RegisterForm
from data.review import Review
from data.brands import Brands
from data.reviewform import ReviewForm

from data import db_session

from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'auto_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def auto():
    session = db_session.create_session()
    reviews = session.query(Review).all()
    return render_template("index.html", reviews=reviews)


# добавить отзыв
@app.route('/review', methods=['GET', 'POST'])
@login_required
def add_review():
    session = db_session.create_session()
    form = ReviewForm()
    form.brand.choices = [(x.id, x.name) for x in session.query(Brands).order_by(Brands.name.asc())]
    if form.validate_on_submit():
        reviews = Review()
        reviews.brand_id = form.brand.data
        reviews.model = form.model.data
        reviews.text = form.text.data
        current_user.reviews.append(reviews)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('review.html', title='Добавление записи',
                           form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    db_session.global_init("db/auto.sqlite")
    app.run(port=8000, host='127.0.0.1', debug=True)
