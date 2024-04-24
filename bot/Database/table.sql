DROP TABLE IF EXISTS telegram_bot_data.users;
CREATE TABLE IF NOT EXISTS telegram_bot_data.users(
  userid bigint PRIMARY KEY,
  usertoken text,
  username varchar(255),
  name varchar (255),
  chromacollection varchar(255),
  lastGen timestamp

                                                  );


--Now we can use our table