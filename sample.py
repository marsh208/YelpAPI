# -*- coding: utf-8 -*-
"""
Yelp Fusion API code sample.

This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.

This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
API_KEY= 'R3Zs7l4Ahk_meyDBaKnIh4kksSQlKU2WGEYO0iM1BQPx3R6U8nAD45C0W_-xZNhS3hNY0YfDtrMPzl6pAvlYRgCqJWQwtzL9KXM5WN_YQrl4CvI_6SSRcGgid8foW3Yx'


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.





def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location, limit):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': limit
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)

#returns all info regarding business id
def query_api(term, location, limit):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location, limit)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))

#returns businesses
def return_business_name(term, location, limit):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location, limit)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))

    return businesses

def format_business_info(businesses, option):   #prints more information on user specified option in main pertaining to selected business
    #####DO TRY CATCH FOR THESE
    print("\n")
    print("Business Name: " + businesses[option-1]['name'])
    print("Website Link: " + str(businesses[option-1]['url']))
    print("Phone Number: " + businesses[option-1]['display_phone']) #business_option - 1 because they are selecting an index in a dictionary
    print("Address: " + str(businesses[option-1]['location']['address1']))
    print("Price Range (0-4): " + str(businesses[option-1]['price']))
    print("Rating (0-5): " + str(businesses[option-1]['rating']))
    print("\n")
    print("Printing original list... ")

def main():

    loop = 1
    while True:
        print("\n")
        print("Welcome to the yelp API!")
        print("0) Quit")
        print("1) Search by location and term") #separate into submenu for reataurants, yes?
        print("2) Display top 10 open restaurants by location")
        print("3) Search for home services")

        user_option = int(input("Please select an option: "))
        if user_option == 0:
            break
        elif user_option == 1: #search by location and food type
            user_term = raw_input("Enter a term to search \n(i.e. breakfast, lunch, dinner, or a business name/type): ")
            user_location = raw_input("Enter a location (i.e. San Francisco, CA): ")
            user_search_limit = int(input(("Enter a search limit: ")))
            try:
                business_list = return_business_name(user_term, user_location, user_search_limit) #takes specified amount of businesses and stores them in bussiness_list
                while(loop == 1):
                    for i in range(user_search_limit):
                        print(str(i+1) + ")" + " " + business_list[i]['name'])
                    business_option = int(input("Select the business you would like to know more about\n or type 0 to go back to menu: "))
                    if business_option == 0:
                        break
                    format_business_info(business_list, business_option)
            except HTTPError as error:
                sys.exit(
                    'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                        error.code,
                        error.url,
                        error.read(),
                    )
                )
        elif user_option == 2:   #returns list of 10 top open restaurants
            user_location = raw_input("Enter a location (i.e. San Francisco, CA): ")
            try:
                business_list = return_business_name("Top 10 Restaurants", user_location, 10)
                while(loop == 1):
                    for i in range(10): #for top 10 list, original option select
                        print(str(i+1) + ")" + " " + business_list[i]['name'])
                    business_option = int(input("Select the business you would like to know more about\n or type 0 to go back to menu: "))
                    if business_option == 0:
                        break
                    format_business_info(business_list, business_option)
            except HTTPError as error:
                sys.exit(
                    'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                        error.code,
                        error.url,
                        error.read(),
                    )
                )

        elif user_option == 3:
            print("1) Contractors")
            print("2) Electricians")
            print("3) Home Cleaners")
            print("4) HVAC")
            print("5) Landscaping")
            print("6) Locksmiths")
            print("7) Movers")
            print("8) Plumbers")

            home_service_option = int(input("Select an option: "))

            user_location = raw_input("Enter a location (i.e. San Francisco, CA): ")

            if home_service_option == 1:
                try:
                    business_list = return_business_name("Top 10 Contractors", user_location, 10)
                    while(loop == 1):
                        for i in range(10): #for top 10 list, original option select
                            print(str(i+1) + ")" + " " + business_list[i]['name'])
                        business_option = int(input("Select the business you would like to know more about\n or type 0 to go back to menu: "))
                        if business_option == 0:
                            break
                        format_business_info(business_list, business_option)

                except HTTPError as error:
                    sys.exit(
                        'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                            error.code,
                            error.url,
                            error.read(),
                        )
                    )






if __name__ == '__main__':
    main()
