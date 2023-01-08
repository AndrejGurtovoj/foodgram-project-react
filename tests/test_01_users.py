from django.urls import reverse

import pytest

from .common import check_attributes, check_pagination_fields, reverse_query


class Test01UserAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_users_not_authenticated(self, client):
        url = reverse('api:user-list')
        response = client.get(url)
        assert response.status_code != 404, (
            f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
        )

        code = 200
        assert response.status_code == code, (
            f'Проверьте, что при GET запросе `{url}` без токена авторизации возвращается статус {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_users_id_not_authenticated(self, client, user):
        url = reverse('api:user-detail', kwargs={'id': user.id})
        response = client.get(url)
        assert response.status_code != 404, (
            f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
        )

        code = 401
        assert response.status_code == code, (
            f'Проверьте, что при GET запросе `{url}` без токена авторизации возвращается статус {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_users_me_not_authenticated(self, client):
        url = reverse('api:user-me')
        response = client.get(url)
        assert response.status_code != 404, (
            f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
        )

        code = 401
        assert response.status_code == code, (
            f'Проверьте, что при GET запросе `{url}` без токена авторизации возвращается статус {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_users_get_anon(self, client, authors):
        url = reverse('api:user-list')
        response = client.get(url)
        assert response.status_code != 404, (
            f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
        )

        code = 200
        assert response.status_code == code, (
            f'Проверьте, что при GET запросе `{url}` для неавторизованного пользователя возвращается статус {code}'
        )

        data = response.json()
        check_pagination_fields(data, len(authors), url)

        fields = {
            'email': (None, True),
            'id': (None, True),
            'username': (None, True),
            'first_name': (None, True),
            'last_name': (None, True),
            'is_subscribed': (False, True),
        }
        for user, result in zip(authors, data['results']):
            check_attributes(user, result, fields, url, data_name='results')

    @pytest.mark.django_db(transaction=True)
    def test_05_users_get_auth(self, user_client):
        url = reverse('api:user-list')
        response = user_client.get(url)
        assert response.status_code != 404, (
            f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
        )

        code = 200
        assert response.status_code == code, (
            f'Проверьте, что при GET запросе `{url}` для авторизованного пользователя возвращается статус {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_06_users_get_me(self, client, user_client):
        url = reverse('api:user-me')
        response = client.get(url)
        assert response.status_code != 404, (
            f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
        )

        code = 401
        assert response.status_code == code, (
            f'Проверьте, что при GET запросе `{url}` для неавторизованного пользователя возвращается статус {code}'
        )
        response = user_client.get(url)
        code = 200
        assert response.status_code == code, (
            f'Проверьте, что при GET запросе `{url}` для авторизованного пользователя возвращается статус {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_07_users_get_with_page_limit(self, client, recipes):
        for limit in range(1, len(recipes) + 1):
            url = reverse_query('api:user-list', query_kwargs={'limit': limit})
            response = client.get(url)
            assert response.status_code != 404, (
                f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
            )

            data = response.json()
            check_pagination_fields(data, len(recipes), url, results_count=limit)
