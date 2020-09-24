CREATE DATABASE intervote;
USE intervote;
CREATE TABLE messages(id int AUTO_INCREMENT, message VARCHAR(255), upvotes INT, downvotes INT, PRIMARY KEY(id));
INSERT INTO messages SET message = "Pie is better than Cake", upvotes = 314, downvotes = 0;
INSERT INTO messages SET message = "Glass half full?", upvotes = 0, downvotes = 0;
INSERT INTO messages SET message = "Coronavirus", upvotes = 0, downvotes = 2020;