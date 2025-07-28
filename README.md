# PDF Parser

This is a simple command-line tool written in Go to parse text from PDF files and output it to standard output, CSV, JSON, or Parquet format.

This tool relies on the `pdftotext` command-line utility, which is part of the `poppler-utils` package.

## Installation

1.  **Install Go:** Make sure you have Go installed on your system. You can download it from [https://golang.org/](https://golang.org/).

2.  **Install `poppler-utils`:** You need to install the `poppler-utils` package, which provides the `pdftotext` utility.

    *   **On Debian/Ubuntu:**
        ```bash
        sudo apt-get update
        sudo apt-get install poppler-utils
        ```

    *   **On CentOS/RHEL:**
        ```bash
        sudo yum install poppler-utils
        ```

    *   **On macOS (using Homebrew):**
        ```bash
        brew install poppler
        ```

3.  **Build the `pdf-parser`:**
    ```bash
    git clone <repository_url>
    cd pdf-parser
    go build -o pdf-parser main.go
    ```

## Usage

To use the `pdf-parser`, run the following command:

```bash
./pdf-parser -input=<path_to_your_pdf_file> -output=<text|csv|json|parquet>
```

### Command-line Flags

*   `-input`: (Required) The path to the input PDF file.
*   `-output`: (Optional) The output format. Can be `text`, `csv`, `json`, or `parquet`. Defaults to `text`.

### Examples

*   **Text Output (default):**
    ```bash
    ./pdf-parser -input=my_document.pdf
    ```

*   **CSV Output:**
    ```bash
    ./pdf-parser -input=my_document.pdf -output=csv
    ```

*   **JSON Output:**
    ```bash
    ./pdf-parser -input=my_document.pdf -output=json
    ```

*   **Parquet Output:**
    ```bash
    ./pdf-parser -input=my_document.pdf -output=parquet
    ```