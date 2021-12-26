from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import requests
import urllib.request
import shutil
import geckodriver_autoinstaller

geckodriver_autoinstaller.install()  # Check if the current version of geckodriver exists
                                     # and if it doesn't exist, download it automatically,
                                     # then add geckodriver to path
# The request must be done by selenium webdriver because it contains JavaScript

##################### Modify these lines #####################
url = "https://www.ecosia.org/images?q=amanite%20tue-mouches"
species_name = "amanite-tue-mouches"
path = "../data/" + species_name + "/"
nb_images = 100
###############################################################

# Initialize the browser
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox()
driver.get(url)

# Parse the HTML
soup = BeautifulSoup(driver.page_source, "html.parser")

# Wait until the user has scrolled enough to load enough images
nb_images_found = 0
while nb_images_found < nb_images:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    a_divs = soup.find_all("a", class_='image-result__link') # Get all the <img> divs that contains a search result
    nb_images_found = len(a_divs)
    print("Images : {}".format(nb_images_found))
    print("Continue scrolling")

# Get the image links from the divs
image_urls = [a["href"] for a in a_divs]

def download_image(image_url, image_name):
    response = requests.get(image_url, stream=True)
    realname = ''.join(e for e in image_name if e.isalnum())

    file = open(path+"{}.jpg".format(realname), 'wb')

    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, file)
    del response

for i in range(nb_images):
    print("Downloaded : {}".format(i))
    image_name = "{}-{}".format(species_name, i)
    download_image(image_urls[i], image_name)
