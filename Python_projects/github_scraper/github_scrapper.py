import requests
from bs4 import BeautifulSoup
import html5lib
import re
import csv
from .constants import *


#This function fetches all the github profile links from the search result page and returns list containing the links 
def get_profile_links(search_query, no_of_results):
    base_url = BASE_URL
    github_url = GITHUB_URL
    links = []

    total_pages = int(no_of_results/10) + 1

    page = 1
    while page <= total_pages:
        req = requests.get(base_url + "p=" + str(page) + "&q=" + str(search_query))
        soup=BeautifulSoup(req.content,'html5lib')

        repo_links_ul = soup.find("ul", class_=REPO_LINKS_CLASSES['ul'])
        repo_links = repo_links_ul.find_all('a', class_=REPO_LINKS_CLASSES['a'])
        for i in repo_links:
            print("/".join(i['href'].split("/")[:2]))
            suffix_url = "/".join(i['href'].split("/")[:2])
            links.append(github_url+suffix_url)
        page += 1    

    return links[:no_of_results]   


#This function writes the contents of the list to a csv file
def write_to_csv(profiles_list):
    with open("github_profiles.csv", 'w') as file:
        fieldnames = ['name', 'username', 'bio', 'followers', 'following', 'profile_pic', 'num_of_repos']
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(profiles_list)


#This function fetches the info of users from the profile page
def get_profile_info(profile_link_list):    
    profiles_list = []
    for profile_link in profile_link_list:
        req = requests.get(profile_link)
        soup = BeautifulSoup(req.content,'html5lib')

        try:
            namediv = soup.find("h1" ,class_=PROFILE_CLASSES['h1'])
            name = namediv.find_all('span')[0].getText()
            name = re.sub(' +', ' ', name)
            name = name.replace('\r', '').replace('\n', '')
            u_name = namediv.find_all('span')[1].getText()
            u_name = re.sub(' +', ' ', u_name)
            u_name = u_name.replace('\r', '').replace('\n', '')

            biodiv = soup.find("div", class_=PROFILE_CLASSES['biodiv'])
            bio = biodiv.find('div').get_text()

            statstab = soup.find(class_=PROFILE_CLASSES['stats_tab'])
            elements = statstab.find(class_=PROFILE_CLASSES['stats_elems'])
            followers = elements.find_all('a')[0].find('span').getText().strip(' ')
            following = elements.find_all('a')[1].find('span').getText().strip(' ')
            #totstars=elements.find_all('a')[2].find('span').getText().strip(' ')

            u_img=soup.find(class_=PROFILE_CLASSES['u_img'])['src']
            repo_num=soup.find(class_=PROFILE_CLASSES['repo_num']).find('span',class_=PROFILE_CLASSES['repo_num_sub']).getText()

            profiles_list.append([name, u_name, bio, followers, following, u_img, repo_num])

            print("Name: ", name)
            print("Username: ", u_name)
            print("Bio: ", bio)
            print("Followers: ", followers)
            print("Following: ", following)
            print("User image: ", u_img)
            print("Repo num: ", repo_num)
        except Exception as e:
            print(e)    

    write_to_csv(profiles_list)
    

if __name__ == '__main__':
    search_query = input("Enter the search query: ")
    no_of_results = int(input("\nEnter the number of results you want (<100): "))

    profile_links =  get_profile_links(search_query, no_of_results)
    get_profile_info(profile_links)