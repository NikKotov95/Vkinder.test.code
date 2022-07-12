import  pytest
from vk_functions import search_users, get_photo, sort_likes, write_msg, add_user, add_user_photos, \
    add_to_black_list

class TestVkinder:

    def setup_class(self):
        print('method setup_class')

    def setup(self):
        print('method setup')

    def teardown(self):
        print('method teardown')

# Тесты по работе приложения

    # Проверка поиска анкет
    @pytest.mark.parametrize('sex, age_at, age_to, city, result', [
        ('1', '18', '21', 'Москва', True)])
    def test_get_photo(self, user_id, result):
        assert get_photo(user_id) == result

    # Тест поиска фотографии
    @pytest.mark.parametrize('user_id, result', [('336261034'), True])
    def test_get_photo(self, user_id, result):
        assert get_photo(user_id) == result

    # Тест сортировки по лайкам
    @pytest.mark.parametrize('list_photos, result',
                             [(['1', 'photo_1', '2', 'photo_2', 'photo_3'],
                               ['1', '2', '3', 'photo_1', 'photo_2', 'photo_3']),])
    def test_sort_likes(self, list_photos, result):
        assert sort_likes(list_photos) == result

# Тесты по работе базы данных

    # Тест первичной регистрации пользователя
    @pytest.mark.parametrize('vk_id, result', [('1', False), ('1', False), ('336261034', False)])
    def test_register_user(self, vk_id, result):
        assert register_user(vk_id) == result

    # Тест добавления пользователя
    @pytest.mark.parametrize('event_id, vk_id, first_name, second_name, city, link, id_user, result',
                             [('7717001', '2', 'goga', 'boba', 'Turkey', 'www.vkman.ru', '1', False)])
    def test_add_user(self, event_id, vk_id, first_name, second_name, city, link, id_user, result):
        assert add_user(event_id, vk_id, first_name, second_name, city, link, id_user) == result

    # Тест добавления фото анкеты в БД
    @pytest.mark.parametrize('event_id, link_photo, count_likes, id_dating_user, result'
                             [('123', 'Link_link', '2', '3350252', False)])
    def test_add_user_photos(self, event_id, link_photo, count_likes, id_dating_user, result):
        assert add_user_photos(event_id, link_photo, count_likes, id_dating_user) == result

    # Добавление в черный список
    @pytest.mark.parametrize('event_id, vk_id, first_name, second_name, city, link, link_photo, count_likes, id_user, result',
                             [('123', '12', '12434', '1251321', 'sdfsdfs', 'fsdfsdfs', '12', '123', False)])
    def test_add_user_to_black_list(self, event_id, vk_id, first_name, second_name, city, link, link_photo, count_likes, id_user, result):
        assert add_to_black_list(event_id, vk_id, first_name, second_name, city, link, link_photo, count_likes, id_user) == result

    def teardow_class(self):
        print('method teardown_class')
