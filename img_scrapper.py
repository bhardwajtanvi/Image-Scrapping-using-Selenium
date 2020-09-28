import os
import time
import requests
from selenium import webdriver
import shutil
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver=webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
glob_time=""

def fetch_image_urls(query: str, max_links_to_fetch: int, wd=driver, sleep_between_interactions: int = 1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

        # build the google query

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")
            return

        # move the result startpoint further down
        results_start = len(thumbnail_results)
        print(image_urls)
    return image_urls

def persist_image(folder_path:str,url:str, counter):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

def search_and_download(search_term, number_images, driver=driver, target_path='./images'):
    
    global glob_time 
    glob_time = str(time.time())
    # print("gt of search",glob_time)
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' '))+'_'+str(number_images)+glob_time) # make the folder name inside images with the search string

    

    if not os.path.exists(target_folder):
        os.makedirs(target_folder) # make directory using the target path if it doesn't exist already

    with driver as wd:
        print(driver)
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)

    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1

def makezip(search_term,number_images):
    target_path='./images'
    global glob_time 
    
    # print("gt",glob_time)
    fold= os.path.join(target_path, '_'.join(search_term.lower().split(' '))+'_'+str(number_images)+glob_time)
    zip_name= search_term.lower()+'_'+str(number_images)+glob_time+'.zip'
    shutil.make_archive("static/"+search_term.lower()+'_'+str(number_images)+glob_time, "zip", fold)
    if os.path.exists(fold):
        shutil.rmtree(fold)
    return zip_name



search_term = 'flute'
# num of images you can pass it from here  by default it's 10 if you are not passing
number_images = 1
search_and_download(search_term=search_term, number_images=number_images) # method to download images
# makezip(search_term=search_term,number_images=number_images)