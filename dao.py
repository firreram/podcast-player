import sqlite3

def get_series():
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  
  sql = 'SELECT * FROM series, users WHERE series.creator_id = users.id'
  
  cursor.execute(sql)
  series = cursor.fetchall()
  
  cursor.close()
  conn.close()

  return series

def get_userbyid(id):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM users where id = ?'
    cursor.execute(sql, (id,))
    user = cursor.fetchone()
  
    cursor.close()
    conn.close()

    return user

def add_user(user):

    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO users(id, username, password, is_creator, userimg) VALUES(?,?,?,?,?)'

    try:
        cursor.execute(
            sql, (user['id'], user['username'], user['password'], user['is_creator'], user['userimg']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def add_serie(serie, user):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  success = False
  sql = 'INSERT INTO series(title, description, category, serie_img, creator_id) VALUES (?, ?, ?, ?, ?)'

  try:
    cursor.execute(sql, (serie['title'], serie['description'], serie['category'], serie['serie_img'], user))
    conn.commit()
    success = True
  except Exception as e:
    print('ERROR', str(e))
    conn.rollback()

  cursor.close()
  conn.close()

  return success

def add_episode(episode, sid, date):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  success = False
  sql = 'INSERT INTO episodes(title, description, date, audiofile, sid) VALUES (?, ?, ?, ?, ?)'

  try:
    cursor.execute(sql, (episode['title'], episode['description'], date, episode['episode_audio'], sid))
    conn.commit()
    success = True
  except Exception as e:
    print('ERROR', str(e))
    conn.rollback()

  cursor.close()
  conn.close()

  return success

def add_comment(user_id, newcomment, episode_id, date):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  success = False
  sql0 = 'SELECT username FROM users WHERE id = ?'
  sql1 = 'INSERT INTO comments(eid, username, content, date) VALUES (?, ?, ?, ?)'
  print('ok')
  try:
    cursor.execute(sql0, (user_id, ))
    user_name = cursor.fetchone()
    cursor.execute(sql1, (episode_id, user_name['username'], newcomment['text'], date))
    conn.commit()
    
    success = True
  except Exception as e:
    print('ERROR', str(e))
    conn.rollback()

  cursor.close()
  conn.close()

  return success

def add_follower(user, serie):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'INSERT INTO users_follows(user_id, sid) VALUES (?, ?)'

  try:
    cursor.execute(sql, (user, serie))
    conn.commit()
  except Exception as e:
    print('ERROR', str(e))
    conn.rollback()

  cursor.close()
  conn.close()

  return

def get_serie(id):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'SELECT * FROM series WHERE id = ?'
  cursor.execute(sql, (id,))
  serie = cursor.fetchone()

  cursor.close()
  conn.close()

  return serie

def get_episodes(id):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'SELECT * FROM episodes WHERE episodes.sid = ? ORDER BY date'
  cursor.execute(sql, (id,))
  episodes = cursor.fetchall()

  cursor.close()
  conn.close()

  return episodes

def get_episode(id):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'SELECT * FROM episodes WHERE id = ?'
  cursor.execute(sql, (id,))
  episode = cursor.fetchone()

  cursor.close()
  conn.close()

  return episode

def get_firstepisode(id):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'SELECT * FROM episodes WHERE id = ?'
  cursor.execute(sql, (id,))
  episode = cursor.fetchone()

  cursor.close()
  conn.close()

  return episode

def get_comments(id):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'SELECT * FROM comments WHERE comments.eid = ? ORDER BY date'
  cursor.execute(sql, (id,))
  comments = cursor.fetchall()

  cursor.close()
  conn.close()

  return comments

def update_comment(id, content):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = 'UPDATE comments SET content = ? WHERE id = ?'

    try:
      cursor.execute(sql, (content, id))
      conn.commit()
    except Exception as e:
      print('ERROR', str(e))
      conn.rollback()

    cursor.close()
    conn.close()

    return 

def delete_comment(id):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'DELETE FROM comments WHERE id = ?'

  try:
    cursor.execute(sql, (id, ))
    conn.commit()
  except Exception as e:
    print('ERROR', str(e))
    conn.rollback()

  cursor.close()
  conn.close()

  return

def update_serie(id, title, description):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = 'UPDATE series SET title = ?, description = ? WHERE id = ?'

    try:
      cursor.execute(sql, (title, description, id))
      conn.commit()
    except Exception as e:
      print('ERROR', str(e))
      conn.rollback()

    cursor.close()
    conn.close()

    return

def delete_serie(id):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'DELETE FROM series WHERE id = ?'

  try:
    cursor.execute(sql, (id, ))
    conn.commit()
  except Exception as e:
    print('ERROR', str(e))
    conn.rollback()

  cursor.close()
  conn.close()

  return

def update_episode(id, title, description):
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = 'UPDATE episodes SET title = ?, description = ? WHERE id = ?'

    try:
      cursor.execute(sql, (title, description, id))
      conn.commit()
    except Exception as e:
      print('ERROR', str(e))
      conn.rollback()

    cursor.close()
    conn.close()

    return

def delete_episode(id):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'DELETE FROM episodes WHERE id = ?'

  try:
    cursor.execute(sql, (id, ))
    conn.commit()
  except Exception as e:
    print('ERROR', str(e))
    conn.rollback()

  cursor.close()
  conn.close()

  return

def get_followed_series(id):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'SELECT * FROM series,users_follows WHERE series.id=users_follows.sid AND users_follows.user_id = ?'
  cursor.execute(sql, (id,))
  series = cursor.fetchall()

  cursor.close()
  conn.close()

  return series

def check_follow(user, id):

    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'SELECT user_id FROM users_follows WHERE sid = ?'

    cursor.execute(sql, (id, ))
    db_list = [p[0] for p in cursor]
    if user in db_list:  
      success = True

    cursor.close()
    conn.close()

    return success

def remove_follower(user, serie):
  conn = sqlite3.connect('db/database.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  sql = 'DELETE FROM users_follows WHERE user_id = ? AND sid = ?'

  try:
    cursor.execute(sql, (user, serie))
    conn.commit()
  except Exception as e:
    print('ERROR', str(e))
    conn.rollback()

  cursor.close()
  conn.close()

  return
  