import requests
from bs4 import BeautifulSoup
from requests.api import head, post
from requests.models import Response

class Api:
    def __init__(self, cookie, userAgent):
        self.headers = {
            'cookie': cookie, 
            'user-agent': userAgent
            }

        response = requests.get(f'https://yougame.biz', headers=self.headers)

        soup = BeautifulSoup(response.text, 'lxml')

        self._xfToken = soup.find('input', {'name': '_xfToken'})['value']

    def getThreadInfo(self, thread_id: int):
        response = requests.get(f'https://yougame.biz/threads/{thread_id}/', headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('h1', class_='p-title-value').text.replace("\xa0", " | ")
        createTime = soup.find('time', class_='u-dt').text
        creator = soup.find('h4', class_='message-name').text
        text = soup.find('div', class_='bbWrapper').text
        try: 
            pages = soup.find_all('li', class_='pageNav-page')[-1].text
        except:
            pages = 1
        back = {"title": title, "time": createTime, "creator": creator, "text": text, "pages": pages}
        return back
    
    def getPosts(self, thread_id: int, page: int):
        if page == 1:
            seen = ""
        else:
            seen = f'page-{page}'
        response = requests.get(f'https://yougame.biz/threads/{thread_id}/{seen}', headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.find_all('article', class_='message--post')
        
        posts = []
        
        for i in range(len(articles)):
            text = articles[i].find('article', class_='message-body').text
            username = articles[i].find('h4', class_='message-name').text
            creationTime = articles[i].find('time', class_='u-dt').text
            post_id = articles[i]['data-content'].split('-')[1]
            member_id = articles[i].find('h4', class_='message-name').find('a', class_='username')['data-user-id']
            posts.append({"username": username, "text": text, "creationTime": creationTime, "post_id": post_id, "member_id": member_id})
        return posts

    def createPost(self, thread_id, message_html):
        requests.post(f'https://yougame.biz/threads/{thread_id}/add-reply', headers=self.headers, data={
            '_xfToken': self._xfToken,
            'message_html': message_html
        })

    def editPost(self, post_id: int, new_html):
        requests.post(f'https://yougame.biz/posts/{post_id}/edit', headers=self.headers, data={
          '_xfToken': self._xfToken,
          'message_html': new_html
        })

    def createThread(self, forum_id: int, title: str, message_html):
        requests.post(f'https://yougame.biz/forums/{forum_id}/post-thread', headers=self.headers, data={
          '_xfToken': self._xfToken,
          'title': title,
          'message_html': message_html
        })

    def editThread(self, thread_id: int, title: str, message_html):
        response = requests.get(f'https://yougame.biz/threads/{thread_id}/', headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')

        post_id = soup.find('article')['data-content'].split('-')[1]
        requests.post(f'https://yougame.biz/posts/{post_id}/edit', headers=self.headers, data={
            '_xfToken': self._xfToken,
            'title': title,
            'message_html': message_html
        })

    def likePost(self, post_id: int, reaction_id: int):
        requests.post(f'https://yougame.biz/posts/{post_id}/react?reaction_id={reaction_id}', headers=self.headers, data={
            '_xfToken': self._xfToken
        })

    def getThreads(self, forum_id: int, page: int):
        if page == 1:
            seen = ""
        else:
            seen = f"page-{page}"
        response = requests.get(f'https://yougame.biz/forums/{forum_id}/{seen}', headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')

        threads = soup.find_all('div', class_='structItem--thread')
        
        returned = []
        
        for i in range(len(threads)):
            creator = threads[i].find('a', class_='username').text
            title = threads[i].find('div', class_='structItem-title').text
            href = threads[i].find('div', class_='structItem-title').find_all('a')[-1]['href']
            returned.append({"creator": creator, "title": title, "href": href})
        return returned