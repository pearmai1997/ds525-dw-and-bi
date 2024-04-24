06 Analytics Engineering

## Step:
### 1. Change Directory
```
cd 06-analytics-engineering
```
<br>

### 2. สร้าางไฟล์ docker compose
```
docker compose up
```
<br>

### 3. Login database
<br>
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/05-creating-and-scheduling-data-pipelines/img/Screen Shot 2567-04-22 at 17.22.58.png" width="70%"></img> 
<br>

### 4. Create Visual ENV
```
python -m venv ENV
source ENV/bin/activate
pip install dbt-core dbt-postgres 
# dbt-spark dbt-bigquery
```

### 5. Initial Project
```
dbt init
```

### 6. Set up and debug
Set up ข้อมูลต่างๆ แล้วนำ code ในไฟล์ profiles.yml ไปใส่ใน folder 06-analytics-engineering > ds525 ตั้งชื่อว่า profiles.yml
```
code /home/codespace/.dbt/profiles.yml
```

```
dbt debug
```