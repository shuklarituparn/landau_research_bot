import os

from playhouse.postgres_ext import *
from datetime import datetime, timedelta
from dotenv import load_dotenv
import psycopg2

load_dotenv()
Database_name = os.getenv("DATABASE_NAME")
Database_user = os.getenv("DATABASE_USERNAME")
Database_pass = os.getenv("DATABASE_PASSWORD")
Database_port = os.getenv("DATABASE_PORT")
Database_host=os.getenv("DATABASE_HOST")
db = PostgresqlExtDatabase(Database_name, user=Database_user, password=Database_pass,port=Database_port, host=Database_host)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    userid = BigIntegerField(primary_key=True)
    usertoken = TextField(default="")
    email = TextField(default="")
    gigachat_token = TextField(default="")
    username = CharField(max_length=255)
    name = CharField(max_length=255)
    chromacollection = CharField(max_length=255)
    lastGen = DateTimeField(default=datetime.now())
    last_gen_gigachat = DateTimeField(default=datetime.now())

    class Meta:
        table_name = "user"


def checking_user_exits(user_id: int) -> bool:
    try:
        User.get(User.userid == user_id)
        return True
    except DoesNotExist:
        return False


def checking_user_email_exits(user_id: int) -> str:
    try:
        email = User.get(User.userid == user_id).email
        return email
    except DoesNotExist:
        return ""


def checking_last_gen_time(user_id: int) -> bool:
    try:
        time_from_db = User.get(User.userid == user_id).lastGen
        current_time = datetime.now()
        timedifference = current_time - time_from_db
        if timedifference >= timedelta(minutes=30):
            return True
        else:
            return False

    except DoesNotExist:
        return False


def checking_last_gen_gigachat_time(user_id: int) -> bool:
    try:
        time_from_db = User.get(User.userid == user_id).last_gen_gigachat
        current_time = datetime.now()
        timedifference = current_time - time_from_db
        if timedifference >= timedelta(minutes=30):
            return True
        else:
            return False

    except DoesNotExist:
        return False



if __name__ == "__main__":
    db.drop_tables([User])
    db.create_tables([User])
