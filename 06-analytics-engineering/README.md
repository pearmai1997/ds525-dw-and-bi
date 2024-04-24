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

### 3. Login database Port 3000
<br>
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/06-analytics-engineering/img/Screen Shot 2567-04-24 at 13.52.43.png" width="70%"></img> 
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
<br>
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/06-analytics-engineering/img/Screen Shot 2567-04-24 at 14.07.28.png" width="70%"></img> 
<br>
```
code /home/codespace/.dbt/profiles.yml
```
<br>
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/06-analytics-engineering/img/Screen Shot 2567-04-24 at 14.53.31.png" width="70%"></img> 
<br>
```
dbt debug
```

### 7. เขียน code sql ใน model แล้ว run
```
dbt run
```
<br>
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/06-analytics-engineering/img/Screen Shot 2567-04-24 at 14.46.58.png" width="70%"></img> 
<br>