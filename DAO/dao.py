import random
import pymysql
import datetime


class DAO:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host='localhost',
                user='root',
                password='root',
                db='food_recommend',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor  # 让查询返回字典
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Database connection failed!", e)
            self.conn = None

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def execute(self, query, params=None, many=False):
        """
        执行SQL语句，支持批量插入
        """
        try:
            if many and params:
                self.cur.executemany(query, params)
            else:
                self.cur.execute(query, params or ())
            self.conn.commit()
            return self.cur.fetchall()
        except Exception as e:
            print("SQL Execution Error:", e)
            return None


def get_user_by_id(user_id):
    """
    根据用户ID获取用户名
    """
    query = "SELECT user_name FROM users WHERE user_id = %s"
    dao = DAO()
    user = dao.execute(query, (user_id,))
    dao.close()
    return user[0]["user_name"] if user else "Anonymous"  # 避免返回None


def insert_user(userName, userEmail, userPhone, userPassword, userDescription, userImg, userRole=0):
    """
    插入用户数据
    """
    userRole = 'admin' if userRole else 'normal'
    query = """
        INSERT INTO users (user_name, user_email, user_phone, user_password, user_description, user_img, user_role)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    dao = DAO()
    dao.execute(query, (userName, userEmail, userPhone, userPassword, userDescription, userImg, userRole))
    dao.close()


def insert_food(foodName, foodDescription, foodImg, foodPrice, foodType):
    """
    插入美食数据
    """
    query = """
        INSERT INTO foods (food_name, food_price, food_description, food_img, food_type)
        VALUES (%s, %s, %s, %s, %s)
    """
    dao = DAO()
    dao.execute(query, (foodName, foodPrice, foodDescription, foodImg, foodType))
    dao.close()


def insert_comment(foodID, userID, comment, rating):
    """
    插入评论数据
    """
    nowdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_name = get_user_by_id(userID)  # 获取用户名称
    sentiment = random.randint(1, 6)  # 生成随机情感评分

    query = """
        INSERT INTO comments (food_id, user_id, comment, comment_date, rating, user_name, sentiment_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    dao = DAO()
    dao.execute(query, (foodID, userID, comment, nowdate, rating, user_name, sentiment))
    dao.close()


def insert_wishlist(foodID, userID):
    """
    插入愿望清单数据
    """
    nowdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
        INSERT INTO wish_lists (food_id, user_id, add_date)
        VALUES (%s, %s, %s)
    """
    dao = DAO()
    dao.execute(query, (foodID, userID, nowdate))
    dao.close()



def get_foods():
    """
    获取所有美食ID
    """
    query = "SELECT food_id FROM foods"
    dao = DAO()
    foods = dao.execute(query)
    dao.close()
    return [{"food_id": row["food_id"]} for row in foods] if foods else []


def get_users():
    """
    获取所有用户ID
    """
    query = "SELECT user_id FROM users"
    dao = DAO()
    users = dao.execute(query)
    dao.close()
    return [{"user_id": row["user_id"]} for row in users] if users else []


