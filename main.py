"""FastAPI endpoint backed by the downloaded Data.go.th CSV resource."""

import csv
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException

DATASET_URL = "https://data.go.th/dataset/zoo-visitors2569"
DATASET_ID = "970c2632-1669-44aa-80c5-2c20cb2295e4"
RESOURCE_ID = "0ecc96cf-d914-42a1-b184-dbbd013c3c9c"
FISCAL_YEAR = 2569
CSV_PATH = Path(__file__).with_name("zoo_visitors_january_2569.csv")

app = FastAPI(
    title="Zoo Visitors 2569 API",
    description="ข้อมูลสถิติผู้เข้าชมสวนสัตว์จากไฟล์ CSV ของ Data.go.th",
    version="1.0.0",
)


def load_records() -> list[dict[str, Any]]:
    if not CSV_PATH.is_file():
        raise HTTPException(status_code=500, detail=f"ไม่พบไฟล์ข้อมูล: {CSV_PATH.name}")

    records: list[dict[str, Any]] = []
    try:
        with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                clean: dict[str, Any] = {}
                for key, raw_value in row.items():
                    if key is None or not key.strip():
                        continue
                    value = (raw_value or "").strip()
                    number = value.replace(",", "")
                    if number.isdigit():
                        clean[key.strip()] = int(number)
                    else:
                        clean[key.strip()] = value or None
                if any(value is not None for value in clean.values()):
                    records.append(clean)
    except (OSError, UnicodeError, csv.Error) as exc:
        raise HTTPException(status_code=500, detail=f"อ่านไฟล์ CSV ไม่สำเร็จ: {exc}") from exc

    if not records:
        raise HTTPException(status_code=500, detail="ไฟล์ CSV ไม่มีรายการข้อมูล")
    return records


@app.get("/api/zoo-visitors", tags=["Zoo visitors"])
def get_zoo_visitors() -> dict[str, Any]:
    records = load_records()
    return {
        "source": "Data.go.th - Open Government Data of Thailand",
        "dataset": "ข้อมูลรายงานสถิติจำนวนผู้เข้าชมสวนสัตว์ ปีงบประมาณ 2569",
        "dataset_url": DATASET_URL,
        "dataset_id": DATASET_ID,
        "resource_id": RESOURCE_ID,
        "resource": "ข้อมูลรายงานสถิติจำนวนผู้เข้าชมสวนสัตว์ อสส มกราคม 2569",
        "fiscal_year": FISCAL_YEAR,
        "records_count": len(records),
        "records": records,
    }


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"message": "Zoo Visitors API", "docs": "/docs", "data": "/api/zoo-visitors"}


@app.get("/health", include_in_schema=False)
def health() -> dict[str, str]:
    return {"status": "ok"}
