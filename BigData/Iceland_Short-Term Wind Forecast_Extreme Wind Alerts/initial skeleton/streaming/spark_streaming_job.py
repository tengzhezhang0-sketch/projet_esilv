{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "b6d94f3e",
   "metadata": {},
   "source": [
    "# Kafka to HDFS"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4a7b8ab5",
   "metadata": {},
   "outputs": [],
   "source": [
    "from pyspark.sql import SparkSession\n",
    "from pyspark.sql.functions import col\n",
    "\n",
    "def main():\n",
    "    # 创建sparksession\n",
    "    spark = (\n",
    "        SparkSession.builder\n",
    "        .appName(\"KafkaWeatherToHDFS\")\n",
    "        .getOrCreate()\n",
    "    )\n",
    "\n",
    "    # TODO: update Kafka bootstrap servers and topic name\n",
    "    # 从kafka读数据\n",
    "    df = (\n",
    "        spark.readStream\n",
    "        .format(\"kafka\") \n",
    "        .option(\"kafka.bootstrap.servers\", \"master:9092,worker1:9093\") # kafka集群地址\n",
    "        .option(\"subscribe\", \"weather_iceland_raw\") # 订阅kafka中的topic\n",
    "        .option(\"startingOffsets\", \"latest\") # 从最新的偏移量开始读\n",
    "        .load()\n",
    "    )\n",
    "    \n",
    "    # Just print raw JSON for now\n",
    "    lines = df.selectExpr(\"CAST(value AS STRING) as raw_line\") \n",
    "    # df 里 value 列是二进制类型（binary），转成字符串让spark读\n",
    "    # lines：只有一列的 DataFrame\n",
    "\n",
    "    # 定义一个流式写入(sink): 把流写成parquet文件\n",
    "    query = (\n",
    "    lines.writeStream\n",
    "    .format(\"parquet\")\n",
    "    .option(\"path\", \"/data/weather/raw\")\n",
    "    .option(\"checkpointLocation\", \"/checkpoints/weather_raw\")\n",
    "    .outputMode(\"append\")\n",
    "    .start()\n",
    ")\n",
    "\n",
    "\n",
    "    query.awaitTermination() # 让主线程卡在这里，持续运行流处理\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    main()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a2ba94e4",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": ".venv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
