from flask import Flask, render_template, redirect, request, abort
from flask_restful import Api
from data import db_session
from data.users import User
from forms.user import RegisterForm
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from loginform import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api()
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    db_session.global_init('test.db')
    session = db_session.create_session()
    users = session.query(User).all()
    names = {}
    for name in users:
        names[name.id] = (name.surname, name.name)
    return render_template("index.html", names=names)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/news')
def news():
    return render_template("news.html")


@app.route('/req')
def req():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        """
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            email=form.email.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
    """
    return render_template("req.html", form=form)


@app.route('/cabinet')
def cabinet():
    return render_template("cabinet.html")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            email=form.email.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


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


'''
@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    form = JobsForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('addjob.html',
                           title='Добавление работы',
                           form=form,
                           message='Проверьте корректность заполнения полей')


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(ids):
    form = JobsForm()
    if form.validate_on_submit():
        pass
    return render_template('addjobs.html', title='Редактирование новости', form=form)
'''


def main():
    db_session.global_init("db/mars_explorer_.db")

    app.run()


if __name__ == '__main__':
    main()
