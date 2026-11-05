# Zoo Visitors 2569 API

FastAPI reads the local `zoo_visitors_january_2569.csv` resource and returns its records as JSON. The CSV contains 63 data rows and is the January 2569 resource for the Data.go.th zoo visitors dataset.

## Run locally (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` for Swagger UI. The endpoint is `GET http://127.0.0.1:8000/api/zoo-visitors`.

The response includes the source, dataset/resource IDs, fiscal year, record count, and actual CSV rows. The downloaded CSV must remain beside `main.py` when running or deploying.

## Postman

Import `postman_collection.json`, send the GET request, and confirm HTTP 200 and the JSON body. Capture the Postman window showing the method, status, and response for submission.
