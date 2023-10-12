from yandex_api_stand_tests import data, sender_stand_request


def get_user_body(param):
    current_body = data.body.copy()
    current_body["firstName"] = param
    return current_body


# Функция для позитивной проверки
def positive_assert(first_name):
    # В переменную user_body сохраняется обновленное тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken, и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть, и он единственный
    assert users_table_response.text.count(str_user) == 1

def negative_assert_symbol(first_name):
    user_body  = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"


def negative_assert_no_first_name(user_body):
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "Не все необходимые параметры были переданы"

def test_create_user_no_first_name_get_error_response():
        user_body = data.body.copy()
        user_body.pop("firstName")
        negative_assert_no_first_name(user_body)

def test_create_user_empty_first_name_get_error_response():
        user_body=get_user_body("")
        negative_assert_no_first_name(user_body)

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааa")

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")

def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")

def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")

def create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и КО")

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№;№;;№;")

def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400