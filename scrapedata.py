import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape Amazon product reviews
def scrape_amazon_reviews(url, max_reviews=100):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    reviews = []

    for page in range(1, max_reviews // 10 + 1):
        page_url = f"{url}&pageNumber={page}"
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        review_elements = soup.find_all('div', {'data-asin': True})

        for review_element in review_elements:
            user_id = review_element['data-asin']
            product_id = review_element.find('a', class_='a-size-base a-link-normal')['href'].split('/')[-1]
            rating = float(review_element.find('span', class_='a-icon-alt').text.split()[0])
            timestamp = int(review_element.find('span', class_='a-time').find('data')['data-asin-time'])

            reviews.append({
                'userId': f'user_{len(reviews)}',
                'productId': product_id,
                'rating': rating,
                'timestamp': timestamp
            })

            if len(reviews) >= max_reviews:
                break

    return reviews

# Example URL for Amazon product reviews (replace with the actual product URL)
amazon_product_url = "https://www.amazon.com/product-reviews/your_product_id"

# Specify the maximum number of reviews to scrape
max_reviews_to_scrape = 100

# Scrape reviews
scraped_reviews = scrape_amazon_reviews(amazon_product_url, max_reviews_to_scrape)

# Convert the scraped data into a pandas DataFrame
df = pd.DataFrame(scraped_reviews)

# Display the DataFrame
print(df)
