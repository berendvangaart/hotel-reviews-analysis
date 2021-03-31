import csv
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_search_url(city):
    """generate a search url"""
    template_url = "https://www.tripadvisor.com/Search?q={" \
                   "}&searchSessionId=C1576A8A16A8F97910EF5EBA2B96B1141615125722171ssid&sid" \
                   "=B344CD17605E41A59618969F7F667CAB1615126002215&blockRedirect=true&ssrc=h&rf=1 "
    return template_url.format(city)


def extract_hotel_links(hotels):
    """return links to review pages"""
    hrefs = []
    for hotel in hotels:
        uri = hotel.find('div', {'class', 'result-title'})
        # remove prefix
        uri = str(uri).replace(
            """<div class="result-title" onclick="widgetEvCall('handlers.openResult', event, this, '""", '')
        # remove data after the address
        split_uri = uri.partition("',")
        # create full path by adding prefix
        uri = "https://www.tripadvisor.com" + split_uri[0]

        hrefs.append(uri)
    return hrefs


def extract_review(review, page):
    review_hotel = page.find('h1', {'class', '_1mTlpMC3'}).text

    review_title = review.find('div', {'class', 'oETBfkHU'})\
        .find('div', {'class', 'glasR4aX'})\
        .find('a', {'class', 'ocfR3SKN'})\
        .find('span').find('span').text
    review_text = review.find('div', {'class', 'oETBfkHU'})\
        .find('div', {'class', '_3hDPbqWO'}).find('div', {'class', '_2f_ruteS'})\
        .find('div', {'class', 'cPQsENeY'}).q.span.text
    raw_rating = review.find('div', {'class', 'oETBfkHU'}).find('div', {'class', '_2UEC-y30'}).div.span
    review_rating = str(raw_rating).replace('<span class="ui_bubble_rating bubble_','')
    review_rating = str(review_rating).replace('"></span>', '')
    review_date = review.find('div', {'class', 'oETBfkHU'}).find('div', {'class', '_3hDPbqWO'}).find('span', {'class', '_34Xs-BQm'}).text
    review_date = str(review_date).replace('Date of stay: ', '')

    return [review_hotel, review_title, review_text, review_rating, review_date]

def save_reviews_to_csv(reviews):
    with open('tripadvisor.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Hotel_Name', 'review_title', 'review_text', 'Reviewer_Score', 'date'])

        writer.writerows(reviews)

def main(cities):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    hotel_hrefs = []
    review_list = []

    for city in cities:
        url = get_search_url(city)
        driver.get(url)

        time.sleep(1)

        soup = bs(driver.page_source, 'html.parser')
        hotels = soup.find_all('div', {'class', 'location-meta-block'})

        links = extract_hotel_links(hotels)
        for link in links:
            hotel_hrefs.append(link)

    for hotel_url in hotel_hrefs:
        driver.get(hotel_url)
        time.sleep(1)
        soup = bs(driver.page_source, 'html.parser')

        reviews = soup.find_all('div', {'class', '_2wrUUKlw'})

        for review in reviews:
            rv = extract_review(review, soup)
            review_list.append(rv)

    # print all reviews
    print('totaal aantal reviews scraped: ', len(review_list))

    save_reviews_to_csv(review_list)

    driver.close()


main(["london", "manchester", "liverpool", "kent", "bristol"])
