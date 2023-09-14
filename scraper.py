import os
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

# Function to scroll down the page and load more images
def scroll_down(driver, num_scrolls):
    for _ in range(num_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for the page to load

# Function to fetch and scrape images based on a search query
def scrape_images(query, num_images):
    # Create a directory to store the downloaded images
    os.makedirs("images", exist_ok=True)

    # Create a subfolder with the query name to store images
    query_folder = os.path.join("images", query)
    os.makedirs(query_folder, exist_ok=True)

    # Set up the Chrome WebDriver
    driver = webdriver.Chrome()

    # Build the Google search URL
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"

    # Send an HTTP GET request to the Google search page
    driver.get(search_url)

    # Initialize a counter for downloaded images
    image_count = 0

    try:
        while image_count < num_images:
            # Scroll down to load more images
            scroll_down(driver, num_scrolls=3)

            # Parse the HTML content of the search page
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Find all image tags in the HTML
            img_tags = soup.find_all("img")

            # Download and save each image
            for img_tag in img_tags:
                if image_count >= num_images:
                    break

                img_url = img_tag.get("src")
                if img_url:
                    # Check if the URL is a valid HTTP/HTTPS link
                    if img_url.startswith("http") or img_url.startswith("https"):
                        # Get the image file name from the URL
                        img_name = f"{query}_{image_count}.jpg"

                        # Send an HTTP GET request to download the image
                        img_response = requests.get(img_url)

                        # Check if the request was successful
                        if img_response.status_code == 200:
                            # Save the image to the subfolder
                            img_path = os.path.join(query_folder, img_name)
                            with open(img_path, "wb") as img_file:
                                img_file.write(img_response.content)
                            print(f"Downloaded: {img_name}")
                            image_count += 1
                    elif img_url.startswith("data:image/jpeg;base64"):
                        # Handle base64-encoded images (optional)
                        # You can add code here to decode and save the image
                        pass

            # Break the loop if enough images have been downloaded
            if image_count >= num_images:
                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        driver.quit()
        print(f"Downloaded {image_count} images based on the search query: {query}")

# Input the search query and the number of images to scrape
search_query = input("Enter a search query: ")
num_images = int(input("Enter the number of images to scrape: "))

# Call the scrape_images function to perform the scraping
scrape_images(search_query, num_images)
