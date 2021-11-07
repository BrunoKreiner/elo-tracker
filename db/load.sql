-- \COPY Users FROM 'data/Users.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'data/Products.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Purchases FROM 'data/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Matches FROM 'data/Matches.csv' WITH DELIMITER ',' NULL '' CSV
-- \COPY Purchases FROM 'data/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
-- \COPY Matches FROM 'data/Matches.csv' WITH DELIMITER ',' NULL '' CSV
\COPY League FROM 'data/League.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Activity FROM 'data/Activity.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Member_of FROM 'data/Member_of.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Rankables FROM 'data/Rankables.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.rankables_rankable_id_seq', 10, false)

