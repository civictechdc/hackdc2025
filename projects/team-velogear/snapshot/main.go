package main

import (
	"encoding/csv"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"os/exec"
	"strings"

	"github.com/xitongsys/parquet-go-source/local"
	"github.com/xitongsys/parquet-go/parquet"
	"github.com/xitongsys/parquet-go/writer"
)

type Line struct {
	Line string `parquet:"name=line, type=BYTE_ARRAY, convertedtype=UTF8"`
}

func main() {
	// Define command-line flags
	inputFile := flag.String("input", "", "Input PDF file")
	outputFormat := flag.String("output", "text", "Output format (text, csv, json, parquet)")
	flag.Parse()

	// Check if input file is provided
	if *inputFile == "" {
		fmt.Println("Input PDF file is required. Use the -input flag.")
		os.Exit(1)
	}

	// Extract text from PDF using pdftotext
	cmd := exec.Command("pdftotext", *inputFile, "-")
	out, err := cmd.Output()
	if err != nil {
		log.Fatalf("Error extracting text with pdftotext: %v", err)
	}

	// Process extracted text
	textData := strings.Split(string(out), "\n")

	// Output the data in the specified format
	switch *outputFormat {
	case "text":
		for _, line := range textData {
			fmt.Println(line)
		}
	case "csv":
		writer := csv.NewWriter(os.Stdout)
		defer writer.Flush()
		for _, line := range textData {
			writer.Write([]string{line})
		}
	case "json":
		jsonData, err := json.MarshalIndent(textData, "", "  ")
		if err != nil {
			fmt.Printf("Error creating JSON: %v", err)
			os.Exit(1)
		}
		fmt.Println(string(jsonData))
	case "parquet":
		outputFile := strings.TrimSuffix(*inputFile, ".pdf") + ".parquet"
		fw, err := local.NewLocalFileWriter(outputFile)
		if err != nil {
			log.Fatalf("Error creating Parquet file: %v", err)
		}
		defer fw.Close()

		pw, err := writer.NewParquetWriter(fw, new(Line), 4)
		if err != nil {
			log.Fatalf("Error creating Parquet writer: %v", err)
		}
		defer pw.WriteStop()

		pw.RowGroupSize = 128 * 1024 * 1024 // 128M
		pw.CompressionType = parquet.CompressionCodec_SNAPPY

		for _, line := range textData {
			if err := pw.Write(Line{Line: line}); err != nil {
				log.Fatalf("Error writing to Parquet file: %v", err)
			}
		}

		fmt.Printf("Parquet file created: %s\n", outputFile)
	default:
		fmt.Println("Invalid output format. Use 'text', 'csv', 'json', or 'parquet'.")
		os.Exit(1)
	}
}
