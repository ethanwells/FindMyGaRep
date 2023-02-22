import requests
import mysql.connector
import json
import datetime


def geocodioTest(testmode):
    print("test geocodio, two way data pass functionality")
    url = "https://obscure-beyond-79368.herokuapp.com/get_rep_info"
    params = {
        "streetAddress": "200 River Vista Dr Atlanta Dr",
        "zipcode": "30339"
    }
    r = requests.get(url, params=params)
    print("here!", r)
    expected = "{\"name\": \"Deborah Silcox\", \"party\": \"Republican\", \"email\": \"deborah.silcox@house.ga.gov\", \"district\": 53}"
    
    if testmode:
        assert(r.text == expected)
        print(" -> SUCCESS")
    repname = json.loads(r.text)["name"]
    repparty = json.loads(r.text)["party"]
    repemail = json.loads(r.text)["email"]
    repdistrict = json.loads(r.text)["district"]
    return repname, repdistrict, repparty, repemail


def remoteDBTest(repdata, username, useraddress):
    repname = repdata[0]
    repdistrict = repdata[1]
    repparty = repdata[2]
    repemail = repdata[3]
    now = datetime.datetime.now()

    # Connect to the remote database
    mydb = mysql.connector.connect(
      host="us-cdbr-east-06.cleardb.net",
      user="bfcd3fe3c5a8f6",
      password="0daf2e76",
      database="heroku_4fdb36266c50912"
    )
    print(mydb)

    # Insert values into the users table
    try:
        mycursor = mydb.cursor()
        sql = "INSERT INTO users (district, fullname, address) VALUES (%s, %s, %s)"
        val = (str(repdistrict), username, useraddress)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted into users table.")
    except:
        print("caught duplicate")
    

    # Insert values into the reps table
    try: 
        mycursor = mydb.cursor()
        sql = "INSERT INTO reps (fullname, district, party, email) VALUES (%s, %s, %s, %s)"
        val = (repname, str(repdistrict), repparty, repemail)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted into reps table.")
    except:
        print("caught duplicate")

    # Insert values into the sessions table
    mycursor = mydb.cursor()
    sql = "SELECT user_id FROM users WHERE fullname = %s AND address = %s"
    val = (username, useraddress)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        user_id = result[0]
        print("user_id: ", user_id)
        # Check if the district exists in the reps table
        sql = "SELECT * FROM reps WHERE district = %s"
        val = (repdistrict,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        if result:
            sql = "INSERT INTO sessions (start_time, user_id, district) VALUES (%s, %s, %s)"
            val = (str(now), user_id, str(repdistrict))
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted into sessions table.")
        else:
            print("ERROR: No district found in the reps table.")
            exit()
    mydb.commit()
    print(mycursor.rowcount, "record inserted into sessions table.")

    # Update sessions_count element for each user in user table
    # Update the sessions_count column in the users table
    mycursor = mydb.cursor()
    sql = """
        UPDATE users 
        SET sessions_count = (
            SELECT COUNT(*) 
            FROM sessions 
            WHERE sessions.user_id = users.user_id
        )
    """
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "users updated")







#('Deborah Silcox', 53, 'Republican', 'deborah.silcox@house.ga.gov')

geocodioTest(True)
remoteDBTest(geocodioTest(False), "ethan wells", "6545 whispering lane")


#print(r.text)
