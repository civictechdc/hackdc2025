# Mirrulations CLI on PyPI

**Team:** Jay Qi ([@jayqi](https://github.com/jayqi))  
**Hackathon:** Civic Hack DC 2025  
**Challenge:** Download Tools

## 🎯 Problem Statement

Accessing the Mirrulations dataset from S3 requires knowledge of tools for working with S3 and about the dataset storage structure. An easy-to-install command-line tool makes the data more accessible to more people.

**Description:**
Check out the full [project readme](./upstream/README.md) for more details.

## 💡 Solution

In preparation for the event, Prof. Ben Coleman provided two scripts on GitHub to download data for a single docket and to transform it into a tabular format. Using these scripts require cloning two repositories and setting up Python virtual environments to run them.

Python packages and the Python Package Index (PyPI) is the way that many open source Python tools are distributed. Python package managers allow users to easily install and use these packages by only requiring that users know the package's name.

In this project, the two scripts were combined into a single package named `mirrulations` to simplify access to the functionality. The package was then published to PyPI, which makes it easy to `pip install mirrulations`. If using the modern package manager uv, a user could even run `uvx mirrulations ...` to directly invoke the tool in one line and skip having to manually install the package themselves. During the event, an improvement was also quickly implemented and published to allow users to exclude certain subsets of a docket's data to reduce the amount of data download needed. Distributing the tool as a package on PyPI streamlines the process of accessing the Mirrulations regulatory comment data for researchers and developers.

## 🚀 Repository

**GitHub:** [jayqi/mirrulations-cli](https://github.com/jayqi/mirrulations-cli)
**PyPI:** [mirrulations](https://pypi.org/project/mirrulations/)

## 🛠️ Tech Stack

- Approach: Python CLI package
- Distribution: PyPI
- Tools: uv, pip
- APIs: Amazon S3

## 📦 Example usage

```bash
## Download Docket CMS-2019-0039 to ./CMS-2019-0039

# Use with pip
pip install mirrulations
mirrulations fetch CMS-2019-0039

##

# Or, use uvx for a direct one-liner
uvx mirrulations fetch CMS-2019-0039
```

## 🤝 Team Members

- **Jay Qi** ([@jayqi](https://github.com/jayqi))
