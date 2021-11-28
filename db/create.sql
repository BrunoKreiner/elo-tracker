-- Feel free to modify this file to match your development goal.
-- Drop Table Rankables;
-- Drop Table Users;
-- Drop Table League;
-- Drop Table Activity;
-- Drop Table Matches;
-- Drop Table Events;
-- Drop Table Member_of;

CREATE TABLE Users (
    id INT GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL
);

CREATE TABLE League (
    l_id INT NOT NULL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    president VARCHAR(255) NOT NULL
);

CREATE TABLE Matches (
    activity VARCHAR(255) NOT NULL,
    matchID INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    user1_ID INT NOT NULL,
    user2_ID INT NOT NULL,
    user1_score INT,
    user2_score INT,
    date_time DATE NOT NULL,
    accepted BOOLEAN NOT NULL
    -- accepted
);

CREATE TABLE Activity (
    name VARCHAR(255) NOT NULL PRIMARY KEY,
    category VARCHAR NOT NULL,
    CHECK (category IN ('People', 'Restaurant'))
);

CREATE TABLE Rankables (
    rankable_id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR NOT NULL,
    about VARCHAR NOT NULL,
    CHECK (category IN ('People', 'Restaurant'))
);

CREATE TABLE Member_of (
    name VARCHAR NOT NULL, -- review hw2 triggers.
    email VARCHAR NOT NULL,
    status VARCHAR(255) NOT NULL,
    PRIMARY KEY (name, email),
    Foreign key(name) references League(name),
    Foreign key(email) references Rankables(email),
    CHECK (status IN ('member', 'coach', 'president'))
);


CREATE TABLE ELOHistory (
    id INT NOT NULL,
    user_id INT NOT NULL,
    activity VARCHAR(255) NOT NULL,
    elo INT NOT NULL,
    matchID INT,

    Foreign key(user_id) references Rankables(rankable_id),
    Foreign key(activity) references Activity(name) -- this foreign key constraint works!
);

CREATE TABLE ParticipatesIn (
    user_ID INT NOT NULL,
    activity VARCHAR(255) NOT NULL,
    elo INT NOT NULL,
    PRIMARY KEY (user_ID, activity),
    --Foreign key(user_ID) references Rankables(rankable_id),
    Foreign key(activity) references Activity(name)
);

CREATE TABLE Notifications (
    user_ID INT NOT NULL,
    descript VARCHAR NOT NULL,
    FOREIGN KEY(user_ID) references Rankables(rankable_id)
);

CREATE TABLE Events (
    event_id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    date TIMESTAMP NOT NULL,
    minELO INT,
    maxELO INT
);


-- trigger to enforce that a user cannot be the president of more than 3 leagues.
CREATE FUNCTION No_More_President() RETURNS TRIGGER AS $$

DECLARE

  temp_var INT;

BEGIN
  -- YOUR IMPLEMENTATION GOES HERE
  select count(*) 
  into temp_var
  from League 
  where League.president = New.president;
  
  IF temp_var > 3
  THEN
    Raise Exception '% is already the president of 3 leagues, hence, cannot be president of another.', New.president;
  
  End if;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER No_More_President
  BEFORE INSERT OR UPDATE ON League
  FOR EACH ROW
  EXECUTE PROCEDURE No_More_President();


-- trigger to enforce that a user cannot be the president of more than 3 leagues.
CREATE FUNCTION elo_notification() RETURNS TRIGGER AS $$

DECLARE

  maxElo INT;
  minElo INT;
  userID INT;

BEGIN
  -- YOUR IMPLEMENTATION GOES HERE
  SELECT user_id into userID FROM ELOHistory ORDER BY id DESC LIMIT 1;  

  SELECT Max(elo) 
  into maxElo 
  FROM (SELECT *
  FROM ELOHistory 
  WHERE user_id = userID
  ORDER BY id 
  DESC LIMIT 2) AS foo;

  SELECT Min(elo) 
  into minElo 
  FROM (SELECT *
  FROM ELOHistory 
  WHERE user_id = userID
  ORDER BY id 
  DESC LIMIT 2) AS foo;
  
  IF maxElo - minElo > 50
  THEN
    Raise Exception '% is already the president of 3 leagues, hence, cannot be president of another.';
  
  End if;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER Elo_Notification
  AFTER INSERT OR UPDATE ON ELOHistory
  FOR EACH ROW
  EXECUTE PROCEDURE elo_notification();