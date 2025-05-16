import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()


def test_show_all_pets(driver):
    # Вводим email
    images_sum = 0
    driver.find_element(By.ID, 'email').send_keys('<your email>')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('<your password>')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # При небольшом размере окна есть кнопка открывающая пункты меню, нажимаем на нее
    driver.implicitly_wait(10)
    driver.get('https://petfriends.skillfactory.ru/all_pets')
    pets_card = driver.find_elements(By.CSS_SELECTOR, ".card")
    #time.sleep(3)

    driver.find_element(By.XPATH, '//span[@class="navbar-toggler-icon"]').click()
    button_my_pets = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Мои питомцы")]')))
    # Проверяем, что мы оказались на главной странице пользователя
    driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click()
    assert driver.find_element(By.TAG_NAME, 'h2').text == "boristsarkov"
    pets_table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table')))
    # Проверяем присутсвие питомцев
    pets_count = driver.find_element(By.CSS_SELECTOR, 'div[class=".col-sm-4 left"]')
    parts_pets_count = pets_count.text.split("\n")
    part_of_part_pets_count = parts_pets_count[1].split(': ')
    assert part_of_part_pets_count[1] != '0'
    images = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//img')
    pets = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//tbody//tr')
    pets_name = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//td[1]')
    pets_species = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//td[2]')
    pets_ages = driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//td[3]')

    # Проверяем наличие фото хотябы у половины питомцев
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            images_sum += 1
    assert images_sum >= len(images) // 2

    # Проверяем, что у всех питомцев есть имя, порода и возраст
    for i in range(len(pets)):
        assert pets_name[i].text != ''
        assert pets_species[i].text != ''
        assert pets_ages[i].text != ''


    # Проверяем что нет повторяющихся питомцев
    for i in range(len(pets)):
        for j in range(i + 1, len(pets)):
            assert pets[i].text != pets[j].text


    # Проверяем что у всех питомцев разные имена
    for i in range(len(pets_name)):
        for j in range(i + 1, len(pets_name)):
            assert pets_name[i].text != pets_name[j].text
