from PageObjTests.pages.login_page import *
from PageObjTests.pages.dashboard_page import *
import allure


@allure.feature("Логин")
@allure.story("Пользователь входит в систему")
@allure.title("Пользователь ввел некорректные данные, ошибка")
def test_login_fail(login_page):
    
    # login_page = LoginPage(page)

    login_page.open_page()
    login_page.login('invalid_user', 'invalid_password')
    
    assert login_page.get_error_message() == login_page.expected_error_msg, 'Got invalid username or password'

@allure.feature("Логин")
@allure.story("Пользователь входит в систему")
@allure.title("Пользователь ввел корректные данные, успех")
@pytest.mark.parametrize('username, password', [('user','user'), ('admin','admin')])
def test_login_success(login_page, dashboard_page, username, password):
    
    # login_page = LoginPage(page)
    # dashboard_page = DashboardPage(page)

    login_page.open_page()
    login_page.login(username, password)

    dashboard_page.assert_welcome_message(f"Welcome {username}")
    #dashboard_page.logout()

@allure.feature("Логин")
@allure.story("Пользователь выходит из системы")
@allure.title("Пользователь успешно вышел из системы, успех")
@pytest.mark.parametrize('username, password', [('user','user'), ('admin','admin')])
def test_logout_success(login_page, dashboard_page, username, password):
    
    # login_page = LoginPage(page)
    # dashboard_page = DashboardPage(page)

    login_page.open_page()
    login_page.login(username, password)

    dashboard_page.logout()