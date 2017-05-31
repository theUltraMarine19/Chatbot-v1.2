from CONSTANTS import db_constants
import psycopg2

hostname = db_constants.myConstants.hostname
username = db_constants.myConstants.username
password = db_constants.myConstants.password
database = db_constants.myConstants.database

def delete_data(table_name):
	sql = 'delete from '+table_name+';'
	conn = None
		# connect to the PostgreSQL database
	conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
		# create a new cursor
	cur = conn.cursor()
		# execute the INSERT statement
	cur.execute(sql)
		# commit the changes to the database
	conn.commit()
		# close communication with the database
	cur.close()

## Takes a topic_name and data which it stores in the database
def create_table(table_name,column_list):
	sql = 'create table '+table_name+'('
	for i in range(0,len(column_list)-1):
		sql = sql + column_list[i][0] + " "+column_list[i][1]+"["+str(column_list[i][2])+"],"

	sql = sql + column_list[-1][0] + " "+column_list[-1][1]+"["+str(column_list[-1][2])+"]);"
	conn = None
		# connect to the PostgreSQL database
	conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
		# create a new cursor
	cur = conn.cursor()
		# execute the INSERT statement
	cur.execute(sql)
		# commit the changes to the database
	conn.commit()
		# close communication with the database
	cur.close()

def delete_table(table_name):
	sql = 'drop table ' + table_name +';'
	conn = None
	# connect to the PostgreSQL database
	conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
	# create a new cursor
	cur = conn.cursor()
	# execute the INSERT statement
	cur.execute(sql)
	# commit the changes to the database
	conn.commit()
	# close communication with the database
	cur.close()


## Takes a topic_name and data which it stores in the database
def add_data(topic_name,data):
	sql = 'INSERT INTO topic_data VALUES(\''+str(topic_name)+'\',\''+str(data)+'\');'
	conn = None
		# connect to the PostgreSQL database
	conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
		# create a new cursor
	cur = conn.cursor()
		# execute the INSERT statement
	cur.execute(sql)
		# commit the changes to the database
	conn.commit()
		# close communication with the database
	cur.close()

def get_parent(topic_name):
	sql = 'select topic_name from topic_map where sub_topic like \''+str(topic_name)+'\';'
	conn = None
	# connect to the PostgreSQL database
	conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
	# create a new cursor
	cur = conn.cursor()
	# execute the INSERT statement
	cur.execute(sql)
	records = cur.fetchall()
	data = records[0]
	# commit the changes to the database
	conn.commit()
	# close communication with the database
	cur.close()
	return data[0]


## Given a topic_name we return the para corresponding to the topi_name
def get_data(topic_name):
	sql = 'select  para from topic_data where topic_name like \''+str(topic_name)+'\';'
	conn = None
		# connect to the PostgreSQL database
	conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
		# create a new cursor
	cur = conn.cursor()
		# execute the INSERT statement
	cur.execute(sql)
	records = cur.fetchall()
	data = records[0]
		# commit the changes to the database
	conn.commit()
		# close communication with the database
	cur.close()
	return data[0]

## Takes a parent topic and a subtopic as params and stores it in the database
def add_topic(topic, subtopic):
	conn = None
		# connect to the PostgreSQL database
	conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
		# create a new cursor
	cur = conn.cursor()
		# execute the INSERT statement

	sql = 'INSERT INTO topic_map VALUES(\''+topic+'\',\''+subtopic+'\');'
	cur.execute(sql)

		# commit the changes to the database
	conn.commit()
		# close communication with the database
	cur.close()

## Takes a topic as input and returns a list of strings as a sub topic
def get_subtopics(topic):

	conn = None

	conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
		# create a new cursor
	cur = conn.cursor()
		# execute the INSERT statement
	sql = 'select sub_topic from topic_map where topic_name like \''+topic+'\';'

	cur.execute(sql)
	
	records = cur.fetchall()

	sub_list = [rec[0] for rec in records]    
		# commit the changes to the database
	conn.commit()
		# close communication with the database
	cur.close()

	return sub_list

def get_all_sub_topics():
	conn = None

	conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
	# create a new cursor
	cur = conn.cursor()
	# execute the INSERT statement
	sql = 'select sub_topic from topic_map ;'

	cur.execute(sql)

	records = cur.fetchall()

	sub_list = [rec[0] for rec in records]
	# commit the changes to the database
	conn.commit()
	# close communication with the database
	cur.close()

	return sub_list