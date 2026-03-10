import os
import django
import pandas as pd
from datetime import date

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_agent_api.settings')
django.setup()

from core.models import ColdStorage, Scheme, CropProduction

def ingest_schemes():
    schemes = [
        {
            "name": "Pradhan Mantri Kisan SAMPADA Yojana (PMKSY)",
            "eligibility": "Farmers, FPOs, Entrepreneurs, Cooperatives.",
            "benefits": "Financial assistance for integrated cold chain and value addition infrastructure.",
            "application_process": "Apply through the MoFPI online portal."
        },
        {
            "name": "Mega Food Park Scheme",
            "eligibility": "SPVs (Special Purpose Vehicles) consisting of entrepreneurs.",
            "benefits": "Capital grant of 50% of the project cost in general areas and 75% in difficult areas.",
            "application_process": "Electronic application followed by physical submission."
        },
        {
            "name": "Unit for Creation/Expansion of Food Processing & Preservation Capacities (CEFPPC)",
            "eligibility": "Individual entrepreneurs, partnership firms, FPOs.",
            "benefits": "Grant-in-aid of 35% to 50% of the eligible project cost.",
            "application_process": "Portal-based application with mandatory documents."
        }
    ]
    for s in schemes:
        Scheme.objects.get_or_create(name=s["name"], defaults=s)
    print("Ingested Schemes.")

def ingest_mock_cold_storages():
    storages = [
        {
            "project_name": "Maharashtra Cold Chain Hub",
            "state": "Maharashtra",
            "district": "Pune",
            "capacity": 5000.0,
            "status": "Operational",
            "approval_date": date(2022, 1, 15),
            "project_cost": 25.5,
            "grant_released": 8.0
        },
        {
            "project_name": "Punjab Apple Store",
            "state": "Punjab",
            "district": "Ludhiana",
            "capacity": 2000.0,
            "status": "Under Implementation",
            "approval_date": date(2023, 5, 20),
            "project_cost": 15.0,
            "grant_released": 3.5
        }
    ]
    for storage_data in storages:
        ColdStorage.objects.get_or_create(project_name=storage_data["project_name"], defaults=storage_data)
    print("Ingested Mock Cold Storages.")

def ingest_mock_crop_production():
    crops = [
        {
            "state": "Maharashtra",
            "district": "Pune",
            "crop": "Tomato",
            "season": "Kharif",
            "area": 12000.0,
            "production": 350000.0,
            "year": "2023-24"
        },
        {
            "state": "Punjab",
            "district": "Ludhiana",
            "crop": "Potato",
            "season": "Rabi",
            "area": 15000.0,
            "production": 450000.0,
            "year": "2023-24"
        }
    ]
    for crop_data in crops:
        CropProduction.objects.get_or_create(
            state=crop_data["state"], 
            district=crop_data["district"], 
            crop=crop_data["crop"], 
            year=crop_data["year"], 
            defaults=crop_data
        )
    print("Ingested Mock Crop Production.")

if __name__ == "__main__":
    ingest_schemes()
    ingest_mock_cold_storages()
    ingest_mock_crop_production()
