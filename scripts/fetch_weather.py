import json
import re
import urllib.request
from datetime import datetime, timezone

ICAO = "SBPA"
API_URL = f"https://aviationweather.gov/api/data/metar?ids={ICAO}&format=json"
OUTPUT_PATH = "data/weather.json"


def fetch_metar():
    with urllib.request.urlopen(API_URL, timeout=20) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if not payload:
        raise RuntimeError(f"No METAR data returned for {ICAO}")
    return payload[0]


def build_record(metar):
    return {
        "icao": metar.get("icaoId", ICAO),
        "name": metar.get("name"),
        "lat": metar.get("lat"),
        "lon": metar.get("lon"),
        "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "obs_time_utc": metar.get("reportTime"),
        "wind": {
            "dir_deg": metar.get("wdir"),
            "speed_kt": metar.get("wspd"),
            "gust_kt": metar.get("wgst"),
        },
        "visibility_sm": metar.get("visib"),
        "flight_category": metar.get("fltCat"),
        "raw_metar": metar.get("rawOb"),
    }


def main():
    metar = fetch_metar()
    record = build_record(metar)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {OUTPUT_PATH}: {record['raw_metar']}")


if __name__ == "__main__":
    main()
