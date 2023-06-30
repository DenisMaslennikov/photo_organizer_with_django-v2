import pytest
from pytest_lazyfixture import lazy_fixture

from django.urls import reverse

from conftest import LIST_VIEW_ENDPOINTS

ADD_IMAGE_ENDPOINT = reverse('gallery:add_image')
UPDATE_IMAGE_ENDPOINT = lazy_fixture('get_image_update_url')

@pytest.mark.django_db
@pytest.mark.parametrize(
    'active_client, result', [
        (lazy_fixture('user_client'), True),
        (lazy_fixture('unlogged_client'), False),
    ]
)
@pytest.mark.parametrize(
    'endpoint', [ADD_IMAGE_ENDPOINT, ]
)
def test_add_image(
        image_model, active_client, result, add_image_post_data, endpoint
):
    """Проверяем добавление изображения"""
    count_before = image_model.objects.count()
    response = active_client.post(endpoint,data=add_image_post_data)
    count_after = image_model.objects.count()
    assert (count_after > count_before) == result, (
        f'Проверьте, что {"авторизированный" if result else "анонимный"} '
        f'пользователь {"не" if not result else ""} может добавить изображение'
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'endpoint', LIST_VIEW_ENDPOINTS
)
def test_paginated_by_form(
        endpoint, unlogged_client, images, paginated_by_get_data
):
    """Проверяем настройку пагинации"""
    response = unlogged_client.get(endpoint, data=paginated_by_get_data)
    paginated_by = paginated_by_get_data['paginated_by']
    assert len(response.context.get('page_obj')) == paginated_by, (
        f'Проверьте что по адресу {endpoint} настройка пагинации работает '
        f'корректно'
    )
    response = unlogged_client.get(endpoint)
    assert len(response.context.get('page_obj')) == paginated_by, (
        f'Проверьте что настройки пагинации сохраняются для адреса {endpoint}'
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'active_client, result', [
        (
                lazy_fixture('unlogged_client'),
                False,
        ),
        (
                lazy_fixture('another_user_client'),
                False,
        ),
        (
                lazy_fixture('user_client'),
                True,
        ),

    ]
)
@pytest.mark.parametrize(
    'endpoint', [UPDATE_IMAGE_ENDPOINT, ]
)
def test_image_update_form(
        endpoint,
        active_client,
        result,
        image,
        image_update_post_data,
):
    response = active_client.post(endpoint, data=image_update_post_data)
    image.refresh_from_db()
    assert (image.name == image_update_post_data['name']) == result, (
        f'Проверьте что {"аноним/не владелец" if not result else "владелец"} '
        f'{"не" if not result else ""} может редактировать информацию об '
        f'изображении'
    )
    assert (image.private == image_update_post_data['private']) == result, (
        f'Проверьте что {"аноним/не владелец" if not result else "владелец"} '
        f'{"не" if not result else ""} может редактировать информацию об '
        f'изображении'
    )
    for tag in image.tags.filter():
        assert (tag.pk in image_update_post_data['tags']) == result, (
            f'Проверьте что '
            f'{"аноним/не владелец" if not result else "владелец"} '
            f'{"не" if not result else ""} может редактировать информацию об '
            f'изображении'
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'active_client, result', [
        (lazy_fixture('unlogged_client'), False),
        (lazy_fixture('another_user_client'), False),
        (lazy_fixture('user_client'), True),
    ]
)
def test_tag_form():
    pass

