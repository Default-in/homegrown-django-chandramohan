import re
from selenium import webdriver
import time
from constants import *
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt


def get_driver():
    driver = webdriver.Chrome(executable_path=DRIVER_LOCATION)
    return driver


def plot_sentiments(reviews):
    sentiment = SentimentIntensityAnalyzer()

    neg_count = 0
    pos_count = 0
    neu_count = 0

    for line in reviews:
        print("Review: ", line)
        sentiment_1 = sentiment.polarity_scores(line)
        print("Sentiment: ", sentiment_1)
        for rev in sentiment_1:
            if rev == 'neg':
                if sentiment_1[rev]:
                    neg_count += 1
            if rev == 'neu':
                if sentiment_1[rev]:
                    neu_count += 1        
            if rev == 'pos':
                if sentiment_1[rev]:
                    pos_count += 1

    x_axis = ['Positive', 'Negative', 'Neutral']
    y_axis = [pos_count, neg_count, neu_count]

    plt.bar(x_axis, y_axis)
    plt.title('Sentiment Analysis')
    plt.xlabel('Sentiments')
    plt.ylabel('Counts')
    plt.show()


def go_to_next_page(driver):
    try:
        next_page_button = driver.find_element_by_xpath(NEXT_PAGE_BUTTON_XPATH)
        next_page_button.click()
        time.sleep(3)    
        return True
    except Exception as exe:
        print("Exception: ", exe) 
        return False


def scrap(url):
    driver = get_driver()
    driver.get(url)
    time.sleep(3)
    try:
        reviews_list = []
        
        index = 0
        while index < 10:

            for review_num in range(1, 5):
                review = driver.find_element_by_xpath(REVIEW_XPATH+str(review_num)+']').text
                print("REVIEW: ", review)
                if review:
                    reviews_list.append(review)

            print("Going to next page.") 
            next_page = go_to_next_page(driver)  
            if not next_page:
                break
            index += 1

        return reviews_list        

    except Exception as e:
        print("Exception: ", e)


if __name__ == '__main__':
    reviews = scrap(ZOMATO_URL)
    plot_sentiments(reviews)

