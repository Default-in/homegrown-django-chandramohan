import re
from selenium import webdriver
import time
from constants import *
import csv


def get_driver():
    driver = webdriver.Chrome(executable_path=DRIVER_LOCATION)
    return driver


def get_no_of_pages(num_of_results):
    num_of_pages = 0
    if num_of_results > 10:
        num_of_pages = num_of_results/10
        num_of_pages = int(num_of_pages) + 1

        return num_of_pages  
    else:
        return 1      


def scrap_data(driver):
    try:
        info_list = []
        info_boxes = driver.find_elements_by_class_name(INFO_BOX_CLASSNAME)
        print('Info boxes: ', info_boxes)

        for info_box in info_boxes:
            name = info_box.find_element_by_class_name(INFO_BOX_SUB_CLASSES['name']).text
            print("Name: ", name)
            stars = info_box.find_element_by_class_name(INFO_BOX_SUB_CLASSES['stars']).text
            print("Stars: ", stars)
            ratings = info_box.find_element_by_class_name(INFO_BOX_SUB_CLASSES['ratings']).text
            print("Ratings: ", ratings)
            location = info_box.find_element_by_class_name(INFO_BOX_SUB_CLASSES['location']).text
            print("Location: ", location)
            opens_at = info_box.find_element_by_class_name(INFO_BOX_SUB_CLASSES['opens_at']).text
            print("Opens at: ", opens_at)

            info_list.append([name, stars, ratings, location, opens_at])

        return info_list

    except Exception as e:
        print("Exception: ", e)    
        return []


def get_listings(main_url, num_of_pages):
    driver = get_driver()

    driver.get(main_url)
    time.sleep(3)

    if num_of_pages == 1:
        data_list = scrap_data(driver)
        for data in data_list:
            print(data) 
        return data_list

    elif num_of_pages > 1:
        combined_list = []

        data_list = scrap_data(driver)
        combined_list.append(data_list)

        for page_num in range(2, num_of_pages+1):    
            new_url = main_url + '/page-' + str(page_num)
            
            driver.get(new_url)
            data_list = scrap_data(driver)
            combined_list.append(data_list)

        return combined_list    


def write_data_to_csv(data_list):
    with open("out.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Stars', 'Ratings', 'Location', 'Opens at'])
        writer.writerows(data_list)




if __name__ == '__main__':
    search_query = input("Enter the search query: ")
    num_of_results = int(input("\nEnter the number of results you want (<100): "))

    num_of_pages = get_no_of_pages(num_of_results)

    main_url = URL + search_query

    data_list = get_listings(main_url, num_of_pages)

    write_data_to_csv(data_list[:num_of_results])



    