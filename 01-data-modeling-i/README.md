# 01 Data Modeling i

## Data Model (SQL)
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/01-data-modeling-i/img/01-data-modeling-i_Database%20ER%20diagram.png" width="70%"></img> 
<br>

## Step:
### 1. Change Directory
```
cd 01-data-modeling-i
```
<br>

### 2. Create Visual ENV
```
python -m venv ENV
source ENV/bin/activate
pip install -r requirements.txt
```
<br>

### 3. Start Postgres and Docker
```
docker-compose up
```
<br>

### 4. Contect Database (Port: 8080)
```
System: PostgreSQL
Server: postgres
Username: postgres
Password: postgres
Database: postgres
```
<br>

### 5. Create Table 
```
python create_tables.py
```
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/01-data-modeling-i/img/create_table.png" width="70%"></img> 
<br>

### 6. Import Data
```
python etl.py
```
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/01-data-modeling-i/img/insert_data.png" width="70%"></img> 
<br>

### 7. Stop Postgres
```
docker-compose down
```
<br>