
from contextlib import contextmanager
import logging
import os

from flask import current_app, g

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 10, dsn=DATABASE_URL, sslmode='require')

    make_table()


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

def make_table():
    with get_db_cursor(True) as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                       posts(id SERIAL, 
                             user_id VARCHAR(128) NOT NULL, 
                             title VARCHAR(64) NOT NULL, 
                             content TEXT NOT NULL, 
                             category VARCHAR(64) NOT NULL, 
                             post_date TIMESTAMP NOT NULL default CURRENT_TIMESTAMP, 
                             post_type VARCHAR(16) NOT NULL, 
                             likes INT NOT NULL DEFAULT 0, 
                             PRIMARY KEY (id))""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                       posts_sub_categories(post_id INT NOT NULL, 
                                            sub_category_title VARCHAR(64) NOT NULL, 
                                            PRIMARY KEY (post_id, sub_category_title), 
                                            FOREIGN KEY (post_id) REFERENCES posts(id))""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                       post_comments(id SERIAL NOT NULL, 
                                     user_id VARCHAR(128) NOT NULL, 
                                     post_id INT NOT NULL, 
                                     content TEXT NOT NULL, 
                                     post_date TIMESTAMP NOT NULL default CURRENT_TIMESTAMP,
                                     revision_date TIMESTAMP, 
                                     likes INT NOT NULL DEFAULT 0, 
                                     PRIMARY KEY (id))""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                       category(title VARCHAR(64) NOT NULL, 
                                description TEXT, 
                                photo VARCHAR(256), 
                                PRIMARY KEY (title))""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                       sub_category(parent_title VARCHAR(64) NOT NULL, 
                                    subtitle VARCHAR(64) NOT NULL, 
                                    photo VARCHAR(256), 
                                    PRIMARY KEY (parent_title, subtitle), 
                                    FOREIGN KEY (parent_title) REFERENCES category(title))""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                       users(user_id VARCHAR(128) NOT NULL, 
                             username VARCHAR(32) NOT NULL, 
                             photo_url VARCHAR(256), 
                             bio TEXT, 
                             PRIMARY KEY (user_id))""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                       user_followers(user_id VARCHAR(128) NOT NULL, 
                                      follower_id VARCHAR(128) NOT NULL, 
                                      PRIMARY KEY (user_id, follower_id), 
                                      FOREIGN KEY (user_id) REFERENCES users(user_id))""")
        
        cur.execute("""CREATE TABLE IF NOT EXISTS 
                       post_likes(post_id INT NOT NULL, 
                                  user_id VARCHAR(128) NOT NULL, 
                                  PRIMARY KEY (post_id, user_id), 
                                  FOREIGN KEY (user_id) REFERENCES users(user_id))""")

def add_post(title, content, category, user_id, post_type):
    with get_db_cursor(True) as cur:
        cur.execute("""INSERT INTO posts (title, content, category, user_id, post_type) 
                       values (%s, %s, %s, %s, %s)""", 
                       (title, content, category, user_id, post_type))

# def get_recent_posts(limit=5, page=0, type="POST"):
#     with get_db_cursor(True) as cur:
#         cur.execute("SELECT title, content, category, post_date, likes, username, photo_url FROM posts, users WHERE post_type = %s AND posts.user_id = users.user_id ORDER BY id desc LIMIT %s OFFSET %s", (type, limit, page*limit))
#         return cur.fetchall()

# updated version includes comment count
def get_recent_posts(limit=5, page=0, type="POST"):
    with get_db_cursor(True) as cur:
        cur.execute("""select posts.title, posts.content, posts.category, posts.post_date, count(post_likes.post_id) as likes, 
                       users.username, users.photo_url, count(post_comments.post_id) as comments, posts.id 
                       FROM posts left outer join users on users.user_id = posts.user_id 
                       left outer join post_comments on post_comments.post_id = posts.id 
                       left outer join post_likes on post_likes.post_id = posts.id 
                       WHERE posts.post_type = %s group by posts.id, username, photo_url 
                       order by posts.id desc limit %s offset %s""", 
                       (type, limit, page*limit))
        return cur.fetchall()

#gets posts by category
def get_recent_posts_by_category(category, limit=1, page=0, type="POST"):
    with get_db_cursor(True) as cur:
        cur.execute("""select posts.title, posts.content, posts.category, posts.post_date, count(post_likes.post_id) as likes, 
                       users.username, users.photo_url, count(post_comments.post_id) as comments 
                       FROM posts left outer join users on users.user_id = posts.user_id 
                       left outer join post_comments on post_comments.post_id = posts.id 
                       left outer join post_likes on post_likes.post_id = posts.id 
                       WHERE posts.category = %s and posts.post_type = %s group by posts.id, username, photo_url 
                       order by posts.id desc limit %s offset %s""", 
                       (category, type, limit, page*limit))
        return cur.fetchall()
    
#gets posts by user
def get_recent_posts_by_user(username, limit=5, page=0, type="POST"):
    with get_db_cursor(True) as cur:
        cur.execute("""select posts.title, posts.content, posts.category, posts.post_date, count(post_likes.post_id) as likes, 
                       users.username, users.photo_url, count(post_comments.post_id) as comments, posts.id
                       FROM posts left outer join users on users.user_id = posts.user_id 
                       left outer join post_comments on post_comments.post_id = posts.id 
                       left outer join post_likes on post_likes.post_id = posts.id 
                       WHERE posts.post_type = %s and users.username = %s group by posts.id, username, photo_url 
                       order by posts.id desc limit %s offset %s""", 
                       (type, username, limit, page*limit))
        return cur.fetchall()

def get_post_count_by_user(user_id):
    with get_db_cursor(True) as cur:
        cur.execute("SELECT COUNT(*) FROM posts WHERE user_id= %s", (user_id, ))
        return cur.fetchone()    
# def get_discussion_count(type="DISCUSSION"):
#     with get_db_cursor(True) as cur:
#         cur.execute("SELECT COUNT(*) FROM posts WHERE post_type = %s", (type,))
#         return cur.fetchall()
    
def add_user(user_id, username):
    with get_db_cursor(True) as cur:
        cur.execute("INSERT INTO users (user_id, username) values (%s, %s)", (user_id, username))

def get_user_by_id(user_id):
    with get_db_cursor(True) as cur:
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        return cur.fetchall()


# def get_recent_discussion(limit=5, page=0, type="DISCUSSION"):
#     with get_db_cursor(True) as cur:
#         cur.execute("SELECT title, content, category, post_date, likes, username, photo_url FROM posts, users WHERE post_type = %s AND posts.user_id = users.user_id ORDER BY id desc LIMIT %s OFFSET %s", (type, limit, page))
#         return cur.fetchall()

def get_post_by_title(title, type="POST"):
    with get_db_cursor(True) as cur:
        cur.execute("SELECT title, content, category, username FROM posts, users WHERE post_type = %s AND title = %s AND posts.user_id = users.user_id", (type, title))
        return cur.fetchone()
    
# returns sub_category_title, count, parent_title in order of most trending first
def get_trending_sub_categories(type='POST', limit=5):
    with get_db_cursor(True) as cur:
        cur.execute("""select sub_category_title, count(*), parent_title 
                       from posts_sub_categories, posts, sub_category 
                       where post_id = id and subtitle = sub_category_title and post_type = %s 
                       group by sub_category_title, parent_title 
                       order by count desc limit %s""", 
                       (type, limit))
        return cur.fetchall()
    
def update_user_bio(user_id, bio):
    with get_db_cursor(True) as cur:
        cur.execute('UPDATE users SET bio=%s where user_id=%s',(bio, user_id,))
        cur.connection.commit()

def update_user_img(photo_url, user_id):
    with get_db_cursor(True) as cur:
        cur.execute("UPDATE users SET photo_url = %s WHERE user_id = %s", (photo_url, user_id))
        cur.connection.commit()


def search_by_category(category, limit=5, page=0):
    with get_db_cursor(False) as cur:
        category = category.lower()
        query = "%" + category + "%"
        cur.execute("""select posts.title, posts.content, posts.category, posts.post_date, count(post_likes.post_id) as likes, 
                       users.username, users.photo_url, count(post_comments.post_id) as comments 
                       FROM posts left outer join users on users.user_id = posts.user_id 
                       left outer join post_comments on post_comments.post_id = posts.id 
                       left outer join post_likes on post_likes.post_id = posts.id 
                       WHERE lower(posts.category) like %s group by posts.id, username, photo_url 
                       order by posts.id desc limit %s offset %s""", 
                       (query, limit, page*limit))
        return cur.fetchall()
        
#db functions for getting likes
def get_likes(post_id):
    with get_db_cursor(False) as cur:
        cur.execute("select count(*) from post_likes where post_id = %s", (post_id,))
        counts = cur.fetchone()
        return counts[0]

def get_does_like(post_id, user_id):
    with get_db_cursor(False) as cur:
        ### Again -- this should really be done with the above in one request. terrible form that it isn't.
        cur.execute("select count(*) from post_likes where post_id = %s and user_id=%s", (post_id,user_id))
        counts = cur.fetchone()
        return counts[0]!=0

def unlike_post(post_id, user_id):
    with get_db_cursor(True) as cur:
        cur.execute("""delete from post_likes where post_id=%s and user_id = %s""" , (post_id, user_id,))

def get_post_by_id(post_id):
    with get_db_cursor(True) as cur:
        cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        return cur.fetchone()



def search_post_type_full_text_content(query, post_type, page=0, limit=5):
    with get_db_cursor(False) as cur:
        cur.execute("""select * from posts
                       WHERE to_tsvector('english', raw_text) @@ plainto_tsquery('english', %s)
                       AND lower(post_type) = %s
                       order by ts_rank(to_tsvector('english', raw_text), plainto_tsquery('english', %s)) desc
                       limit %s offset %s""",
                       (query, post_type, query, limit, limit*page))
        return cur.fetchall()


def get_comments_by_post_id(post_id):
    with get_db_cursor(True) as cur:
        cur.execute("SELECT * FROM post_comments WHERE post_id = %s", (post_id,))
        return cur.fetchall()
 
def add_comment( user_id, post_id, content):
    with get_db_cursor(True) as cur:
        cur.execute("INSERT INTO post_comments (user_id, post_id, content) values (%s, %s, %s)", (user_id, post_id, content))

