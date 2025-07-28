import os
import sys
import time
import threading
import queue
import click
import boto3
from botocore import UNSIGNED
from botocore.config import Config


BUCKET = 'mirrulations'
RAW_DATA_PREFIX = 'raw-data'
DERIVED_DATA_PREFIX = 'derived-data'

s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))

def get_agency(docket):
    return docket.split('-')[0].split('_')[0]


def s3_key_exists(prefix):
    resp = s3_client.list_objects_v2(Bucket=BUCKET, Prefix=prefix, MaxKeys=1)
    return 'Contents' in resp and len(resp['Contents']) > 0

def download_file(s3_key, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    s3_client.download_file(BUCKET, s3_key, local_path)

def get_file_list(prefix, file_type=None):
    count = 0
    total_size = 0
    files = []
    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix):
        for obj in page.get('Contents', []):
            files.append({'Key': obj['Key'], 'Size': obj['Size']})
        count = len(files)
        total_size = sum(f['Size'] for f in files)
        if file_type:
            print(f"{file_type}: {count}", end='\r', flush=True)
    if file_type:
        print(f"{file_type}: {count}")
    return files, total_size

def relative_s3_path(s3_key, base_prefix):
    return os.path.relpath(s3_key, base_prefix)

def print_stats(stats, totals, start_times):
    text_total = totals['text']
    text_done = stats['docket'] + stats['documents'] + stats['comments'] + stats.get('derived', 0)
    elapsed_text = time.time() - start_times['text']
    text_rate = text_done / elapsed_text if elapsed_text > 0 else 0
    text_remain = text_total - text_done
    text_eta = (text_remain / text_rate) if text_rate > 0 else float('inf')
    text_eta_str = f"{int(text_eta // 60):2d}m{int(text_eta % 60):02d}s" if text_eta != float('inf') else '  N/A '
    output = f"Text: {text_done:6}/{text_total:6} ETA:{text_eta_str:7}"
    if 'binary' in stats:
        bin_total = totals['binary']
        bin_done = stats['binary']
        if start_times['binary'] is None and bin_done > 0:
            start_times['binary'] = time.time()
        elapsed_bin = (time.time() - start_times['binary']) if start_times['binary'] else 0
        bin_rate = bin_done / elapsed_bin if elapsed_bin > 0 else 0
        bin_remain = bin_total - bin_done
        bin_eta = (bin_remain / bin_rate) if bin_rate > 0 else float('inf')
        bin_eta_str = f"{int(bin_eta // 60):2d}m{int(bin_eta % 60):02d}s" if bin_eta != float('inf') else '  N/A '
        output += f" | Bin: {bin_done:6}/{bin_total:6} ETA:{bin_eta_str:7}"
    print(f"\r{output.ljust(80)}", end='', flush=True)

def download_worker(q, stats, totals, start_times, base_prefix, output_folder):
    while True:
        item = q.get()
        if item is None:
            break
        s3_key, file_type, size = item
        rel_path = relative_s3_path(s3_key, base_prefix[file_type])
        # Place raw-data files under raw-data/, derived-data files under derived-data/
        if file_type in ('docket', 'documents', 'comments', 'binary'):
            local_path = os.path.join(output_folder, 'raw-data', rel_path)
        elif file_type == 'derived':
            local_path = os.path.join(output_folder, 'derived-data', rel_path)
        else:
            local_path = os.path.join(output_folder, rel_path)
        try:
            download_file(s3_key, local_path)
            if file_type in stats:
                stats[file_type] += 1
        except Exception as e:
            print(f"\nError downloading {s3_key}: {e}", file=sys.stderr)
            sys.exit(1)
        stats['remaining'][file_type] -= 1
        print_stats(stats, totals, start_times)
        q.task_done()


@click.command("fetch")
@click.argument('docket_id')
@click.option('--output-folder', default='.', help='Target output folder (default: current directory)')
@click.option('--exclude', multiple=True, help="Exclude specifc file types from download. Options: docket, documents, comments, derived")
@click.option('--include-binary', is_flag=True, help='Include binary data in download')
def main(docket_id, output_folder, exclude, include_binary):
    agency = get_agency(docket_id)
    # S3 prefixes
    raw_agency_docket_prefix = f'{RAW_DATA_PREFIX}/{agency}/{docket_id}/'
    raw_text_prefix = f'{RAW_DATA_PREFIX}/{agency}/{docket_id}/text-{docket_id}/'
    raw_binary_prefix = f'{RAW_DATA_PREFIX}/{agency}/{docket_id}/binary-{docket_id}/'
    derived_prefix = f'{DERIVED_DATA_PREFIX}/{agency}/{docket_id}/'
    if not s3_key_exists(raw_agency_docket_prefix):
        print(f"Docket {docket_id} for agency {agency} not found in S3 bucket.", file=sys.stderr)
        sys.exit(1)
    if not s3_key_exists(raw_text_prefix):
        print(f"Text data for docket {docket_id} not found.", file=sys.stderr)
        sys.exit(1)
    print("Preparing download lists...")
    file_lists = {}
    total_sizes = {}
    if 'docket' not in exclude:
        file_lists['docket'], total_sizes['docket'] = get_file_list(f'{RAW_DATA_PREFIX}/{agency}/{docket_id}/text-{docket_id}/docket/', 'docket')
        print(f"Docket total size:   {total_sizes['docket']/1e6:.2f} MB")
    else:
        print("Skipping docket data download")
    if 'documents' not in exclude:
        file_lists['documents'], total_sizes['documents'] = get_file_list(f'{RAW_DATA_PREFIX}/{agency}/{docket_id}/text-{docket_id}/documents/', 'documents')
        print(f"Document total size: {total_sizes['documents']/1e6:.2f} MB")
    else:
        print("Skipping document data download due to --exclude")
    if 'comments' not in exclude:
        file_lists['comments'], total_sizes['comments'] = get_file_list(f'{RAW_DATA_PREFIX}/{agency}/{docket_id}/text-{docket_id}/comments/', 'comments')
        print(f"Comment total size:  {total_sizes['comments']/1e6:.2f} MB")
    else:
        print("Skipping comment data download due to --exclude")
    if 'derived' not in exclude:
        if s3_key_exists(derived_prefix):
            file_lists['derived'], total_sizes['derived'] = get_file_list(derived_prefix, 'derived')
            print(f"Derived total size:  {total_sizes['derived']/1e6:.2f} MB")
        else:
            print("Derived data not found - skipping")
    else:
        print("Skipping derived data download due to --exclude")
    if include_binary and s3_key_exists(raw_binary_prefix):
        file_lists['binary'], total_sizes['binary'] = get_file_list(raw_binary_prefix, 'binary')
        print(f"Binary total size:   {total_sizes['binary']/1e6:.2f} MB")
    # Stats
    totals = {
        'text': len(file_lists.get('docket', [])) + len(file_lists.get('documents', [])) + len(file_lists.get('comments', []))
    }
    if 'derived' in file_lists:
        totals['text'] += len(file_lists['derived'])
    stats = {
        'docket': 0,
        'documents': 0,
        'comments': 0,
        'remaining': {k: len(v) for k, v in file_lists.items()}
    }
    if 'derived' in file_lists:
        stats['derived'] = 0
    start_times = {'text': time.time(), 'binary': None}
    if 'binary' in file_lists:
        totals['binary'] = len(file_lists['binary'])
        stats['binary'] = 0
    base_prefix = {
        'docket': f'{RAW_DATA_PREFIX}/{agency}/{docket_id}/text-{docket_id}/',
        'documents': f'{RAW_DATA_PREFIX}/{agency}/{docket_id}/text-{docket_id}/',
        'comments': f'{RAW_DATA_PREFIX}/{agency}/{docket_id}/text-{docket_id}/',
        'binary': f'{RAW_DATA_PREFIX}/{agency}/{docket_id}/',
        'derived': derived_prefix,
    }
    # Download queue
    q = queue.Queue()
    for file_type, files in file_lists.items():
        for f in files:
            q.put((f['Key'], file_type, f['Size']))
    num_threads = min(8, q.qsize())
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=download_worker, args=(q, stats, totals, start_times, base_prefix, os.path.join(output_folder, docket_id)))
        t.start()
        threads.append(t)
    q.join()
    for _ in threads:
        q.put(None)
    for t in threads:
        t.join()
    print("\nStep 4 complete: Download finished.")
    print("All files for docket {0} have been downloaded to {1}".format(docket_id, os.path.abspath(os.path.join(output_folder, docket_id))))

if __name__ == '__main__':
    main()
