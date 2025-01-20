-- public.news_articles определение

-- Drop table

-- DROP TABLE public.news_articles;

CREATE TABLE public.news_articles (
	article_id serial4 NOT NULL,
	title text NULL,
	source_name varchar(255) NULL,
	published_at timestamp NULL,
	url text NULL,
	"content" text NULL,
	youtube_video_id varchar(50) NULL,
	CONSTRAINT news_articles_pkey PRIMARY KEY (article_id)
);


-- public.news_articles внешние включи

ALTER TABLE public.news_articles ADD CONSTRAINT news_articles_youtube_video_id_fkey FOREIGN KEY (youtube_video_id) REFERENCES public.youtube_trends(video_id);
