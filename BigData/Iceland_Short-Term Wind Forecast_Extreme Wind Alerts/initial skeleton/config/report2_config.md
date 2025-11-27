# Report 2 – Infrastructure Configuration

## 1. Cluster Overview

- Number of VMs: 2
- OS: Ubuntu (assumed)
- Project: Iceland Short-Term Wind Monitoring & Extreme Wind Alerts

### 1.1 Node roles

| Node | Hostname | Example IP     | Role summary                                |
|------|----------|----------------|---------------------------------------------|
| VM1  | vm1      | 10.0.0.4       | Master-ish: HDFS NN, Spark master, Kafka, TSDB, Grafana |
| VM2  | vm2      | 10.0.0.5       | Worker: HDFS DN, Spark worker              |

> Replace the IPs with your real Azure VM addresses.

---

## 2. Component Mapping

### 2.1 Hadoop / HDFS

| Component      | Role   | Host | Port(s)             | Notes                         |
|----------------|--------|------|---------------------|-------------------------------|
| HDFS NameNode  | Master | vm1  | 8020 (RPC), 9870 UI | `fs.defaultFS = hdfs://vm1:8020` |
| HDFS DataNode  | Worker | vm2  | 9864 UI             | Data storage                  |

HDFS data & checkpoint paths:

- Raw data: `hdfs://vm1:8020/data/weather/raw`
- Spark checkpoints:  
  - `hdfs://vm1:8020/checkpoints/weather_raw`
  - `hdfs://vm1:8020/checkpoints/weather_metrics` (for later)

### 2.2 Spark

| Component      | Role               | Host | Port(s)      | Notes                      |
|----------------|--------------------|------|--------------|----------------------------|
| Spark Master   | Master/Standalone  | vm1  | 7077, 8080 UI| Standalone cluster mode    |
| Spark Worker   | Worker/Executor    | vm2  | 8081 UI      | Connects to `spark://vm1:7077` |

### 2.3 Kafka

| Component     | Role       | Host | Port(s)   | Notes                                   |
|---------------|------------|------|-----------|-----------------------------------------|
| Zookeeper     | Coord      | vm1  | 2181      | Only if using ZooKeeper-based Kafka     |
| Kafka Broker  | Messaging  | vm1  | 9092      | `advertised.listeners=PLAINTEXT://vm1:9092` |

Kafka topics:

| Topic name            | Purpose                             | Partitions | Notes                    |
|-----------------------|-------------------------------------|------------|--------------------------|
| `weather_iceland_raw` | Raw forecast stream from Open-Meteo | 3          | Producer writes JSON     |

### 2.4 Time-Series Database & Grafana

| Component   | Role             | Host | Port | Notes                          |
|-------------|------------------|------|------|--------------------------------|
| TimescaleDB | Time-series DB   | vm1  | 5432 | PostgreSQL + Timescale         |
| Grafana     | Dashboard        | vm1  | 3000 | Connects to TimescaleDB       |

Planned tables (simplified):

- `weather_raw` (optional, HDFS is main raw store)
- `weather_metrics` (aggregated KPIs per location and time window)
- `weather_alerts` (extreme wind flags and durations)

---

## 3. Data Flow & Connections

1. **Producer → Kafka**  
   - Python script `producer/openmeteo_producer.py` runs on VM1 (or locally and points to VM1).  
   - Connects to Kafka broker `vm1:9092`.  
   - Sends JSON messages to topic `weather_iceland_raw`.

2. **Kafka → Spark → HDFS (raw landing)**  
   - Spark Structured Streaming job `spark/streaming_job_skeleton.py` runs on VM1 (master) and VM2 (worker).  
   - Reads from topic `weather_iceland_raw`.  
   - Writes raw data to `hdfs://vm1:8020/data/weather/raw` with checkpoint at `hdfs://vm1:8020/checkpoints/weather_raw`.

3. **(Later) Kafka → Spark → Time-Series DB → Grafana**  
   - Another streaming job will compute window metrics & alerts and write to TimescaleDB.  
   - Grafana reads from TimescaleDB and exposes dashboards.

---

## 4. Checkpoint 2 Demo Plan

For the Checkpoint 2 demo, the following steps will be shown:

1. Kafka topic `weather_iceland_raw` is created on VM1.  
2. The Python producer sends a few test messages into the topic.  
3. Spark Structured Streaming job starts, consuming from Kafka.  
4. New files appear under the HDFS path `/data/weather/raw`, proving that **data is landing in HDFS**.
