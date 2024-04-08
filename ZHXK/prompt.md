### Instructions:
Your task is convert a question into a SQL query, given a Postgres database schema.
Adhere to these rules:
- **Deliberately go through the question and database schema word by word** to appropriately answer the question
- **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
- When creating a ratio, always cast the numerator as float

### Input:
Generate a SQL query that answers the question `8月16日有多少个号码语音不正常？`.
This query will run on a database whose schema is represented in this string:
CREATE TABLE IF NOT EXISTS fjq_test (
    id INT AUTO_INCREMENT PRIMARY KEY,
    procedure_starttime DATETIME, -- 2023 year
    procedure_endtime DATETIME,-- 2023 year
    md5_num VARCHAR(20),
    localcity VARCHAR(512),
    nodeb_cellid VARCHAR(512),
    procedure_type VARCHAR(512),
    service_type VARCHAR(512),
    call_service_type VARCHAR(512),
    epsfb_flag VARCHAR(512),
    procedure_status VARCHAR(512),
    md5_monum VARCHAR(512),
    md5_mtnum VARCHAR(512),
    call_side VARCHAR(512),
    alerting_time VARCHAR(512),
    calldrop_flag VARCHAR(512),
    err_scene_category VARCHAR(512),
    err_scene_code VARCHAR(512),
    sip_fail_cause VARCHAR(512),
    nodeb_cellid_dest VARCHAR(512),
    err_scene VARCHAR(512),
    mos_ul VARCHAR(512),
    mos_dl VARCHAR(512)
);
语音不正常的定义是 ((procedure_status为失败 and err_scene为空)  or  err_scene不为空)


### Response:
Based on your instructions, here is the SQL query I have generated to answer the question `8月16日有多少个号码语音不正常？`:
```sql
```



```
### Instructions:
Your task is convert a question into a SQL query, given a Postgres database schema.
Adhere to these rules:
- **Deliberately go through the question and database schema word by word** to appropriately answer the question
- **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
- current time： `{current_time}`

### Example：
Q:列出主叫号码
A:SELECT md5_num
  FROM fjq_test 
  WHERE  call_side="主叫"; 

Q:列出一分钟内所有记录
A:SELECT *
  FROM fjq_test
  WHERE  procedure_starttime >= DATE_SUB(NOW(), INTERVAL 1 MINUTE)
  AND    procedure_endttime <=NOW();

Q:列出今天的所有记录
A:SELECT *
  FROM fjq_test
  WHERE  DATE(procedure_starttime) = CURRENT_DATE();

Q:列出昨天的所有记录
A:SELECT *
  FROM fjq_test
  WHERE  DATE(procedure_starttime) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY);
  
Q:列出去年的所有记录
A:SELECT *
  FROM fjq_test
  WHERE  YEAR(procedure_starttime) =YEAR(CURRENT_DATE()) - 1;

Q:查询语音不正常的号码
A:SELECT md5_num
  FROM fjq_test
  WHERE  (fjq_test.procedure_status = '失败' and fjq_test.err_scene is null or fjq_test.err_scene is not null);

Q:列出所有基站小区
A:SELECT nodeb_cellid,nodeb_cellid_dest
  FROM fjq_test;
  

### Input:
Generate a SQL query that answers the question `{user_question}`.
This query will run on a database whose schema is represented in this string:
{table_metadata_string}

### Response:
Based on your instructions and , here is the SQL query I have generated to answer the question `{user_question}`:
```sql

```

prompt设置建议：



> 建表语句+查询语句+3行数据