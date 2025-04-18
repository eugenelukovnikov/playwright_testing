import pytest
import os

from pathlib import Path
from playwright.sync_api import Page

from PageObjTests.pages.login_page import LoginPage
from PageObjTests.pages.dashboard_page import DashboardPage


# Чтобы делать скриншоты упавших тестов:

# @pytest.fixture(autouse=True)
# def take_screenshot_on_failure(request, page):
#     yield
#     if request.node.rep_call.failed:  # Если тест упал
#         screenshot_dir = Path("screenshots")
#         screenshot_dir.mkdir(exist_ok=True)
        
#         test_name = request.node.name
#         page.screenshot(path=str(screenshot_dir / f"{test_name}.png"), full_page=True)


# Чтобы делать скриншоты всех тестов:
@pytest.fixture(autouse=True)
def take_screenshot_always(request, page):
    yield
    screenshot_dir = Path("screenshots")
    screenshot_dir.mkdir(exist_ok=True)
    
    test_name = request.node.name
    status = "passed" if not request.node.rep_call.failed else "failed"
    page.screenshot(path=str(screenshot_dir / f"{test_name}_{status}.png"), full_page=True)


#Allure
# @pytest.hookimpl(tryfirst=True)
# def pytest_configure(config):
#     config.option.allure_report_dir = "allure-results"


#Параметры
def pytest_addoption(parser):
    parser.addoption('--language', action='store', default="en",
                   help="Choose language for browser"),
    parser.addoption("--rvideo", action="store_true", help="Record video for tests")

#Фикстура создания контекста с настройками
@pytest.fixture(scope="function")
def context(browser, request):
    
    context = browser.new_context(
        locale=request.config.getoption("language"),
        ignore_https_errors=True,
        viewport=None,
        accept_downloads=True,
        record_video_dir="videos/" if request.config.getoption("--rvideo") else None,
        record_video_size={"width": 1280, "height": 720}
    )

    yield context
    context.close()
    #Если юзаем --rvideo, то осуществляется запись
    if request.config.getoption("--rvideo") and request.node.rep_call.failed:
        video = request.node.video
        video.save_as(Path("videos") / f"FAILED_{request.node.name}.webm")

#Основная фикстура страницы
@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    
    # Настройка загрузки файлов
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(downloads_dir, exist_ok=True)
    
    def handle_download(download):
        download.save_as(os.path.join(downloads_dir, download.suggested_filename))
    
    page.on("download", handle_download)
    
    yield page
    page.close()

@pytest.fixture(autouse=True)
def trace_failed_tests(request, page):
    page.context.tracing.start(screenshots=True)
    yield
    
    if request.node.rep_call.failed:
        trace_path = f"traces/trace_failed_{request.node.name}.html"
        page.context.tracing.stop(path=trace_path)
        
        with open(trace_path, "r") as f:
            print(f"\nFAILED TEST TRACE:\n{f.read()}\n")


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def dashboard_page(page):
    return DashboardPage(page)