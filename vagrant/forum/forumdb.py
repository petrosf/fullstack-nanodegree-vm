#
# Database access functions for the web forum.
# 
import psycopg2
import bleach

## Database connection

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.
    

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    
    #posts.sort(key=lambda row: row['time'], reverse=True)
    DB = psycopg2.connect("dbname=forum")
    cur = DB.cursor()

    query = "SELECT time,content FROM posts ORDER BY time DESC;"
    cur.execute(query)

    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in cur.fetchall()]

    DB.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    
    DB = psycopg2.connect("dbname=forum")
    cur = DB.cursor()

    clean_content = bleach.clean(content)
    cur.execute("INSERT INTO posts(content) VALUES(%s)",(clean_content,))

    DB.commit()
    DB.close()


