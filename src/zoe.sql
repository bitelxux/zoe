
-- Table: messages
CREATE TABLE messages ( 
    payload   TEXT,
    ts        DATETIME,
    ackd      BOOLEAN,
    sender    VARCHAR( 50 ),
    recipient VARCHAR( 50 ),
    type      INT 
);


-- Table: contacts
CREATE TABLE contacts ( 
    id     INTEGER        PRIMARY KEY AUTOINCREMENT,
    name   VARCHAR( 50 ),
    email  VARCHAR( 50 ),
    avatar BLOB 
);

INSERT INTO [contacts] ([id], [name], [email], [avatar]) VALUES (1, 'cnn', null, null);
INSERT INTO [contacts] ([id], [name], [email], [avatar]) VALUES (2, 'otro', null, null);
