-- public.youtube_categories определение

-- Drop table

-- DROP TABLE public.youtube_categories;

CREATE TABLE public.youtube_categories (
	category_id varchar(50) NOT NULL,
	category_name text NULL,
	CONSTRAINT youtube_categories_pkey PRIMARY KEY (category_id)
);
