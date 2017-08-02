import bs4
import requests
import time
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def get_query_link(term):
    term = term.replace(' ', '+')
    query = 'https://www.google.com/search?q={}&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiz_fam6bfVAhVp0FQKHZO4APQQ_AUICygC&biw=1439&bih=760'
    return query.format(term)


def get_image_links(query_str, limit=250):
    # used `brew install chromedriver` to get driver
    link = get_query_link(query_str)
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(link)
    thumbs = driver.find_elements_by_class_name('rg_i')
    urls = set()
    count = 0
    i = 0

    while count < limit:
        try:
            thumb = thumbs[i]
            i += 1
            ActionChains(driver).move_to_element(thumb).click().perform()
            if len(driver.window_handles) > 1:
                window_handles = driver.window_handles
                driver.switch_to_window(driver.window_handles[1])
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
                continue
        except:
            thumbs = driver.find_elements_by_class_name('rg_i')
            if i > len(thumbs):
                break
        time.sleep(0.05)
        imgs = driver.find_elements_by_class_name('irc_mi')
        for img in imgs:
            try:
                url = img.get_attribute('src')
            except:
                continue
            if url and not url in urls:
                urls.add(url)
                count += 1
    driver.close()
    path = query_str.replace(' ', '_') + '.txt'
    with open(path, 'w') as f:
        for url in urls:
            f.write(url + '\n')


def download_images(term):
    url_file = term.replace(' ', '_') + '.txt'
    count = 0
    base_path = 'photos/' + term.replace(' ', '_') + '{}.{}'
    with open(url_file) as urls:
        for url in urls:
            url = url.strip()
            ext = url.split('.')[-1]
            if ext in ['jpg', 'png']:
                path = base_path.format(count, ext)
                try:
                    download_image(url, path)
                    count += 1
                except:
                    pass


def download_image(url, filename):
    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        with open(filename, 'wb') as f:
            f.write(r.content)


def main():
    """gathers images of apples and oranges and stores it in the photos/ directory"""
    if not os.path.exists('photos'):
        os.makedirs('photos')
    apple = 'apple fruit'
    orange = 'orange fruit'
    get_image_links(apple)
    download_images(apple)
    get_image_links(orange)
    download_images(orange)


if __name__ == '__main__':
    main()
