05 Creating and Scheduling Data Pipelines

## Step:
### 1. Change Directory
```
cd 05-creating-and-scheduling-data-pipelines
```
<br>

### 2. สร้าางไฟล์ docker compose
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.0/docker-compose.yaml'
```
<br>

### 3. ปรับ config service ที่ไม่ใช้งาน
```
AIRFLOW__CORE__EXECUTOR: CeleryExecutor -> LocalExecutor

# AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
# AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0

#redis:
#condition: service_healthy

cooment redis + airflow worker + airwork trigger + folwer
```
<br>

### 4. run code จะได้ folder ต่างๆเข้ามา ex. dags, logs
```sh
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
<br>

### 5. Start docker
```
docker-compose up
```
<br>


### 6. Airflow UI port 8080
username: airflow
password: airflow
<br>

### 7. Create Dags
<br>
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/05-creating-and-scheduling-data-pipelines/img/Screen Shot 2567-04-22 at 17.22.58.png" width="70%"></img> 
<br>

### 7. List Table in Postgres and Select data
```
docker compose exec postgres bash
psql -d airflow -U airflow

\dt
select * from actors;
```
<br>
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/05-creating-and-scheduling-data-pipelines/img/Screen Shot 2567-04-22 at 17.12.10.png" width="70%"></img> 
<br>
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/05-creating-and-scheduling-data-pipelines/img/Screen Shot 2567-04-22 at 17.19.35.png" width="70%"></img> 
<br>
