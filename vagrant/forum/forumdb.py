# "Database code" for the DB Forum.

import psycopg2
import bleach

DBNAME = "forum"

def get_posts():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select content, time from posts order by time desc")
  posts = c.fetchall()
  db.close()
  return posts

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  # sanitize input with bleach to avoid script injection attack
  content = bleach.clean(content)
  # We substitute %s with a python tuple (hence the comma) to avoid
  # SQL injection attacks.
  c.execute("insert into posts values (%s)", (content,))
  # Code to replace spam with a message
  # % means any string can go there
  # c.execute(
  #   "update posts set content = 'This spam message has been deleted!' where content like '%Spam%'")
  db.commit()
  db.close()
