BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "courses_course" (
	"id"	integer NOT NULL,
	"tutor_id"	bigint NOT NULL,
	"shortcut"	varchar(20) NOT NULL,
	"name"	varchar(200) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("tutor_id") REFERENCES "user_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "issues_comment" (
	"id"	integer NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"name"	varchar(100) NOT NULL,
	"description"	text NOT NULL,
	"author_id"	bigint NOT NULL,
	"ticket_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("author_id") REFERENCES "user_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("ticket_id") REFERENCES "issues_ticket"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "issues_mediatype" (
	"id"	integer NOT NULL,
	"name"	varchar(50) NOT NULL UNIQUE,
	"icon"	varchar(19),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "issues_tag" (
	"id"	integer NOT NULL,
	"name"	varchar(99) NOT NULL UNIQUE,
	"slug"	varchar(50) NOT NULL UNIQUE,
	"icon"	varchar(19),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "issues_ticket" (
	"id"	integer NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"name"	varchar(100) NOT NULL,
	"location"	varchar(100),
	"description"	text NOT NULL,
	"severity"	integer NOT NULL,
	"status"	integer NOT NULL,
	"author_id"	bigint NOT NULL,
	"course_id"	bigint NOT NULL,
	"media_type_id"	bigint NOT NULL,
	CONSTRAINT "unique_author" UNIQUE("author_id","name","created_at"),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("author_id") REFERENCES "user_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("course_id") REFERENCES "courses_course"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("media_type_id") REFERENCES "issues_mediatype"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "issues_ticket_tags" (
	"id"	integer NOT NULL,
	"ticket_id"	bigint NOT NULL,
	"tag_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("ticket_id") REFERENCES "issues_ticket"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("tag_id") REFERENCES "issues_tag"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "issues_tickethistory" (
	"id"	integer NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"type"	integer NOT NULL,
	"status"	integer NOT NULL,
	"severity"	integer NOT NULL,
	"ticket_id"	bigint NOT NULL,
	"updated_by_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("ticket_id") REFERENCES "issues_ticket"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("updated_by_id") REFERENCES "user_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "user_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"first_name"	varchar(150) NOT NULL,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"role"	varchar(50) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE INDEX IF NOT EXISTS "courses_course_tutor_id_36617ab0" ON "courses_course" (
	"tutor_id"
);
CREATE INDEX IF NOT EXISTS "issues_comment_author_id_21f9ca55" ON "issues_comment" (
	"author_id"
);
CREATE INDEX IF NOT EXISTS "issues_comment_ticket_id_7ed17d41" ON "issues_comment" (
	"ticket_id"
);
CREATE INDEX IF NOT EXISTS "issues_ticket_author_id_103e4726" ON "issues_ticket" (
	"author_id"
);
CREATE INDEX IF NOT EXISTS "issues_ticket_course_id_4f273c76" ON "issues_ticket" (
	"course_id"
);
CREATE INDEX IF NOT EXISTS "issues_ticket_media_type_id_e6f3ca7c" ON "issues_ticket" (
	"media_type_id"
);
CREATE INDEX IF NOT EXISTS "issues_ticket_tags_tag_id_9d91bea6" ON "issues_ticket_tags" (
	"tag_id"
);
CREATE INDEX IF NOT EXISTS "issues_ticket_tags_ticket_id_f177e02b" ON "issues_ticket_tags" (
	"ticket_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "issues_ticket_tags_ticket_id_tag_id_1d0f094e_uniq" ON "issues_ticket_tags" (
	"ticket_id",
	"tag_id"
);
CREATE INDEX IF NOT EXISTS "issues_tickethistory_ticket_id_1cee7a95" ON "issues_tickethistory" (
	"ticket_id"
);
CREATE INDEX IF NOT EXISTS "issues_tickethistory_updated_by_id_0f3c9985" ON "issues_tickethistory" (
	"updated_by_id"
);
COMMIT;
