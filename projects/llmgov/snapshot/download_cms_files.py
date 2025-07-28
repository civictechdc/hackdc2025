#!/usr/bin/env python3

import boto3
import os
import concurrent.futures
from botocore.exceptions import ClientError
from botocore import UNSIGNED
from botocore.config import Config


def download_s3_files(bucket_name, prefix, local_dir=None, use_unsigned=True):
    """
    Download all files from an S3 bucket with a specific prefix

    Args:
        bucket_name (str): The S3 bucket name
        prefix (str): The prefix/folder to download from
        local_dir (str): Local directory to save files (defaults to current directory)
        use_unsigned (bool): Whether to use unsigned requests (no authentication)
    """
    if local_dir is None:
        local_dir = os.getcwd()

    # Create local directory if it doesn't exist
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # Initialize S3 client
    if use_unsigned:
        # Use unsigned requests (--no-sign-request equivalent)
        s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        print("Using unsigned requests (--no-sign-request)")
    else:
        s3_client = boto3.client("s3")

    try:
        # List all objects with the given prefix
        print(f"Listing objects in s3://{bucket_name}/{prefix}")
        paginator = s3_client.get_paginator("list_objects_v2")
        files_to_download = []

        # Paginate through results
        for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
            if "Contents" in page:
                for obj in page["Contents"]:
                    files_to_download.append(obj["Key"])

        total_files = len(files_to_download)
        print(f"Found {total_files} files to download")

        if total_files == 0:
            print("No files found matching the prefix.")
            return

        # Function to download a single file
        def download_file(s3_key):
            # Create local path - preserve directory structure
            relative_path = s3_key
            if prefix and s3_key.startswith(prefix):
                relative_path = s3_key[len(prefix) :]
                if relative_path.startswith("/"):
                    relative_path = relative_path[1:]

            # Prefix directories under CMS with "CMS-2025-"
            path_parts = relative_path.split("/")
            if len(path_parts) > 1:  # If there are subdirectories
                # The first part might be empty if the path starts with a slash
                first_non_empty_idx = 0
                while (
                    first_non_empty_idx < len(path_parts)
                    and not path_parts[first_non_empty_idx]
                ):
                    first_non_empty_idx += 1

                # If we have a valid directory part, prefix it
                if (
                    first_non_empty_idx < len(path_parts) - 1
                ):  # Make sure it's not the filename
                    path_parts[first_non_empty_idx] = (
                        f"CMS-2025-{path_parts[first_non_empty_idx]}"
                    )
                    relative_path = "/".join(path_parts)

            local_file_path = os.path.join(local_dir, relative_path)

            # Create directories if they don't exist
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

            # Download the file
            try:
                s3_client.download_file(bucket_name, s3_key, local_file_path)
                print(f"Downloaded: {s3_key} -> {local_file_path}")
                return True
            except Exception as e:
                print(f"Error downloading {s3_key}: {str(e)}")
                return False

        # Download files using thread pool for better performance
        successful_downloads = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(download_file, files_to_download))
            successful_downloads = sum(results)

        print(
            f"Download complete. {successful_downloads}/{total_files} files downloaded successfully."
        )

    except ClientError as e:
        print(f"AWS Error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    # Configuration
    bucket_name = "mirrulations"
    prefix = "raw-data/CMS/CMS-2025"
    local_download_dir = "./raw_data/CMS"

    # Download the files with unsigned requests (equivalent to --no-sign-request)
    download_s3_files(bucket_name, prefix, local_download_dir, use_unsigned=True)
