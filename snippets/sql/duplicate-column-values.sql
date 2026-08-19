-- snippet:
-- title: "Find repeated values in a column"
-- card_title: "Find duplicate column values"
-- summary: "Group by a column and return each value that appears more than once, together with how many times it is duplicated."
-- tags: [duplicates]
-- added: "2026-08-19T16:35:00+01:00"
-- submitted_by: Lupraxus
-- runnable: false
-- caveats: "Replace table_name and column_name. COUNT(*) includes NULL groups on engines that group NULLs together; COUNT(column_name) ignores NULLs."
-- end-snippet
SELECT column_name, COUNT(*) AS duplicates
FROM table_name
GROUP BY column_name
HAVING COUNT(*) > 1;
