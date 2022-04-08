import flask

import db_session
from jobs import Jobs
from flask import request, jsonify
import datetime

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('team_leader.name', 'user_add', 'job',
                                    'work_size', 'collaborators', 'start_date',
                                    'end_date', 'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('team_leader.name', 'user_add', 'job',
                                       'work_size', 'collaborators', 'start_date',
                                       'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'user_add', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    jobs = Jobs(
        team_leader=request.json['team_leader'],
        user_add=request.json['user_add'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=datetime.date(*request.json['start_date']),
        end_date=datetime.date(*request.json['end_date']),
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/editing/<int:jobs_id>', methods=['POST'])
def editing_jobs(jobs_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'user_add', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    jobs_ed = db_sess.query(Jobs).filter(jobs_id == Jobs.id).first()
    if jobs_ed:
        db_sess.delete(jobs_ed)
        jobs = Jobs(
            id=jobs_id,
            team_leader=request.json['team_leader'],
            user_add=request.json['user_add'],
            job=request.json['job'],
            work_size=request.json['work_size'],
            collaborators=request.json['collaborators'],
            start_date=datetime.date(*request.json['start_date']),
            end_date=datetime.date(*request.json['end_date']),
            is_finished=request.json['is_finished']
        )
        db_sess.add(jobs)
        db_sess.commit()
    else:
        return jsonify({'success': 'NO Id'})
    return jsonify({'success': 'OK'})

