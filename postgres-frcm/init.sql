CREATE USER firerisk WITH PASSWORD 'firerisk';

GRANT ALL PRIVILEGES ON DATABASE fireriskdb TO firerisk;

CREATE TABLE IF NOT EXISTS FireRiskData (
    Id SERIAL PRIMARY KEY,
    FireRisk FLOAT NOT NULL,
    Lon FLOAT NOT NULL,
    Lat FLOAT NOT NULL,
    Source TEXT,
    TimeCreated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ExpirationDate TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL '1 hour'),
    TimeToUpdate INTERVAL,
    NumberOfRequests INTEGER DEFAULT 0
);

INSERT INTO FireRiskData (FireRisk, Lon, Lat, Source, TimeCreated, ExpirationDate) VALUES
(
    0.1, 
    60.3695783,
    5.3471855,
    'test1', 
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP + INTERVAL '3 minute'
);

INSERT INTO FireRiskData (FireRisk, Lon, Lat, Source, TimeCreated, ExpirationDate) VALUES
(
    60.3802674,
    0.99, 
    5.3318417,
    'test2', 
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS SubscribedUser (
    Id SERIAL PRIMARY KEY,
    IP VARCHAR(15) NOT NULL,
    AuthenticationToken VARCHAR(100) NOT NULL,
    SubscribedDataId INTEGER REFERENCES FireRiskData(Id),
    UpdateInterval INTERVAL,
    SubscriptionStatus BOOLEAN
);

SELECT * FROM FireRiskData;

DELETE FROM fireriskdata WHERE CURRENT_TIMESTAMP >= ExpirationDate;

SELECT * FROM FireRiskData;