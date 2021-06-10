
from starlette import status

from app.core import settings
from app.main import app


def get_settings_override():
    return settings.Settings(
        app_name="Use of English Pro Settings",
        admin_email="testing_admin@example.com"
    )


app.dependency_overrides[settings.get_settings] = get_settings_override


class TestMain:

    def test_read_main(self, client):
        response = client.get(app.url_path_for('main'))
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'FastApi': 'UOE PRO'}

    def test_app(self, client):
        response = client.get("/info")
        data = response.json()
        assert data == {
            "app_name": "Use of English Pro Settings",
            "admin_email": "testing_admin@example.com"
        }
