import tests.user.factories


class TestUser:
    def test_get_user(self, database, client):
        user = tests.user.factories.UserFactory.create()
        database.session.commit()

        response = client.get('/users/{id}'.format(id=user.id))

        assert response.get_json() == user.to_dict()
