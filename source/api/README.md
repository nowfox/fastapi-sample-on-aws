# API Introduction
## Run locally
Python version requirement 3.11
### 1. Installation package
```shell
pip install -r requirements.txt
pip install uvicorn
```
### 2. Starting web services locally
```shell
uvicorn main:app --reload
```
### 3. View API
http://127.0.0.1:8000/docs

## File Naming
| File Name         | Role        |
|------------------|-----------|
| main.py          | controller |
| service.py       | service   |
| schemas.py       | VO        |
| crud.py          | DAO       |
| db/models-xxx.py | DO        |

## Add a module
### 1. Generate DDL sql
Recommend using DataGrip, Place constraints use Inside table mode
### 2. Install omm
```shell
pip install omymodels
```
### 3. Generate models
```shell
omm db.sql -m sqlalchemy -t models_xxx.py
```
### 4. Generate schemas
```shell
omm db.sql -m pydantic --defaults-off -t schemas.py
```
### 5. Coding
Develop controllers, services, dao normally, and modify schemas
### 6. Export API
Add the router for the module to main.py in the root directory

```python
from pet.main import router as pet_router

app.include_router(pet_router)
```

### 7. Manual packaging testing
```shell
zip -r api.zip * -x "venv/*" "lambda/*_test.py"
```
Then put this zip file into lambda and run it.

## PyTest
### 1. Installation package
```shell
pip install -r pytest/requirements.txt
```

### 2. Test
```shell
python -m pytest pytest -s
```