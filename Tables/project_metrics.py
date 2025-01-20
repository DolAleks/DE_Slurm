-- public.project_metrics определение

-- Drop table

-- DROP TABLE public.project_metrics;

CREATE TABLE public.project_metrics (
	metric_date date NOT NULL,
	total_news int4 NULL,
	related_news int4 NULL,
	related_percentage float8 NULL,
	videos_with_related_news int4 NULL,
	CONSTRAINT project_metrics_pkey PRIMARY KEY (metric_date)
);
