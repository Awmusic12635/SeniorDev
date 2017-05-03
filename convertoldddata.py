import json, MySQLdb

# Database connection information
db = MySQLdb.connect(user="root", passwd="Wa3wqpn3hr", db="dradis")
outputFile = "old.json"

c = db.cursor(MySQLdb.cursors.DictCursor)


# Handle Users

c.execute("""SELECT * FROM student""")

for i in range(c.rowcount):
    row = c.fetchone()
    #print(row['ID'], row['username'], row['password'])


