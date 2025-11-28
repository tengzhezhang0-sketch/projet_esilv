#!/usr/bin/env bash
# 提交kafka_streaming_job到yarn
# 用hadoop用户跑

/opt/spark/bin/spark-submit \
# 指定Spark的集群管理器 -> 用Hadoop YARN作为资源管理调度
  --master yarn \ 
  --deploy-mode client \
  # 运行时自动下载并加载Spark Kafka连接器这个依赖包
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.7 \
  # python主程序路径
  /home/hadoop/bigdata-iceland-wind/streaming/spark_streaming_job.py

