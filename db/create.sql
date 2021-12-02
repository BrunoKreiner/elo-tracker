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

CREATE TABLE Activity (
    name VARCHAR(255) NOT NULL PRIMARY KEY,
    category VARCHAR NOT NULL,
    CHECK (category IN ('People', 'Restaurant', 'School' ))
);

CREATE TABLE Matches (
    activity VARCHAR(255) NOT NULL,
    matchID INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    user1_ID INT NOT NULL,
    user2_ID INT NOT NULL,
    user1_score INT,
    user2_score INT,
    date_time DATE NOT NULL,
    accepted BOOLEAN NOT NULL,
    Foreign key(activity) references Activity(name)
);


CREATE TABLE Rankables (
    rankable_id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR NOT NULL,
    about VARCHAR NOT NULL,
    CHECK (category IN ('People', 'Restaurant', 'Code Editor', 'School'))
);

CREATE TABLE Member_of (
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    status VARCHAR(255) NOT NULL,
    PRIMARY KEY (name, email),
    Foreign key(name) references League(name),
    Foreign key(email) references Rankables(email),
    CHECK (status IN ('member', 'coach', 'president', 'grandmaster', 'novice'))
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
    Foreign key(user_ID) references Rankables(rankable_id),
    Foreign key(activity) references Activity(name)
);

CREATE TABLE Notifications (
    user_ID INT NOT NULL,
    descript VARCHAR NOT NULL,
    date_time DATE NOT NULL,
    FOREIGN KEY(user_ID) references Rankables(rankable_id)
);

CREATE TABLE Events (
    event_id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    minELO INT,
    maxELO INT,
    category VARCHAR NOT NULL,
    FOREIGN KEY(type) references Activity(name),
    CHECK (category IN ('People', 'Restaurant', 'Code Editor', 'School')) 
);

CREATE TABLE MatchInEvent (
    match_id INT NOT NULL PRIMARY KEY,
    event_id INT NOT NULL,
    FOREIGN KEY(event_id) references Events(event_id)
);

-- trigger to enforce that for MatchInEvent, the match and the event are of the same activity/type
CREATE FUNCTION Match_Event_Activity_Alike_Match() RETURNS TRIGGER as $$

DECLARE

  temp_var1 activityFromMatch;
  temp_var2 activityFromEvent;


BEGIN
  select T.activity
  into temp_var1
  from (
  SELECT activity
  FROM Events
  WHERE Events.id = New.event_id
  ) as T


  select J.activity
  into temp_var2
  from (
  SELECT user1_ID
  FROM Matches
  WHERE Matches.matchID = New.match_id
  
  
  
  ) as J

  
  IF (temp_var1 <> temp_var2) 
  THEN
    Raise Exception 'The match activity type does not match the event activity type'
  
  End if;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;




CREATE TRIGGER Match_Event_Activity_Alike
  BEFORE INSERT OR UPDATE ON MatchInEvent
  FOR EACH ROW
  EXECUTE PROCEDURE Match_Event_Activity_Alike_Match();

-- trigger to enforce that for MatchInEvent, the elo scores of the players (when added) are within the range





--CREATE TRIGGER EloInRange
 -- BEFORE INSERT OR UPDATE ON MatchInEvent
  --FOR EACH ROW
  --EXECUTE PROCEDURE EloInRange();






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



  
CREATE FUNCTION Match_To_Approve() RETURNS TRIGGER AS $$
-- DECLARE @begin_text TEXT = "You have a pending match in ";
-- DECLARE @end_text TEXT = " with user ";

BEGIN
  INSERT INTO Notifications(user_ID, descript, date_time)
  VALUES(NEW.user2_ID, CONCAT('You have a pending match in ', NEW.activity, ' with user ', (SELECT name FROM Rankables WHERE NEW.user1_ID = rankable_id)), CURRENT_TIMESTAMP);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER Match_To_Approve
  AFTER INSERT ON Matches
  FOR EACH ROW
  EXECUTE PROCEDURE Match_To_Approve();


CREATE FUNCTION ParticipatesInValidation() RETURNS TRIGGER AS $$

DECLARE

  temp_var INT;

BEGIN
  -- YOUR IMPLEMENTATION GOES HERE
  select count(*) 
  into temp_var
  from ParticipatesIn 
  where New.activity = ParticipatesIn.activity AND New.user1_ID = ParticipatesIn.user_ID;
  
  IF temp_var < 1 
  THEN
    INSERT INTO ParticipatesIn(user_ID, activity, elo)
    VALUES(NEW.user1_ID, New.activity, 1000);
    
  
  End if;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER ParticipatesInValidation
  BEFORE INSERT OR UPDATE ON Matches
  FOR EACH ROW
  EXECUTE PROCEDURE ParticipatesInValidation();
  

-- trigger to enforce that a user cannot be the president of more than 3 leagues.
-- CREATE FUNCTION elo_notification() RETURNS TRIGGER AS $$

-- DECLARE

--   maxElo INT;
--   minElo INT;
--   userID INT;

-- BEGIN
--   -- YOUR IMPLEMENTATION GOES HERE
--   SELECT user_id into userID FROM ELOHistory ORDER BY id DESC LIMIT 1;  

--   SELECT Max(elo) 
--   into maxElo 
--   FROM (SELECT *
--   FROM ELOHistory 
--   WHERE user_id = userID
--   ORDER BY id 
--   DESC LIMIT 2) AS foo;

--   SELECT Min(elo) 
--   into minElo 
--   FROM (SELECT *
--   FROM ELOHistory 
--   WHERE user_id = userID
--   ORDER BY id 
--   DESC LIMIT 2) AS foo;
  
--   IF maxElo - minElo > 50
--   THEN
    
  
--   End if;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER Elo_Notification
--   AFTER INSERT OR UPDATE ON ELOHistory
--   FOR EACH ROW
--   EXECUTE PROCEDURE elo_notification();
