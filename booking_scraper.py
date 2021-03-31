import csv
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re

def get_search_url(city):
    """generate a search url"""
    template_url = "https://www.booking.com/{}"
    return template_url.format(city)


def extract_hotel_links(hotels):
    """return links to review pages"""
    hrefs = []
    for hotel in hotels:
        uri = hotel.find('a', {'class', 'js-sr-hotel-link', })
        uri = str(uri).replace('<a class="js-sr-hotel-link hotel_name_link url" href="',"")
        split_url = uri.partition(";highlight")
        uri = "https://www.booking.com" + (str(split_url[0]))
        hrefs.append(uri)
    return hrefs


def extract_review(review, soup):
    review_hotel = soup.find('h2', {'class', 'hp__hotel-name'}).text
    review_title = review.find('h3', {'class': 'c-review-block__title'}).text
    review_both = review.find_all('span', {'class': 'c-review__body'})

    pos = review.find_all('svg', {'class': '-iconset-review_great'})
    neg = review.find_all('svg', {'class': '-iconset-review_poor'})

    review_positive_text = ''
    review_negative_text = ''
    if len(review_both) == 2:
        review_positive_text = review_both[0].text
        review_negative_text = review_both[1].text
    elif len(pos) == 1 and len(neg) == 0:
        review_positive_text = review_both[0].text
    elif len(neg) == 1 and len(pos) == 0:
        review_negative_text = review_both[0].text

    review_rating = review.find('div', {'class': 'bui-review-score__badge'}).text
    review_date = review.find('span', {'class', 'c-review-block__date'}).text
    review_date = str(review_date).replace('Reviewed: ', '')

    return [review_hotel, review_title, review_positive_text, review_negative_text, review_rating, review_date]


def save_reviews_to_csv(reviews):
    with open('booking.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Hotel_Name', 'review_title', 'review_positive','review_negative', 'Reviewer_Score', 'date'])

        writer.writerows(reviews)


def main(cities):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    hotel_hrefs = []
    review_list = []

    for city in cities:
        url = get_search_url(city)
        print("url: ", url)
        driver.get(url)

        time.sleep(1)

        soup = bs(driver.page_source, 'html.parser')
        hotels = soup.find_all('div', {'class', 'sr_item'})

        links = extract_hotel_links(hotels)

        for link in links:
            hotel_hrefs.append(link)

    print(hotel_hrefs)
    for url in hotel_hrefs:
        driver.get(url)
        time.sleep(1)

        element = driver.find_element_by_xpath('//*[@id="show_reviews_tab"]')
        element.click();

        time.sleep(1)

        soup = bs(driver.page_source, 'html.parser')
        reviews = soup.find_all('li', {'class', 'review_list_new_item_block'})

        for review in reviews:
            rv = extract_review(review, soup)
            review_list.append(rv)

    save_reviews_to_csv(review_list)

    driver.close()




main(["maastricht", "manchester", "liverpool", "kent", "bristol"])