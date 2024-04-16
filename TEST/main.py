import sqlalchemy
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
KONTAKTS = {}
USER = None


@app.route("/")
def index():
    global USER
    USER = int(str(current_user).split(' ')[1])  # КОСТЫЛЬ НА КОТОРОМ ДЕРЖИТСЯ ВСЕЛЕННАЯ
    return render_template("index.html",
                           kont=KONTAKTS.items())


@app.route('/news/<int:count>')
def news(count):
    form = NewsForm()
    db_sess = db_session.create_session()
    par = db_sess.query(News).filter(10 * count < News.id, News.id < 10 * (count + 1)).all()  # ВОЗВРАЩАЕТ СПИСОК 10и КЛАССОВ НЬЮС
    return render_template("news.html",
                           form=form,
                           paper=par,
                           count=count,
                           kodon=(len(par) == 9))


@app.route('/req')
def req():
    form = RequForm()
    return render_template("req.html",
                           form=form,
                           kont=KONTAKTS.items())


@app.route('/autos/<int:count>')
def autos(count):
    db_sess = db_session.create_session()
    listt = db_sess.query(Autos).filter(10 * count < Autos.id, Autos.id < 10 * (count + 1)).all()
    if listt:
        return render_template("autos.html",
                               listt=listt,
                               count=count,
                               kodon=(len(listt) == 9))


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
            return redirect('/cabinet')
        return render_template('login.html',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('login.html',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    print(0)
    if form.is_submitted():
        print(2)
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Register',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Register',
                                   form=form,
                                   message="Адресс электронной почты уже используется")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
            type=-1,
            other='nomer:NaN contakt:NaN image:NaN'
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/cabinet')
    print('no')
    return render_template('register.html',
                           title='Регистрация',
                           form=form)


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
    return render_template('requ.html',
                           title='Добавление заказа',
                           form=form)


@app.route('/requ/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_requ(id):
    form = RequForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        requ = db_sess.query(Requ).filter(Requ.id == id,
                                          Requ.id_for == USER
                                          ).first()
        if requ:
            form.title.data = requ.title
            form.content.data = requ.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        requ = db_sess.query(Requ).filter(Requ.id == id,
                                          Requ.id_for == USER
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
                                      Requ.id_for == USER
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
        news.id_whom = USER
        db_sess.add(news)
        db_sess.commit()
        return redirect('/news/0')
    return render_template('news.html',
                           title='Добавление новости',
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.id_whom == USER
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.id_whom == USER
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
                                      News.id_whom == USER
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


# ===========================================================================ГЛАВНАЯ-ПРОГРАММА================================
def main():
    global KONTAKTS
    db_session.global_init("db/test.db")

    sess = db_session.create_session()
    nomers = sess.query(User).filter(User.type == 0).all()
    ''' User.other имеет вид около-csv строки, где разделитель пробел: 
      [0]                          [1]                        [2]
    "nomer:<автомобильный номер> contakt:<телефонный номер> image:<путь>" '''
    for nomer in nomers:
        vdrug = nomer.other.split(' ')[1]  # разбиение информации на части, взятие телефонного номера
        KONTAKTS[nomer.name + ' ' + nomer.surname] = vdrug[vdrug.index(':') + 1:]

    app.run()


if __name__ == '__main__':
    main()
