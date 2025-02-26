import pymysql
import datetime

class DAO:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost', user='root', password='root', db='food_recommend', charset='utf8'
        )
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def execute(self, query, params=None):
        self.cur.execute(query, params or ())
        self.conn.commit()
        return self.cur.fetchall()

def insert_user(userName, userEmail, userPhone, userPassword, userDescription, userImg, userRole=0):
    userRole = 'admin' if userRole else 'normal'
    query = """
        INSERT INTO users (user_name, user_email, user_phone, user_password, user_description, user_img, user_role)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    dao = DAO()
    dao.execute(query, (userName, userEmail, userPhone, userPassword, userDescription, userImg, userRole))
    dao.close()

def insert_food(foodName, foodDescription, foodImg, foodPrice, foodType):
    query = """
        INSERT INTO foods (food_name, food_price, food_description, food_img, food_type)
        VALUES (%s, %s, %s, %s, %s)
    """
    dao = DAO()
    dao.execute(query, (foodName, foodPrice, foodDescription, foodImg, foodType))
    dao.close()

def insert_comment(foodID, userID, comment, rating):
    nowdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        INSERT INTO comments (food_id, user_id, comment, comment_date, rating)
        VALUES (%s, %s, %s, %s, %s)
    """
    dao = DAO()
    dao.execute(query, (foodID, userID, comment, nowdate, rating))
    dao.close()

def insert_wishlist(foodID, userID):
    nowdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        INSERT INTO wish_lists (food_id, user_id, add_date)
        VALUES (%s, %s, %s)
    """
    dao = DAO()
    dao.execute(query, (foodID, userID, nowdate))
    dao.close()

def get_foods():
    query = "SELECT food_id FROM foods"
    dao = DAO()
    foods = dao.execute(query)
    dao.close()
    return [
        {"food_id": row[0]} for row in foods
    ]

def get_users():
    query = "SELECT user_id FROM users"
    dao = DAO()
    users = dao.execute(query)
    dao.close()
    return [
        {"user_id": row[0]} for row in users
    ]

