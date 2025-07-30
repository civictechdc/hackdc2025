# Hive-partitioned Parquet

**Team:** Jay Qi ([@jayqi](https://github.com/jayqi))  
**Hackathon:** Civic Hack DC 2025  
**Challenge:** Data Accessibility & Cost / Data Quality & Derived Layers

## 🎯 Problem Statement

The Mirrulations dataset contains over 2.3 TB of data, including 640 GB of text. Much of the data is well-structured and stored in a JSON format in cloud object storage. However, the size and format of the dataset can make it potentially difficult to work with. JSON-formatted files are monolithic—in general, the entire file needs to be downloaded and opened in order to access any of the contents. This means that users often need to download large sets of entire files even if they only need a small portion of the information for their query or analysis.

## 💡 Solution

This project implements a proof-of-concept data pipeline that transforms the data from JSON to a storage structure that uses Parquet files as the data format and a structure called Hive partitioning. These are two modern data engineering techniques that work well with cloud object storage. Compatibility with modern tools means that users can use SQL or popular dataframe libraries like Polars to directly and efficiently query from the remote files—the modern tools will intelligently apply filtering so that only portions of the data relevant to the query will be scanned or downloaded. This strategy enables better performance for performing data analysis over the large dataset.

The linked repository contains a data pipeline for transforming the data, implemented using DuckDB. It also contains a demonstration notebook that shows how DuckDB can efficiently and performantly perform SQL queries against the Hive-partitioned data, where only relevant subsets of the data are transferred. The demo uses a transformed sample of the dataset in remote S3 storage. The README contains an in-depth discussion of the advantages of Parquet and of Hive partitioning.

**Description:**
Check out the full [project readme](./upstream/README.md) for more details.

## 🚀 Repository

**GitHub:** [jayqi/mirrulations-hive-partitioned-parquet](https://github.com/jayqi/mirrulations-hive-partitioned-parquet)

## 🛠️ Tech Stack

- Query Engine: DuckDB
- Development environment: Jupyter notebooks
- Strategy: Hive-partitioned Parquet
- Storage: S3-compatible storage

## Team Members

- **Jay Qi** ([@jayqi](https://github.com/jayqi))
