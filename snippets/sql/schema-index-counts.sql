-- snippet:
-- title: "Count indexes per table in a schema"
-- card_title: "Count indexes per table"
-- summary: "List each table in an Oracle schema with how many indexes it has, using ALL_INDEXES grouped and ordered by table name."
-- tags: [indexes, oracle]
-- added: "2026-08-19T16:36:00+01:00"
-- submitted_by: Lupraxus
-- runnable: false
-- caveats: "Oracle data dictionary. Replace SCHEMA_NAME. Filter TABLE_OWNER instead of OWNER if you want indexes on that schema's tables regardless of who owns the index."
-- end-snippet
SELECT table_name, COUNT(*) AS index_count
FROM all_indexes
WHERE owner = 'SCHEMA_NAME'
GROUP BY table_name
ORDER BY table_name;
