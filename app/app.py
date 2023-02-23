import re
from flask import Flask, request, jsonify
from flask.views import MethodView
from db import User, Session, Advertisement
from errors import HttpError
from schema import validate_create_user, validate_create_advertisement
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

app = Flask('app')
bcrypt = Bcrypt(app)


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error', 'description': error.message})
    http_response.status_code = error.status_code
    return http_response

def get_user(user_id: int, sesion: Session):
    user = sesion.query(User).get(user_id)
    if user is None:
        raise HttpError(404, f'User id={user_id} not found')
    return user

def get_advertisement(adv_id: int, sesion: Session):
    adv = sesion.query(Advertisement).get(adv_id)
    if adv is None:
        raise HttpError(404, f'advertisement id={adv_id} not found')
    return adv



def hello():
    json_data = request.json
    headers = request.headers
    qs = request.args
    print(f'{json_data=}')
    print(f'{headers=}')
    print(f'{qs=}')
    return jsonify({'hello': 'world'})
app.add_url_rule('/hello', view_func=hello, methods=['POST'])


class AdvertisementView(MethodView):

    def get(self, adv_id: int):
        with Session() as sesion:
            adv = get_advertisement(adv_id, sesion)
            return jsonify({
                'id': adv.id,
                'title': adv.title,
                'description': adv.description,
                'creation_time': adv.creation_time,
                'user_id': adv.id_user,
                'user_name': adv.user.username
            })

    def post(self):
        json_data = validate_create_advertisement(request.json)
        with Session() as session:
            new_post = Advertisement(**json_data)
            session.add(new_post)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, f"user with id={json_data['id_user']} not found")
            return jsonify({
                'id':new_post.id,
                'title': new_post.title,
                'create_time': new_post.creation_time.isoformat(),
                'id_user': new_post.id_user,
                'username':new_post.user.username

            })

    def patch(self,adv_id: int):
        json_data = request.json
        with Session() as session:
            post = get_advertisement(adv_id, session)
            for fild, value in json_data.items():
                setattr(post, fild, value)
            session.add(post)
            session.commit()
        return jsonify({'status': 'ok'})

    def delete(self, adv_id):
        with Session() as session:
            post = get_advertisement(adv_id, session)
            session.delete(post)
            session.commit()
        return jsonify({'status': 'ok'})

class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            return jsonify({
                'id': user.id,
                'name': user.username,
                'creation_time': user.creation_time,
                'password':user.password,
                'post': [{'id':k.id, 'title': k.title} for k in user.advertisements]
            })



    def post(self):
        json_data = validate_create_user(request.json)
        password:   str= json_data['password']
        password: bytes = password.encode()
        password: bytes = bcrypt.generate_password_hash(password)
        password: str = password.decode()
        json_data['password'] = password
        with Session() as session:
            new_user = User(**json_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'User already exist')
            return jsonify({
                'id': new_user.id,
                'creat_time': (new_user.creation_time.isoformat()),
                'password': new_user.password
            })

    def patch(self, user_id: int):
        json_data = request.json
        print(json_data)
        with Session() as session:
            user = get_user(user_id, session)
            for fild, value in json_data.items():
                setattr(user, fild, value)
            session.add(user)
            session.commit()
        return jsonify({'status':'ok'})


    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()
        return jsonify({'status':'ok'})



app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('users_with_id'),
                 methods=['GET', "PATCH", 'DELETE'])
app.add_url_rule('/users/', view_func=UserView.as_view('users'), methods=['POST'])
app.add_url_rule('/adv/<int:adv_id>', view_func=AdvertisementView.as_view('adv_with_id'),
                 methods=['GET', "PATCH", 'DELETE'])
app.add_url_rule('/adv/', view_func=AdvertisementView.as_view('adv'), methods=['POST'])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

# app.run(host='0.0.0.0', port=5000)