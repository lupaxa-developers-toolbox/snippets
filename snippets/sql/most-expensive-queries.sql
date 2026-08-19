-- snippet:
-- title: "Show the N most expensive queries"
-- card_title: "N most expensive queries"
-- summary: "Return the SQL Server plans that have used the most CPU, with execution count, total and average worker time, query text, and the XML plan for review."
-- tags: [performance, sql-server]
-- added: "2026-08-19T16:36:00+01:00"
-- submitted_by: Lupraxus
-- runnable: false
-- caveats: "SQL Server DMVs. Needs VIEW SERVER STATE. Change TOP (10) for N. Worker time is microseconds. DB_NAME(st.dbid) is NULL for some ad hoc batches."
-- end-snippet
SELECT TOP (10)
    st.text AS query_text,
    qs.execution_count,
    qs.total_worker_time / 1000000.0 AS total_cpu_seconds,
    qs.total_worker_time / qs.execution_count / 1000.0 AS avg_cpu_ms,
    qp.query_plan,
    DB_NAME(st.dbid) AS database_name
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
CROSS APPLY sys.dm_exec_query_plan(qs.plan_handle) qp
ORDER BY qs.total_worker_time DESC;
