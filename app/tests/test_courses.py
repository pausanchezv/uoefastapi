import json
from starlette import status
from app.main import app


class TestApps:

    def setup(self):
        pass

    def test_get_course(self, client):
        response = client.post(
            app.url_path_for('create_course'),
            json={"name": "FCE", "level": "B2", "description": "desc", "background_color": "bg"},
        )

        response_data = json.loads(response.content)
        assert response.status_code == status.HTTP_201_CREATED

        response = client.get(app.url_path_for('get_course', **{"course_id": 1}))
        response_data = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        print(response_data)
        #assert response.json() == {'FastApi': 'UOE PRO'}


class TestApps2:

    def setup(self):
        pass

    def test_get_course2(self, client):
        response = client.post(
            app.url_path_for('create_course'),
            json={"name": "FCE", "level": "B2", "description": "desc", "background_color": "bg"},
        )

        response_data = json.loads(response.content)
        assert response.status_code == status.HTTP_201_CREATED

        response = client.get(app.url_path_for('get_course', **{"course_id": 1}))
        response_data = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        print(response_data)
        #assert response.json() == {'FastApi': 'UOE PRO'}
