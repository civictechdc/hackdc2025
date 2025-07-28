# Hive-partioned Parquet for Mirrulations

This repository demos writing Mirrulations data with a [Hive-partitioned Parquet](https://duckdb.org/docs/stable/data/partitioning/hive_partitioning.html#hive-partitioning) storage strategy. This is an approach for building data lakes that uses a cloud-optimized file format and structure that enables efficient and fast querying, even directly from cloud object storage.

This work was done as part of [Civic Hack DC](https://www.civictechdc.org/events/civichackdc/) in July 2025.

## Why Parquet?

[Apache Parquet](https://parquet.apache.org/) is a modern columnar tabular data file format. Some advantages of Parquet include:

- It is a columnar data format. This means that if you only care about certain columns in the data, your query engine can ignore other non-relevant columns and efficiently read less data.
- It supports filter pushdown. Parquet stores metadata about groups of rows. If you have filters in your query, query engines can read that metatadata to skip reading irrelevant parts of the data.
- The specification natively supports modern compression algorithms and uses compression by default. In this demo, 2.5 GB of JSON data was compressed into 424 MB of Parquet.
- It is a self-describing typed format. This means that the column types are saved as part of the file, so you won't run into problems where numeric data is treated like a string, or vice versa—a common pain point for CSV files..
- Parquet supports nested data types, so even though the raw data are fairly complex nested data structures, it can handle storing and querying that data natively.
- Parquet has wide support across modern tools for working with tabular data, like DuckDB, Pandas, Polars.

## Why Hive-partitioning?

[Hive-partitioning](https://duckdb.org/docs/stable/data/partitioning/hive_partitioning.html#hive-partitioning) is a partitioning strategy for splitting a dataset up into multiple files with a particular folder structure. The structure, example shown below, allows query engines to perform filter pushdown and skip reading files that aren't relevant to a query.

```
.
└── parquet/
    ├── comments/
    │   ├── agency_code=CMS/
    │   │   ├── year=2022/
    │   │   │   ├── docket_id=CMS-2022-0001/
    │   │   │   │   ├── data_0.parquet
    │   │   │   │   ├── data_1.parquet
    │   │   │   │   └── ...
    │   │   │   └── docket_id=CMS-2022-0002/
    │   │   │       └── ...
    │   │   └── year=2023/
    │   │       └── ...
    │   ├── agency_code=DEA/
    │   │   └── ...
    │   └── agency_code=FTA/
    │       └── ...
    ├── dockets/
    │   ├── agency_code=CMS/
    │   │   └── ...
    │   ├── agency_code=DEA/
    │   │   └── ...
    │   └── ...
    └── documents/
        └── ...
```

## This demo

### Data

The notebooks in this repository use a dataset distributed during the Civic Hack DC event. The dataset was a subset of the data from the [Mirrulations](https://registry.opendata.aws/mirrulations/) dataset. It looked something like this, relative to the repository root.

```
.
└── mirrulations/
    └── bulk/
        └── raw-data/
            ├── CMS/
            │   ├── CMS-2022-0001
            │   ├── CMS-2022-0002
            │   └── ...
            ├── DEA/
            │   ├── DEA-2016-0002
            │   └── ...
            └── FTA/
                └── ...

```

### Environment set up

This project uses [uv](https://docs.astral.sh/uv/) to manage the Python environment. To set up the environment, run:

```bash
uv sync
```

### Notebooks

#### `to_hive_partitioned_parquet.ipynb`

This notebook reads the `raw-data` JSON files and writes it out to `./parquet` in a Hive-partitioned parquet format. The SQL queries flatten some hand-picked fields into columns as a demonstration.

#### `example_queries.ipynb`

This notebook demos using DuckDB to query the Hive-partioned dataset, including directly from an S3 bucket. It shows that DuckDB can query this dataset relatively quickly, including through filter pushdown and skipping reading files, and gives you the power of using a SQL query engine for querying that data.

## Some notes about future production implementation

- Some kind of batch job will be needed to continually transform new data from the JSON format into the Hive-partitioned Parquet data lake.
- There are a few different strategies for implementing the transformation job:
    - Distributed processing systems like AWS Glue+AWS Athena or Spark support writing out data both in Parquet and with Hive-partitioning. They can process large datasets quickly through parallelization and a large amount of compute.
    - You could also do it in a more DIY manner using something like DuckDB, which is what this demo used. If this is slow, you'd need to parallelize it and distribute it yourself.
- More thoughtful design should be conducted with regards to what are the right partition keys, and what fields should be pulled out of the JSON as columns in Parquet, based on what expected query patterns will be. Additionally, some nested array fields like attachments could be split out into additional entitites, like `comment_attachments`.
