# Mirrulations

A command-line tool for working with dockets from regulations.gov via the [Mirrulations dataset](https://registry.opendata.aws/mirrulations/).

This tool currently has two commands that wrap two existing scripts:

- `mirrulations fetch` — Download all data for a specific docket by ID. See [documentation](https://github.com/mirrulations/mirrulations-fetch/).
- `mirrulations csv` — Reformat comments data as a tabular CSV file. See [documentation](https://github.com/mirrulations/mirrulations-csv).

## Example usage

```bash
# Download Docket CMS-2019-0039 to ./CMS-2019-0039
mirrulations fetch CMS-2019-0039

# Transform comments into a CSV to ./CMS-2019-0039.csv
mirrulations csv CMS-2019-0039/raw-data/comments/
```

## Excluding file types

`mirrulations fetch` supports a multiple use `--exclude` flag to exclude certain file types. By default, the following types are downloaded: `docket`, `documents`, `comments`, `derived`.

For example, to exclude `comments` and `derived` and to only include `docket` and `documents`:

```bash
mirrulations fetch CMS-2019-0039 --exclude comments --exclude derived
```
