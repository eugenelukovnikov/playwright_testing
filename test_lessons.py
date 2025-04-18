import pytest
import os
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright, expect

@pytest.mark.skip()
def test_check_form_is_filled(page):

    page.goto("https://demo.playwright.dev/todomvc/#/")

    assert page.url == "https://demo.playwright.dev/todomvc/#/"
    expect(page).to_have_url("https://demo.playwright.dev/todomvc/#/")

    to_do_locator = "//input[@class='new-todo']"
    items_to_do = "//li[@data-testid='todo-item']"
    first_toggle_locator = "//li[@data-testid='todo-item'][1]//input[@class='toggle']"
    expected_count = 2

    assert page.locator(to_do_locator).input_value() == ""
    expect(page.locator(to_do_locator)).to_be_empty()

    page.locator(to_do_locator).fill('Task Number 1')
    page.locator(to_do_locator).press('Enter')
    page.locator(to_do_locator).fill('Task Number 2')
    page.locator(to_do_locator).press('Enter')

    assert page.locator(items_to_do).count() == expected_count, f'Count is not {expected_count}'
    expect(page.locator(items_to_do)).to_have_count(2)

    page.locator(first_toggle_locator).click()
    first_item = page.locator(items_to_do).first
    
    assert first_item.get_attribute("class") == 'completed'
    expect(page.locator(items_to_do).nth(0)).to_have_class('completed')
    assert 'stop this!' == 'i like it'

