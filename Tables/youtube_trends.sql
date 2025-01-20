-- public.youtube_trends определение

-- Drop table

-- DROP TABLE public.youtube_trends;

CREATE TABLE public.youtube_trends (
	video_id varchar(50) NOT NULL,
	title text NULL,
	category varchar(50) NULL,
	"views" int8 NULL,
	likes int8 NULL,
	"comments" int8 NULL,
	published_at timestamp NULL,
	region varchar(10) NULL,
	trend_date date NULL,
	CONSTRAINT youtube_trends_pkey PRIMARY KEY (video_id)
);
