from flask import jsonify
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash
from data import db_session
from .parser_user import parser
from data.users import User


def abort_user_not_found(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        abort(404, message=f'User с указанным id не найден')
    return


def set_password(password):
    return generate_password_hash(password)


class UsersResource(Resource):
    def get(self, user_id):
        abort_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        return jsonify({'user': user.to_dict(only=('name', 'surname', 'age', 'position', 'speciality',
                                                   'address', 'email', 'hasged_password'))})

    def delete(self, user_id):
        abort_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)

        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'Удаление прошло успешно'})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({'users': [item.to_dict(only=('name', 'surname', 'age', 'position', 'speciality',
                                                     'address', 'email', 'hasged_password')) for item in users]})

    def post(self):
        db_sess = db_session.create_session()
        arg = parser.parse_args()
        user = User(name=arg['name'], surname=arg['surname'], age=arg['age'], position=arg['position'],
                    speciality=arg['speciality'], address=arg['address'], email=arg['email'],
                    hashed_password=set_password(arg['hashed_password']))
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'Новый пользователь добавлен'})
