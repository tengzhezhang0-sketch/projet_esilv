# Kafka message schema: `weather_iceland_raw`

## exemple
```json
{
  "location_id": "reykjavik",
  "latitude": 64.13,
  "longitude": -21.94,
  "forecast_time": 1731576000,
  "ingest_time": 1731572400,
  "wind_speed_10m": 18.5,
  "wind_gusts_10m": 26.3,
  "temperature_2m": 3.1,
  "precipitation": 0.4,
  "pressure_msl": 1002.3
}
```
---
**forecast_time:** event time (Unix timestamp, UTC)

**ingest_time:** processing time when the record is sent to Kafka