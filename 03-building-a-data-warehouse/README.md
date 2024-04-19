# 03 Building a data warehouse

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

### 4. Create dataset in Google Cloud
BigQuery Studio > Create Dataset
<br>
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/03-building-a-data-warehouse/img/Screen Shot 2567-04-19 at 17.37.02.png" width="70%"></img> 
<br>

### 5. Create Service Account 
IAM & Admin > Service Account > Create (role: Admin)  
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/03-building-a-data-warehouse/img/Screen Shot 2567-04-19 at 17.42.42.png" width="70%"></img> 
<br>

### 6. Get Key
Service Account > Key > Create New Key (.JSON) > Upload Key Json File to Folder
<img src="https://github.com/pearmai1997/ds525-dw-and-bi/blob/main/03-building-a-data-warehouse/img/Screen Shot 2567-04-19 at 18.01.43.png" width="70%"></img> 
<br>

### 7. Change Key Path and Project ID in etl_bigquery.py
<br>

### 8. Insert Data to BigQuery
```
python etl_bigquery.py
```