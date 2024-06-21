import requests
from bs4 import BeautifulSoup
import psycopg2

# Define the URL of the blog to scrape
BLOG_URL = 'https://www.python.org/blogs/'

def scrape_blog_data():
    response = requests.get(BLOG_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    blogs = []

    for item in soup.find_all('article'):
        title = item.find('h2').text.strip()
        link = item.find('a')['href']
        date = item.find('time')['datetime']
        blogs.append((title, link, date))

    return blogs

def save_to_db(blogs):
    try:
        # Connect to your postgres DB
        connection = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='123456',
            host='psql-db',
            port='5432'
        )
        cursor = connection.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blogs (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                link TEXT,
                date TIMESTAMP
            );
        ''')

        # Insert blog data into the table
        for blog in blogs:
            cursor.execute('''
                INSERT INTO blogs (title, link, date)
                VALUES (%s, %s, %s);
            ''', blog)

        connection.commit()
        cursor.close()
        connection.close()
        print("Data saved successfully")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    blogs = scrape_blog_data()
    save_to_db(blogs)
