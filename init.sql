CREATE USER docker;
GRANT ALL PRIVILEGES ON DATABASE fizikdb TO docker;
--CREATE TABLE Credentials (
--    user_id bigserial primary key,
--    username varchar(20) NOT NULL,
--    password char(64) NOT NULL,
--    email text NOT NULL,
--    date_created timestamp default NULL
--);
--
--CREATE TABLE FoodLog (
--    food_log_entry_id bigserial primary key,
--    user_id bigint references Credentials(user_id),
--    food_id varchar(64) NOT NULL,
--    serving_size varchar(20),
--    amount varchar(20) NOT NULL,
--    date_created timestamp default NULL
--);
