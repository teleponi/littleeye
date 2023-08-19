 TABLE  "courses_course" (
	"id"	integer NOT NULL,
	"tutor_id"	bigint NOT NULL,
	"shortcut"	varchar(20) NOT NULL,
	"name"	varchar(200) NOT NULL,
);

 TABLE  "issues_comment" (
	"id"	integer NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"name"	varchar(100) NOT NULL,
	"description"	text NOT NULL,
	"author_id"	bigint NOT NULL,
	"ticket_id"	bigint NOT NULL,
);

 TABLE  "issues_mediatype" (
	"id"	integer NOT NULL,
	"name"	varchar(50) NOT NULL UNIQUE,
	
);
 TABLE  "issues_tag" (
	"id"	integer NOT NULL,
	"name"	varchar(99) NOT NULL UNIQUE,
);

 TABLE  "issues_ticket" (
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
);

 TABLE  "issues_ticket_tags" (
	"id"	integer NOT NULL,
	"ticket_id"	bigint NOT NULL,
	"tag_id"	bigint NOT NULL,
	
);

 TABLE  "issues_tickethistory" (
	"id"	integer NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"type"	integer NOT NULL,
	"status"	integer NOT NULL,
	"severity"	integer NOT NULL,
	"ticket_id"	bigint NOT NULL,
	"updated_by_id"	bigint NOT NULL,
	"comment_id"	bigint,
	
);

 TABLE  "user_user" (
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
	
);
 
