from sqlite3 import connect

f = 'classes.db'

def get_classes():
    db = connect(f)
    c = db.cursor()
    res = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    res = [str(n[0]) for n in res]
    db.close()
    return res

def create_class(name):
    db = connect(f)
    c = db.cursor()
    c.execute('CREATE TABLE if NOT EXISTS %s(Category STRING, Percent INTEGER, Score STRING)' % (name))
    db.commit()
    db.close()

def get_class_info(table):
    db = connect(f)
    c = db.cursor()
    res = c.execute('SELECT * from %s' % (table)).fetchall()
    db.close()
    return res

def insert_category(table,category,percent,score):
    db = connect(f)
    c = db.cursor()
    c.execute('INSERT INTO %s VALUES(\"%s\",%d,\"%s\")' % (table,category,percent,score))
    db.commit()
    db.close()

def modify_category_entry(table,old_name,new_name,new_percent,new_score):
    db = connect(f)
    c = db.cursor()
    c.execute('UPDATE %s SET Category=\"%s\", Percent=%d, Score=\"%s\" WHERE Category==\"%s\"' % (table,new_name,new_percent,new_score,old_name))
    db.commit()
    db.close()

def delete_category_entry(table,category):
    db = connect(f)
    c = db.cursor()
    c.execute('DELETE from %s where Category==\"%s\"' % (table,category))
    db.commit()
    db.close()

def drop_class_table(name):
    db = connect(f)
    c = db.cursor()
    c.execute('DROP TABLE %s' % (name))
    db.commit()
    db.close()
    
#get_classes()
#print get_class_info('cse_214')

'''
f = 'database.db'
db = connect(f)
c = db.cursor()

c.execute("some command")


query = "SELECT ..."
res = c.execute(query)
'''


'''
db schema

tables (classes)

Category | Percent | Score

'''
