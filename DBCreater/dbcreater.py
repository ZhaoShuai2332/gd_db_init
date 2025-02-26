import pymysql
import random
from DAO import dao
import pandas as pd
import numpy as np

comment_df = pd.read_csv('D://projects//gd_db_init//data//dealed_data//translated_comment.csv')
user_df = pd.read_csv('D://projects//gd_db_init//data//dealed_data//users.csv')
food_df = pd.read_csv('D://projects//gd_db_init//data//dealed_data//translated_food.csv')

db = dao.DAO()

# insert user
def insertUser():
    for index, row in user_df.iterrows():
        userName = row['Username']
        userEmail = row['Email']
        userPhone = row['Phone']
        userPassword = "123456"
        userDescription = "null"
        userImg = "null"
        userRole = 0
        dao.insert_user(userName, userEmail, userPhone, userPassword, userDescription, userImg, userRole)

# insert food
def insertFood():
    for index, row in food_df.iterrows():
        foodName = row['foodname']
        foodDescription = row['recommend']
        foodImg = row['imgurl']
        foodPrice = row['price']
        foodType = row['foodtype']
        dao.insert_food(foodName, foodDescription, foodImg, foodPrice, foodType)

# insert comment
def insertRandomComments():
    food_ids = [food['food_id'] for food in dao.get_foods()]
    user_ids = [user['user_id'] for user in dao.get_users()]

    for index, row in comment_df.iterrows():
        foodID = random.choice(food_ids)
        userID = random.choice(user_ids)
        comment = row['text']
        rating = row['label']
        dao.insert_comment(foodID, userID, comment, rating)


# Insert random wishlist items
def insertRandomWishlist():
    food_ids = [food['food_id'] for food in dao.get_foods()]
    user_ids = [user['user_id'] for user in dao.get_users()]

    for _ in range(len(user_ids) * 7):  # Each user might have multiple wishlist items
        foodID = random.choice(food_ids)
        userID = random.choice(user_ids)
        dao.insert_wishlist(foodID, userID)


if __name__ == '__main__':
    # insertUser()
    insertFood()
    insertRandomComments()
    insertRandomWishlist()

