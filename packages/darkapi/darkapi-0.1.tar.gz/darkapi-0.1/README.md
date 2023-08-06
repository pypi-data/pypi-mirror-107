## Установка:

```
pip install darkapi
```

## Примеры:

* **Информация о теме**
  ```
  from pydarkapi import darkapi

  api = darkapi.Api(cookie, useragent)

  print(api.getThreadInfo(thread_id))
  ```

## Список методов

* **getThreadInfo(thread_id: int)** - *Информация о теме*

* **getPosts(thread_id: int, page: int)** - *Получить сообщения в теме*

* **createPost(thread_id, message_html)** - *Написать в тему*

* **editPost(post_id: int, new_html)** - *Редактировать сообщение в теме*

* **createThread(forum_id: int, title: str, message_html)** - *Создать тему*

* **editThread(thread_id: int, title: str, message_html)** - *Редактировать тему*