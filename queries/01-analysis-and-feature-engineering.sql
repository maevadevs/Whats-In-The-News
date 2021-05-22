-- Check the current state of the DB Table
SELECT *
FROM public."AllTheNews21"
LIMIT 100;


-- How many article entries are in this dataset?
SELECT COUNT(*) AS articles_count
FROM public."AllTheNews21";
-- Answer: 2,584,165


-- What is the MAX year in this dataset?
SELECT MAX(year) AS max_year
FROM public."AllTheNews21";
-- Answer: 2020


-- What is the MIN year in this dataset?
SELECT MIN(year) AS min_year
FROM public."AllTheNews21";
-- Answer: 2016


-- How many article entries per year?
SELECT
	year,
	COUNT(*) AS articles_count
FROM public."AllTheNews21"
GROUP BY year
ORDER BY year;
-- Answer:
-- 2016		595,062
-- 2017		635,785
-- 2018		547,159
-- 2019		616,181
-- 2020		189,978


-- What is the Average article entries per year?
with cte AS (
	SELECT
		year,
		COUNT(*) AS articles_count
	FROM public."AllTheNews21"
	GROUP BY year
	ORDER BY year
)
SELECT AVG(cte.articles_count) AS mean_articles_count_per_year
FROM cte;
-- Answer: 516,833 Articles per year


-- How many entries per month for each year?
SELECT
	year,
	month,
	COUNT(*) AS entries
FROM public."AllTheNews21"
GROUP BY year, month
ORDER BY year, month;
-- Answer
-- 2016	1	46,614
-- 2016	2	47,694
-- 2016	3	50,708
-- 2016	4	49,307
-- 2016	5	49,914
-- 2016	6	50,586
-- 2016	7	49,992
-- 2016	8	49,728
-- 2016	9	49,772
-- 2016	10	53,179
-- 2016	11	52,447
-- 2016	12	45,121
-- 2017	1	52,689
-- 2017	2	51,453
-- 2017	3	58,926
-- 2017	4	51,772
-- 2017	5	58,680
-- 2017	6	54,367
-- 2017	7	50,669
-- 2017	8	52,987
-- 2017	9	50,488
-- 2017	10	54,773
-- 2017	11	54,770
-- 2017	12	44,211
-- 2018	1	50,437
-- 2018	2	48,894
-- 2018	3	53,061
-- 2018	4	49,916
-- 2018	5	52,116
-- 2018	6	47,961
-- 2018	7	45,439
-- 2018	8	42,343
-- 2018	9	38,757
-- 2018	10	43,311
-- 2018	11	40,915
-- 2018	12	34,009
-- 2019	1	40,775
-- 2019	2	40,502
-- 2019	3	46,530
-- 2019	4	46,212
-- 2019	5	48,246
-- 2019	6	53,485
-- 2019	7	56,620
-- 2019	8	54,449
-- 2019	9	58,958
-- 2019	10	65,376
-- 2019	11	55,830
-- 2019	12	49,198
-- 2020	1	55,485
-- 2020	2	59,475
-- 2020	3	74,891
-- 2020	4	127


-- What is the Average article entries per month overall?
with cte AS (
	SELECT
		year,
		month,
		COUNT(*) AS articles_count
	FROM public."AllTheNews21"
	GROUP BY year, month
	ORDER BY year, month
)
SELECT AVG(cte.articles_count) AS mean_articles_count_per_year
FROM cte;
-- Answer: 49,695 Articles per month over the 5 years


-- Which month is overall the highest? Which month is the lowest?
SELECT
	month,
	COUNT(*) AS articles_count
FROM public."AllTheNews21"
GROUP BY month
ORDER BY month;
-- Answer:
-- 1	246,000
-- 2	248,018
-- 3	284,116
-- 4	197,334
-- 5	208,956
-- 6	206,399
-- 7	202,720
-- 8	199,507
-- 9	197,975
-- 10	216,639
-- 11	203,962
-- 12	172,539


-- How many months are in this dataset in total?
with cte  AS (
	SELECT 
		year,
		COUNT(DISTINCT month) AS months_in_year
	FROM public."AllTheNews21"
	GROUP BY year
)
SELECT SUM(months_in_year) AS months_in_dataset
FROM cte;
-- Answer: 52
-- 2016	12
-- 2017	12
-- 2018	12
-- 2019	12
-- 2020	4


/* Feature Engineering */
/* ******************* */


-- -- Add Feature: Length of title
-- ALTER TABLE public."AllTheNews21" 
-- ADD COLUMN title_length bigint; 
-- -- Now update the value of the new column
-- UPDATE public."AllTheNews21" 
-- SET title_length = LENGTH(title); 


-- -- Add Feature: Length of article
-- ALTER TABLE public."AllTheNews21" 
-- ADD COLUMN article_length bigint; 
-- -- Now update the value of the new column
-- UPDATE public."AllTheNews21" 
-- SET article_length = LENGTH(article); 
