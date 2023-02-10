import requests
import json
from datetime import date
from constants import *


def dead_link_check(link):
    response = requests.get(link)
    if response.status_code != 200:
        return True
    return False


def get_data_from_product_hunt():
    all_products_list = []
    for page_no in range(1, 3):
        products_list = []

        url = BASE_POSTS_URL + str(page_no)
        data = requests.get(url, headers=HEADERS)
        formatted_data = json.loads(data.content)

        for product in formatted_data['posts']:
            product_name = product['name']
            product_url = product['discussion_url']
            product_category = product['category_id']
            comments_count = product['comments_count']
            upvotes_count = product['votes_count']

            products_list.append({'name': product_name, 'url': product_url, 'category': product_category, 'comments_count': comments_count, 'upvotes_count': upvotes_count})

        all_products_list.extend(products_list)

    return all_products_list


def get_top_5_upvoted_products():

    url = TOP_POSTS_URL+str(date.today().month)+'&search[featured_year]='+str(date.today().year)+'&per_page=5'
    data = requests.get(url, headers=HEADERS)
    formatted_data = json.loads(data.content)

    print("Top 5 upvoted products\n")
    for product in formatted_data['posts']:
        print("Product name: ", product['name'])
        #print("Product url: ", product['redirect_url'])
        print("Product url: ", product['discussion_url'])
        print('Comments count: ', product['comments_count'])
        print("Upvotes count: ", product['votes_count'])


def get_deadlinks_ranking(all_products_list):
    vote_ranking = {}
    comment_ranking = {}
    for product in all_products_list:
        comments_count = product['comments_count']
        votes_count = product['upvotes_count']
        product_name = product['name']
        product_link = product['url']

        print("Product name: ", product_name)
        #print("Product url: ", product['redirect_url'])
        print("Product url: ", product_link)
        print('Comments count: ', comments_count)
        print("Upvotes count: ", votes_count)
        print('\n\n')
        
        if dead_link_check(product_link):
            vote_ranking[product_name] = votes_count
            comment_ranking[product_name] = comments_count
    
    sorted_vote_ranking = sorted(vote_ranking.items(), key=lambda x: x[1], reverse=True)
    sorted_comment_ranking = sorted(comment_ranking.items(), key=lambda x: x[1], reverse=True)


    print("Sorted vote ranking: ", sorted_vote_ranking)
    print("Sorted comment ranking: ", sorted_comment_ranking)
    return [sorted_vote_ranking, sorted_comment_ranking]

        
if __name__ == "__main__":
    #data = get_data_from_product_hunt()
    #rankings_list = get_deadlinks_ranking(data)
    get_top_5_upvoted_products()