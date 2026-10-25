from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import get_connection

app = FastAPI(title="Smart Irrigation System API")


# ---------- Request & Response Models ----------

class SensorReading(BaseModel):
    sensor_id: str
    field_id: int
    moisture_value: float


class SensorReadingResponse(BaseModel):
    id: int
    sensor_id: str
    moisture_value: float
    timestamp: datetime


class FieldRegistration(BaseModel):
    farmer_id: int
    crop_id: int
    location_lat: float
    location_lng: float
    size_acres: float
    sensor_id: str


class FarmerRegistration(BaseModel):
    name: str
    phone: str
    preferred_language: str = "en"


class CropRegistration(BaseModel):
    name: str
    growth_stage: str
    water_requirement_mm_per_day: float


# ---------- Health Check ----------

@app.get("/")
def root():
    return {"status": "Smart Irrigation API is running"}


# ---------- Sensor Ingestion ----------

@app.post("/sensor-reading")
def ingest_reading(reading: SensorReading):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO sensor_reading (sensor_id, field_id, moisture_value)
                       VALUES (%s, %s, %s) RETURNING id""",
                    (reading.sensor_id, reading.field_id, reading.moisture_value),
                )
                new_id = cur.fetchone()[0]
                conn.commit()
                return {"status": "stored", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sensor-readings/{field_id}", response_model=List[SensorReadingResponse])
def get_readings(field_id: int, limit: int = 20):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT id, sensor_id, moisture_value, reading_timestamp
                       FROM sensor_reading WHERE field_id = %s
                       ORDER BY reading_timestamp DESC LIMIT %s""",
                    (field_id, limit),
                )
                rows = cur.fetchall()
                return [
                    {
                        "id": r[0],
                        "sensor_id": r[1],
                        "moisture_value": r[2],
                        "timestamp": r[3],
                    }
                    for r in rows
                ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- Farmer / Crop / Field Registration ----------

@app.post("/farmer")
def register_farmer(farmer: FarmerRegistration):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO farmer (name, phone, preferred_language)
                       VALUES (%s, %s, %s) RETURNING id""",
                    (farmer.name, farmer.phone, farmer.preferred_language),
                )
                new_id = cur.fetchone()[0]
                conn.commit()
                return {"status": "created", "farmer_id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/crop")
def register_crop(crop: CropRegistration):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO crop (name, growth_stage, water_requirement_mm_per_day)
                       VALUES (%s, %s, %s) RETURNING id""",
                    (crop.name, crop.growth_stage, crop.water_requirement_mm_per_day),
                )
                new_id = cur.fetchone()[0]
                conn.commit()
                return {"status": "created", "crop_id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/field")
def register_field(field: FieldRegistration):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO field (farmer_id, crop_id, location_lat, location_lng, size_acres, sensor_id)
                       VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
                    (
                        field.farmer_id,
                        field.crop_id,
                        field.location_lat,
                        field.location_lng,
                        field.size_acres,
                        field.sensor_id,
                    ),
                )
                new_id = cur.fetchone()[0]
                conn.commit()
                return {"status": "created", "field_id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))