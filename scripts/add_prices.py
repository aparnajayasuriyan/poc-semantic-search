import os
import json
import math
import random

random.seed(42)

RANGES = {
    "Camera Body": (300.0, 8000.0),
    "Lens": (80.0, 6000.0),
    "External Flash": (50.0, 1500.0),
    "Lighting Kit": (50.0, 2500.0),
    "Video Light": (30.0, 1200.0),
    "Microphone": (50.0, 1200.0),
    "Audio Recorder": (50.0, 900.0),
    "Gimbal": (150.0, 4000.0),
    "Tripod": (20.0, 1200.0),
    "Camera Bag": (20.0, 800.0),
    "Memory Card": (10.0, 400.0),
    "Battery": (20.0, 200.0),
    "Accessory": (5.0, 600.0),
    "Filter": (10.0, 400.0),
    "Monitor": (200.0, 3000.0),
    "Storage": (50.0, 1200.0),
}

DEFAULT_RANGE = (10.0, 900.0)

def sample_price(cat: str) -> float:
    low, high = RANGES.get(cat, DEFAULT_RANGE)
    # use log-uniform sampling for realistic spread across decades
    if low <= 0 or high <= 0:
        return round(random.uniform(low, high), 2)
    val = math.exp(random.uniform(math.log(low), math.log(high)))
    return round(val, 2)

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(repo_root, "data", "camera_catalog.json")
    backup_path = data_path + ".bak"

    if not os.path.exists(data_path):
        raise SystemExit(f"Catalog not found: {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # backup original
    if not os.path.exists(backup_path):
        with open(backup_path, "w", encoding="utf-8") as bf:
            json.dump(catalog, bf, indent=2)

    for product in catalog:
        if "price" not in product:
            price = sample_price(product.get("category", ""))
            product["price"] = price

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    print(f"Wrote {len(catalog)} entries to {data_path} (backup at {backup_path})")
    print("Sample entries:")
    for p in catalog[:6]:
        print(f"- id={p.get('id')} name={p.get('name')[:40]} price=${p.get('price')}")

if __name__ == '__main__':
    main()
