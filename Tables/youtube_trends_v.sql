-- public.youtube_trends_v исходный текст

CREATE OR REPLACE VIEW public.youtube_trends_v
AS SELECT yt.video_id,
    yt.title,
    yt.category,
    yt.views,
    yt.likes,
    yt.comments,
    yt.published_at,
    yt.region,
    yt.trend_date,
    yc.category_id,
    yc.category_name
   FROM youtube_trends yt
     LEFT JOIN youtube_categories yc ON yc.category_id::text = yt.category::text;
