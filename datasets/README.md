# Datasets

This is a sample slice of the Mirrulations dataset, does not include the raw attachments, but does include some of the derived data from the pdf comments. The top-level structure might not be exactly the same as the full dataset, but the docket-level structure and files themselves are the same.

The dataset is stored in a [./dataset.tar.gz](./dataset.tar.gz) file

It's a mixed bag of bulk data and specific dockets. The output structure is as follows:

## File Structure

```
datasets.tar.gz/
    bulk/
      derived-data/
      └── <agency>
          └── <docket id>
              └── mirrulations
                  └── extracted_txt
                      └── comments_extracted_text
                          └── pdfminer
                              ├── <docket id>_<comment id>_attachment_<num>_extracted.
                              └── ...
      raw-data/ 
      └── <agency>
          └── <docket id>
              └── text-<docket id>
                  ├── comments
                  │   ├── <docket id>_<comment id>.json
                  │   └── ...
                  ├── docket
                  │   ├── <docket id>.json
                  |   └── ...
                  └── documents
                      ├── <document id>.json
                      ├── <document id>_content.htm
                      └── ...

    specific/
    ├── CMS-2019-0039
    │   └── ...
    ├── CMS-2022-0163
    │   └── ...
    ├── CMS-2025-0050
    │   └── ...
    ├── DEA-2016-0015
    │   └── ...
    ├── DEA-2024-0059
    │   └── ...
    └── HHS-ONC-2019-0002
        └── derived-data/
            └── mirrulations
                └── extracted_txt
                    └── comments_extracted_text
                        └── pdfminer
                            ├── <docket id>_<comment id>_attachment_<num>_extracted.txt
                            └── ...
            raw-data/ 
            └── text-<docket id>
                ├── comments
                │   ├── <docket id>_<comment id>.json
                │   └── ...
                ├── docket
                │   ├── <docket id>.json
                |   └── ...
                └── documents
                    ├── <document id>.json
                    ├── <document id>_content.htm
                    └── ...
```

use the `mirrulations-fetch` tool to download the full dataset.
