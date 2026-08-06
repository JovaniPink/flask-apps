from app import create_app
from models import User, db


def test_health_and_database_contract():
    app = create_app()

    with app.app_context():
        db.create_all()
        db.session.add(User(username='tester', email='tester@example.com'))
        db.session.commit()
        assert db.session.scalar(db.select(User.username)) == 'tester'

    client = app.test_client()
    assert client.get('/').text == 'Hello, World!'
    assert client.get('/healthz').get_json() == {'status': 'ok'}


def test_celery_task_runs_eagerly():
    app = create_app()
    response = app.test_client().post('/api/process_data')

    assert response.status_code == 200
    task_id = response.get_json()['task_id']
    status_response = app.test_client().get(f'/api/tasks/{task_id}')
    assert status_response.get_json() == {'status': 'processed'}
