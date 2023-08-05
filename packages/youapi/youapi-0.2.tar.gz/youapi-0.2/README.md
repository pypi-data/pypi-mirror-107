## Установка:

```
pip install youapi
```

## Примеры:

* **Информация о теме**
  ```
  from pyyouapi import youapi

  client = youapi.Api(cookie, useragent)

  print(client.getThreadInfo(thread_id))
  ```

## Список методов

* **getThreadInfo(thread_id: int)** - *Информация о теме*

* **getPosts(thread_id: int, page: int)** - *Получить сообщения в теме*

* **createPost(thread_id, message_html)** - *Написать в тему*

* **editPost(post_id: int, new_html)** - *Редактировать сообщение в теме*

* **createThread(forum_id: int, title: str, message_html)** - *Создать тему&

* **editThread(thread_id: int, title: str, message_html)** - *Редактировать тему*

* **likePostlikePost(post_id: int, reaction_id: int)** - *Лайкнуть пост*

* **getThreads(forum_id: int, page: int)** - *Список тем раздела*