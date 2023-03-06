import time
import urllib.request
import instaloader
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from .models import Instagramlink

from django.core.files import File
import urllib.request
import os


def web_scraping():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("http://www.instagram.com")
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
    username.clear()
    username.send_keys('your-username-instagram')
    password.clear()
    password.send_keys('your-password-instagram')

    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']"))).click()

    time.sleep(5)
    alert = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    alert2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    time.sleep(5)
    driver.get("https://www.instagram.com/wayu.uz/")
    time.sleep(5)
    n_scrolls = 1
    for _ in range(n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
    anchors = driver.find_elements(By.TAG_NAME, 'a')
    anchors = [a.get_attribute('href') for a in anchors]
    parent_dir = "you_path"

    for i, a in enumerate(anchors):
        if str(a).startswith("https://www.instagram.com/p/"):
            print(a)
            L = instaloader.Instaloader()
            post = instaloader.Post.from_shortcode(L.context, a.split("/")[-2])
            if not post.is_video:
                urllib.request.urlretrieve(str(post.url), f"{parent_dir}/{i}.jpg")
                obj = Instagramlink.objects.create(link=a, image=f"instagram/{i}.jpg")
                obj.save()


