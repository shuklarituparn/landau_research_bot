import os

from playhouse.postgres_ext import *
from datetime import datetime, timedelta
from dotenv import load_dotenv
import psycopg2

load_dotenv()
Database_name = os.getenv("DATABASE_NAME")
Database_user = os.getenv("DATABASE_USERNAME")
Database_pass = os.getenv("DATABASE_PASSWORD")
db = PostgresqlExtDatabase(Database_name, user=Database_user, password=Database_pass)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    userid = BigIntegerField(primary_key=True)
    usertoken = TextField()
    username = CharField(max_length=255)
    name = CharField(max_length=255)
    chromacollection = CharField(max_length=255)
    lastGen = DateTimeField(default=datetime.now())

    class Meta:
        table_name = "user"


def checking_user_exits(user_id: int) -> bool:
    try:
        User.get(User.userid == user_id)
        return True
    except DoesNotExist:
        return False


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


# if __name__ == "__main__":
#     db.drop_tables([User])
#     db.create_tables([User])