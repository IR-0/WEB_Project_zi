from flask import Flask, render_template, redirect, request, abort
from flask_restful import Api
from data import db_session
from data.users import User
from data.news import News
from data.requ import Requ
from data.autos import Autos
from forms.user import RegisterForm
from forms.new import NewsForm
from forms.req import RequForm
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from loginform import LoginForm
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api()
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/news')
def news():
    form = NewsForm()
    db_sess = db_session.create_session()
    paper = db_sess.query(News).all()  # ВОЗВРАЩАЕТ СПИСОК КЛАССОВ НЬЮС
    print(paper[0].title, '=========================================================================================')
    return render_template("news.html", form=form, paper=paper)


@app.route('/req')
def req():
    return render_template("req.html")


@app.route('/autos')
def autos():
    return render_template("autos.html")


@app.route('/cabinet')
def cabinet():
    return render_template("cabinet.html")
# ================================================================USER==============================================


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    print(0)
    if form.is_submitted():
        print(2)
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="Адресс электронной почты уже используется")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
            type=-1,
            other=0
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    print('no')
    return render_template('register.html', title='Регистрация', form=form)


# ============================================================================REQUEST==================================
@app.route('/requ',  methods=['GET', 'POST'])
@login_required
def add_requ():
    form = RequForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        requ = Requ()
        requ.title = form.title.data
        requ.content = form.content.data
        requ.data_on = datetime.date.today()
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('requ.html', title='Добавление заказа',
                           form=form)


@app.route('/requ/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_requ(id):
    form = RequForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        requ = db_sess.query(Requ).filter(Requ.id == id,
                                          Requ.id_for == current_user.id
                                          ).first()
        if requ:
            form.title.data = requ.title
            form.content.data = requ.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        requ = db_sess.query(Requ).filter(Requ.id == id,
                                          Requ.id_for == current_user.id
                                          ).first()
        if requ:
            requ.title = form.title.data
            requ.content = form.content.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('requ.html',
                           title='Редактирование заказа',
                           form=form
                           )


@app.route('/requ_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def requ_delete(id):
    db_sess = db_session.create_session()
    requ = db_sess.query(Requ).filter(Requ.id == id,
                                      Requ.id_for == current_user.id
                                      ).first()
    if requ:
        db_sess.delete(requ)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


# ==========================================================================NEWS========================================
@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        db_sess.add(news)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.id_whom == current_user.id
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.id_whom == current_user.id
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.id_whom == current_user.id
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


# ===========================================================================ГЛАВНАЯ-ПРОГРАММА================================
def main():
    db_session.global_init("db/test.db")

    app.run()


if __name__ == '__main__':
    main()
