# Webmention Receiver Endpoint & Sending Client

## Use

Create `gunicorn.conf.py`:

    bind = "0.0.0.0:8010"
    workers = 1
    worker_class = "gevent"

Then run:

    web serve webmention

A webmention endpoint server will start at port `8010` and received mentions
will be stored in the SQLite database `web-Webmention.db`.

You should put that server behind Caddy or Nginx.

You may then query the webmentions multiple ways:

### Command Line Interface

    $ mentions from friendsdomain.com
    {
        'content': 'yo',
        'mention-of': 'yourdomain.com/posts/2021/035/3'
    }

### Python Local Client

    >>> from understory import web
    >>> receiver = web.indie.webmention.LocalClient()
    >>> receiver.from_domain("friendsdomain.com")[0]
    {
        'content': 'yo',
        'mention-of': 'yourdomain.com/posts/2021/035/3'
    }

### Python Remote API

    >>> from understory import web
    >>> web.get("http://0.0.0.0:8010/?source=friendsdomain.com").json
    {
        'type': 'feed',
        'name': 'Webmentions',
        'children': [
            {
                'content': 'yo',
                'mention-of': 'yourdomain.com/posts/2021/035/3'
            }
    }

### SQLite via Python ORM

    >>> from understory import sql
    >>> db = sql.db("web-Webmention.db")
    >>> db.select("mentions", where="source LIKE ?",
    ...           vals=["friendsdomain.com%"])[0]["mention"]
    {
        'content': 'yo',
        'mention-of': 'yourdomain.com/posts/2021/035/3'
    }
