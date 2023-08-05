import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import xml.etree.ElementTree as ET


class GoogleNews:
    """
    Create an instance of `GoogleNews` class.
    ```python
    articles = GoogleNews()
    ```
    | Methods                | Details                                                                                          |
    | ---------------------- | ------------------------------------------------------------------------------------------------ |
    | `.getArticles(topic="github")`       | Returns the list of articles with title, descriptions, news source, date and link in JSON format |
    | `.top_stories()`       | Returns the list of top stories listed regarding the mentioned topic                             |
    | `.timed_aticles(time)` | Returns the list of top stories listed regarding the mentioned topic and within that time frame  |
    | `.bylanguage(lang)`    | Returns the list of top stories listed regarding the mentioned topic in the specified language   |
    | `.bynumerofdaysback(number)` | Returns the list of stories listed regarding the mentioned topic by given number of days back from the current day  |
    | `.bylocation(countryname)` | Returns the list of top stories listed of the specified country or geolocation               |

    """

    def __init__(self):
        pass

    def get_articles(self, topic: str):
        """
        Class - `GoogleNews`
        Example:
        ```python
        articles = GoogleNews()
        articles.get_articles(topic="github")
        ```
        Parameters required  -  `topic`\n
        Returns:
        ```js
        {
            "link": "Link to the article",
            "title": "Tile of the article",
            "date": "Date the article was posted",
        }
        ```
        """
        url = "https://news.google.com/rss/search?q=" + topic
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, features="xml")
            # find all li tags
            lis = soup.find_all("item")
            sub_articles = []
            for li in lis:
                sub_articles.append(
                    {
                        "link": li.link.text,
                        "title": li.title.text,
                        "Date & Time": li.pubDate.text,
                    }
                )
            return sub_articles[:8]
        except:
            return None

    def top_stories(self):
        """
        Class - `GoogleNews`
        Example:
        ```python
        articles = GoogleNews()
        articles.top_stories()
        ```
        Returns:
        ```js
        [
            {
                "link": "Link of the news",
                "title": "Title of the top story",
                "date": "Date of the top story"
            },
            ...
        ]
        ```
        """
        url = "https://news.google.com/news/rss"
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, features="xml")
            lis = soup.find_all("item")
            sub_articles = []
            for li in lis:
                sub_articles.append(
                    {
                        "link": li.link.text,
                        "title": li.title.text,
                        "Date & Time": li.pubDate.text,
                    }
                )
            return sub_articles
        except:
            return None

    def timed_articles(self, topic: str, time="1h"):
        """
        Class - `GoogleNews`
        Example:
        ```python
        articles = GoogleNews(topic="github")
        articles.timed_articles(time)
        ```
        Parameter required - `topic` and `time`\n
        Time format: \n
        + 1h - within 1 hour (default)
        + 1d - within 24 hours
        + 7d - within a week
        + 1y - within a year
        Returns:
        ```js
        [
            {
                "link": "Link of the news",
                "title": "Title of the top story",
                "date": "Date of the top story"
            },
            ...
        ]
        ```
        """
        if time != "":
            time = " when:" + time
        url = "https://news.google.com/news/rss/search?q=" + topic + time
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, features="xml")
            lis = soup.find_all("item")
            sub_articles = []
            for li in lis:
                sub_articles.append(
                    {
                        "link": li.link.text,
                        "title": li.title.text,
                        "Date & Time": li.pubDate.text,
                    }
                )
            return sub_articles
        except:
            return None

    def bynumberofdaysback(self, topic: str, number: int):
      """
        Class - `GoogleNews`
        Example:
        ```python
        articles = GoogleNews()
        articles.bynumberofdaysback(topic="github",number)
        ```
        Parameters required  -  `topic` and `number`\n
        Returns:
        ```js
        {
            "link": "Link to the article",
            "title": "Tile of the article",
            "date": "Date the article was posted",
        }
        ```
      """

      number = int(number)
      x =pd.datetime.today()
      temp_time = str(x + pd.Timedelta(days=-int(number)))[:10]
      today =str(x)[:10]
      time =  'after%3A'+ temp_time + '+before%3A' + today


      url = "https://news.google.com/news/rss/search?q=" + topic + time

      try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, features="xml")
        lis = soup.find_all("item")
        sub_articles = []
        for li in lis:
          sub_articles.append(
              {
                  
                  "link": li.link.text,
                  "title": li.title.text,
                  "Date & Time": li.pubDate.text,
              }
          )
        return sub_articles

      except:
        return None


    def bylanguage(self, topic: str, language: str):
      """
        Class - `GoogleNews`
        Example:
        ```python
        articles = GoogleNews()
        articles.bylanguage(topic="github",language:"en")
        ```
        Parameters required  -  `topic` and `language`\n
        Returns:
        ```js
        {
            "link": "Link to the article",
            "title": "Tile of the article",
            "date": "Date the article was posted",
        }
        ```
      """

      if len(language) >=3:
        return None

      addlang = '&hl='+language
      url = "https://news.google.com/news/rss/search?q=" + topic + addlang

      try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, features="xml")
        lis = soup.find_all("item")
        sub_articles = []
        for li in lis:
          sub_articles.append(
              {
                  
                  "link": li.link.text,
                  "title": li.title.text,
                  "Date & Time": li.pubDate.text,
              }
          )
        return sub_articles

      except:
        return None


    def bylocation(self, location: str):
      """
        Class - `GoogleNews`
        Example:
        ```python
        articles = GoogleNews()
        articles.bylocation(topic="github",location="Pakistan")
        ```
        Parameters required  -  `topic` and `location`\n
        Returns:
        ```js
        {
            "link": "Link to the article",
            "title": "Tile of the article",
            "date": "Date the article was posted",
        }
        ```
      """
      
      url = 'https://news.google.com/news/rss/headlines/section/geo/{}'.format(location)

      try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, features="xml")
        lis = soup.find_all("item")
        sub_articles = []
        for li in lis:
          sub_articles.append(
              {
                  
                  "link": li.link.text,
                  "title": li.title.text,
                  "Date & Time": li.pubDate.text,
              }
          )
        return sub_articles

      except:
        return None






