
/* Drop Triggers */

DROP TRIGGER TRI_chat_cid;
DROP TRIGGER TRI_schedule_sid;



/* Drop Tables */

DROP TABLE chat CASCADE CONSTRAINTS;
DROP TABLE users CASCADE CONSTRAINTS;



/* Drop Sequences */

DROP SEQUENCE SEQ_chat_cid;
DROP SEQUENCE SEQ_schedule_sid;




/* Create Sequences */

CREATE SEQUENCE SEQ_chat_cid INCREMENT BY 1 START WITH 1;
CREATE SEQUENCE SEQ_schedule_sid INCREMENT BY 1 START WITH 1;



/* Create Tables */

CREATE TABLE chat
(
	cid number NOT NULL,
	"uid" varchar2(12),
	u_question varchar2(100000) NOT NULL,
	c_answer varchar2(100000) NOT NULL,
	c_date varchar2(1000000) DEFAULT '' NOT NULL,
	origin_date varchar2(1000000) DEFAULT '' NOT NULL,
	PRIMARY KEY (cid)
);


CREATE TABLE users
(
	"uid" varchar2(12) NOT NULL,
	pwd char(60) NOT NULL,
	uname varchar2(16) NOT NULL,
	email varchar2(40) NOT NULL,
	regDate date DEFAULT SYSDATE,
	isDeleted number DEFAULT 0,
	PRIMARY KEY ("uid")
);



/* Create Foreign Keys */

ALTER TABLE chat
	ADD FOREIGN KEY ("uid")
	REFERENCES users ("uid")
;



/* Create Triggers */



CREATE OR REPLACE TRIGGER TRI_chat_cid BEFORE INSERT ON chat
FOR EACH ROW
BEGIN
	SELECT SEQ_chat_cid.nextval
	INTO :new.cid
	FROM dual;
END;

/






