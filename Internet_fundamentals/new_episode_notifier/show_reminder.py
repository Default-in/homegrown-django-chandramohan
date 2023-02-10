import requests
import json
import os.path
from constants import *
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import csv
import pandas

def send_mail(html_content):
    message = Mail(
        from_email = FROM_EMAIL,
        to_emails = TO_EMAIL,
        subject = SUBJECT,
        html_content = html_content
    )
        #html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


def check_if_file_exists():
    if os.path.exists(LOCAL_FILE_NAME):   
        return True
    return False 


def write_to_csv(show_details_list):
    print("Show details list: ", show_details_list)
    if not check_if_file_exists():
        with open(LOCAL_FILE_NAME, 'w+') as file:
            fieldnames = FIELDNAMES
            writer = csv.writer(file)
            writer.writerow(fieldnames)
            writer.writerow(show_details_list)    
    else:
        with open(LOCAL_FILE_NAME, 'a') as file:
            data = pandas.read_csv(LOCAL_FILE_NAME, header=0)
            existing_show_ids_list = list(data.show_id)
            print("Existing show ids", existing_show_ids_list)
            if int(show_details_list[1]) not in existing_show_ids_list:
                writer = csv.writer(file)
                writer.writerow(show_details_list)
            else:
                print("You have already added that show!!!")    

    
def get_shows_list():
    url = MOVIE_DB_URL

    data = requests.get(url)
    formatted_data = json.loads(data.content)

    #print(formatted_data['results'])

    for name in formatted_data['results']:
        print(name['name'])


def search_for_show(show_to_search):
    url = 'https://api.themoviedb.org/3/search/tv?api_key=489d17035e3c102567659de6759b8bfd&language=en-US&page=1&query=' + show_to_search
    data = requests.get(url)
    formatted_data = json.loads(data.content)

    search_results_list = []

    print("Results: \n")
    index = 1
    for show in formatted_data['results']:
        print(index,'. ', show['name'])
        search_results_list.append({'show_name':show['name'], 'id': show['id'] })
        index += 1

    return search_results_list


def get_details_of_the_show(show_id):
    get_more_details_of_show_url = 'https://api.themoviedb.org/3/tv/' + str(show_id) + '?api_key=489d17035e3c102567659de6759b8bfd&language=en-US'
    more_details_of_show = requests.get(get_more_details_of_show_url)
    formatted_more_show_data = json.loads(more_details_of_show.content)

    print("Details: ", formatted_more_show_data)

    print("Last episode to air: ", formatted_more_show_data['last_episode_to_air']['episode_number'])
    print("Last season to air: ", formatted_more_show_data['last_episode_to_air']['season_number']) 

    most_recent_season = formatted_more_show_data['last_episode_to_air']['season_number']
    most_recent_episode = formatted_more_show_data['last_episode_to_air']['episode_number']

    return [most_recent_season, most_recent_episode]


def add_show_to_track(show):
    show_details = get_details_of_the_show(show['id'])
    write_to_csv([show['show_name'], str(show['id']), str(show_details[0]), str(show_details[1])])


def check_new_releases():
    data = pandas.read_csv(LOCAL_FILE_NAME, header=0)
    #existing_show_ids_list = list(data.show_id)
    #print(data.head())
    for index, row in data.iterrows():
        print (index,row["show_name"], row["show_id"], row["last_season_watched"], row["last_episode_watched"])
        show_update = get_details_of_the_show(row["show_id"])
        if show_update[0] >= int(row["last_season_watched"]):
            if show_update[1] > int(row["last_episode_watched"]):
                html_content = '<strong>The season {} episode {} of {} is out now. Check it out.!!! </strong>'.format(show_update[0], show_update[1], row["show_name"])
                send_mail(html_content)


if __name__ == "__main__":
    #if check_if_file_exists():
    #    check_new_releases()
    #else:
    print("Here are some top shows trending these days.\n")
    get_shows_list()

    flag = True
    while flag:
        print("Enter the name of the show you'd like to add for tracking (enter exit when done): ")
        show_to_search = str(input())
        if show_to_search.lower() != 'exit': 
            search_results_list = search_for_show(show_to_search)
            index = int(input("Select the index from search results (like 1,2,3 etc.) : "))
            add_show_to_track(search_results_list[index-1])
        else:
            flag = False   

