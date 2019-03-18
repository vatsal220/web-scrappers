import json
import requests
from bs4 import BeautifulSoup

url_list = ['https://towardsdatascience.com/data-science/home', 'https://towardsdatascience.com/machine-learning/home', 'https://towardsdatascience.com/programming/home', 'https://towardsdatascience.com/data-visualization/home']

#This function gathers all the url's from the links in url_list, then displays the unique links from each url
def find_articles_in_page(all_urls):
    headers = {'User-Agent': 'Mozilla/5.0'}
    unique_links = []   #Empty varaible to store the unique links into
    for page_url in all_urls:           #Soupifies all the url's
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):  #Finds all the unique a tags which include a link
            if link['href'] not in unique_links:
                unique_links.append(link['href'])   #Adds it to the unique links variable, .append makes it so it doesnt get overwritten

    return unique_links

#This function filters the unique links for the links which have are towardsdatascience
def filter_links(unique_links):
    filtered_links = []     #Empty variable to store the filtered links
    for link in unique_links:       #Noticed a pattern, if unique links meet a certain criteria then they will be filtered
        if "-------------" in link and "https://towardsdatascience.com" in link:
            if link not in filtered_links:
                filtered_links.append(link)
                print("--->", link)
    return filtered_links

#This function scrapes the title, text, author and clap number from the list of filtered links and stores it in a json file
def scrape_article(final_articles):
    dict_article_data = []      #Empty variable to store the scraped article data
    file = "medium_data.json"       #Name of the json file being saved
    for page_content in final_articles:     #Loops through all of the filtered links to get the necessary information
        #Gets the contents of the url
        response = requests.get(page_content)
        text = response.text
        soup = BeautifulSoup(text, 'html.parser')

        #Retrieves article title
        title = soup.title
        print(title)

        #Retrieves article author
        container_author = soup.find("div",{"class": "u-paddingBottom3"})
        author = container_author.a.contents
        print(author)

        #Retrieves the clap number
        container_clap = soup.find("span", {"class": "u-relative u-background js-actionMultirecommendCount u-marginLeft16"})
        clap = container_clap.button.contents
        print(clap)

        #Stores the scraped data into a dictionary
        scrapped_data = {
            'title': title,
            'text': text,
            'author' : author,
            'clap': clap
        }
        dict_article_data.append(scrapped_data)

    with open(file, 'w', encoding="utf-8") as f:        #Saves the file
        for item in dict_article_data:
            f.write("%s\n" % item)

    return dict_article_data

#Calls the functions
unique_links = find_articles_in_page(url_list)
final_articles = filter_links(unique_links)
scraped_articles = scrape_article(final_articles)
print(scraped_articles)
