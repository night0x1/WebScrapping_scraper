# In this project we will attempt to extract the most recent articles
# related to cyber attacks
import csv
import requests
from bs4 import BeautifulSoup

def techcrunch():

    # Test out if we need the current url incase error
    base_url = 'https://techcrunch.com/page/1/?s=Hackers'
    current_url = base_url

    # Let's build the headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    }

    # Let's set up the request
    req = requests.get(current_url, headers=headers)

    if req.status_code == 200:
        print('Extracting data....')
    else:
        print(f'Error detected {req.status_code}')


    # let's create a dictionary that holds the information
    recent_cyber_articles = []

    while current_url:

        # Let's create the soup
        soup = BeautifulSoup(req.text, "html.parser")

        # Create for loop -> iterate the data we need to extract

        for articles in soup.find_all("div", class_="loop-card__content"):

            # Debugged the error on publish -> conduct fail safe switch
            author_tag = articles.find('a', class_='loop-card__author')
            title_tag = articles.find('a', class_='loop-card__title-link')
            publish_tag = articles.find('time', class_='loop-card__meta-item loop-card__time wp-block-tc23-post-time-ago')
            link_tag = articles.find('a', class_='loop-card__title-link')



            # Author -> Title -> Publish Date -> href
            author = author_tag.get_text(strip=True) if author_tag else None
            title = title_tag.get_text(strip=True) if title_tag else None
            publish = publish_tag.get_text(strip=True) if publish_tag else None
            link = link_tag['href'] if link_tag and link_tag.has_attr('href') else None


            # Store data
            recent_cyber_articles.append({
                'Author': author,
                'Title': title,
                'Publish': publish,
                'Link': link
            })

        # End the loop for now - we're not paginating yet
        break

    # --- Export Data To CSV ---
    with open("recent_cyber.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ['Author', 'Title', 'Publish', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(recent_cyber_articles)

    print(f"\n Extracted {len(recent_cyber_articles)} articles.")


techcrunch()
