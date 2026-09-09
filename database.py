import mysql.connector

from config import Config

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="jeeva2325",
    database="fullstack_app"
)