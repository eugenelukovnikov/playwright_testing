import pytest
import os
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright, expect

@pytest.mark.skip()
def test_select(page):
    
    page.goto("https://zimaev.github.io/select/", wait_until='domcontentloaded')
    page.select_option('//select[@id="floatingSelect"]', value="3")
    page.select_option('//select[@id="skills"]', value=["playwright", "python"])

@pytest.mark.skip()
def test_drag_and_drop(page):
    
    page.goto('https://zimaev.github.io/draganddrop/')
    page.drag_and_drop("//img[@id='drag']", "//div[@id='drop']")

@pytest.mark.skip()
def test_dialogs(page):
    
    page.goto("https://zimaev.github.io/dialog/")
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_text("Диалог Confirmation").click()

@pytest.mark.skip()
def test_alert_confirmation_message(page):
    
    page.goto("https://zimaev.github.io/dialog/")

    dialog_messages = []  

    page.on("dialog", lambda d: (
        dialog_messages.append(d.message),
        d.accept() 
    ))

    page.get_by_text("Диалог Confirmation").click()

    assert "Вы хотите сохранить изменения?" in dialog_messages
    assert page.locator("//div[@id='msg']").inner_text() == 'Изменения сохранены!'

@pytest.mark.skip()    
def test_prompt_confirmation_message(page):
    
    page.goto("https://zimaev.github.io/dialog/")

    dialog_messages = []  

    page.on("dialog", lambda d: (
        dialog_messages.append(d.message),
        d.accept('10') 
    ))

    page.get_by_text("Диалог Prompt").click()

    assert "Please enter any number" in dialog_messages  
    assert page.locator("//div[@id='msg']").inner_text() == 'You have entered number: 10'

@pytest.mark.skip() 
def test_uploading(page):
    
    page.goto('https://zimaev.github.io/upload/')
    file_path = Path('screenshots') / 'test_prompt_confirmation_message[chromium]_passed.png'
    page.set_input_files("//input[@id='formFile']", file_path)
    # page.set_input_files("//input[@id='formFile']", os.path.join(os.getcwd(), "screenshots", "test_prompt_confirmation_message[chromium]_passed.png"))     
    page.click("//input[@id='file-submit']")

@pytest.mark.skip()
def test_downloading(page):
    
    page.goto('https://demoqa.com/upload-download')
    with page.expect_download() as download_info:
        page.locator("//a[@id='downloadButton']").click()
    
    download = download_info.value
    destination_folder_path = 'downloads'
    download.save_as(os.path.join(destination_folder_path, download.suggested_filename))

@pytest.mark.skip()
def test_get_all_elements(page):
   
    page.goto('https://td-prometey.ru/catalog/pechi-dlya-bani/')
    row = page.locator("//span[contains(@class, 'product-cat-title product-cat-title--custom')]")
    print(row.all_inner_texts())

@pytest.mark.skip()
def test_full_page_loaded(request, page):
    
    page.goto('https://td-prometey.ru/catalog/pechi-dlya-bani/')

@pytest.mark.skip()
def test_change_window(page):
    
    page.goto("https://zimaev.github.io/tabs/")
    with page.context.expect_page() as dashboard_page:
        page.click("//button[@id='dashboard']")
    dashboard = dashboard_page.value
    dashboard.screenshot(path="screenshots/dashboard_page_screenshot.png", full_page=True)
    assert dashboard.locator("//h1[@class='h2']").inner_text() == "Dashboard"
    expect(dashboard.locator("//h1[@class='h2']"), "css class not h2").to_have_class('h2')

@pytest.mark.skip()
# Перехват и изменение запроса, если есть заданные по умолчанию данные
def test_network(page):
    page.route("api/register", lambda route: route.continue_(post_data='{"email": "user","password": "secret"}'))
    page.goto('https://reqres.in/')
    page.get_by_text('Register - successful').click()

@pytest.mark.skip()
def test_mock_brewery_db(page):
    
    mock_content = Path("test_data/breweries.html").read_text(encoding="utf-8")
    
    page.route("**/**/France", lambda route: route.fulfill(
        status=200,
        content_type="text/html",
        body=mock_content
    ))

    expected_text = "Moscow. Kidding!"

    page.goto('https://openbrewerydb.org/breweries/France')
    assert page.get_by_text("Moscow. Kidding!").inner_text() == expected_text, f'Expected {expected_text}, but got {page.get_by_text("Moscow. Kidding!").inner_text()}'
    
@pytest.mark.skip()
def test_mock_200(page):
    page.route("**/api/data", lambda route: route.fulfill(
        status=200,  # можно поставить любой код (404, 500 и т.д.)
        content_type="application/json",  # или "text/html"
        body='{"success": true, "message": "Моковые данные!"}'
    ))

    page.goto("https://example.com/api/data")
    assert page.get_by_text("Моковые данные!").is_visible() 

@pytest.mark.skip()
def test_mock_500(page):
    page.route("**/api/error", lambda route: route.fulfill(
        status=500,
        body='{"error": "Сервер упал!"}'
    ))