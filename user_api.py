import flask
import db_session
from users import User
from jobs import Jobs
from departments import Department
from flask import request, jsonify

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name',
                                    'age', 'position', 'speciality',
                                    'address', 'email', 'hashed_password', 'modified_date'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:users_id>', methods=['GET'])
def get_one_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict(only=('id', 'surname', 'name',
                                         'age', 'position', 'speciality',
                                         'address', 'email', 'hashed_password', 'modified_date'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name',
                  'age', 'position', 'speciality',
                  'address', 'email', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    users = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email']
    )
    users.set_password(request.json['hashed_password'])
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    if db_sess.query(Jobs).filter((Jobs.user_add == users_id) | (Jobs.team_leader == users_id)).first():
        return jsonify({'error': 'Пользователю принадлежат работы или он team_leader'})
    if db_sess.query(Department).filter(Department.chief == users_id).first():
        return jsonify({'error': 'Пользователю принадлежат Департаменты'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/editing/<int:users_id>', methods=['POST'])
def editing_users(users_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name',
                  'age', 'position', 'speciality',
                  'address', 'email', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    users_ed = db_sess.query(User).filter(users_id == User.id).first()
    if users_ed:
        db_sess.delete(users_ed)
        users = User(
            surname=request.json['surname'],
            name=request.json['name'],
            age=request.json['age'],
            position=request.json['position'],
            speciality=request.json['speciality'],
            address=request.json['address'],
            email=request.json['email']
        )
        users.set_password(request.json['hashed_password'])
        db_sess.add(users)
        db_sess.commit()
    else:
        return jsonify({'success': 'NO Id'})
    return jsonify({'success': 'OK'})
