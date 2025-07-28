from pathlib import Path
from rich.console import Console
import json
import polars as pl
from glob import glob
DATA_PATH = '/data/mirrulations/specific/DEA-2016-0015/raw-data/comments'
comment_id = 'DEA-2016-0015-12614.json'



def load_data(comment_id:str):
    
    fn = Path(DATA_PATH, comment_id)

    df = (
        pl.read_json(fn)
        .unnest('data')
        .unnest('attributes')
        .unnest('links')
    )

    return df

def load_data_json(comment_id:str):

    fn = Path(DATA_PATH, comment_id)

    with open(fn) as fh:
        d = json.load(fh)['data']['attributes']

    return d

def fetch_comments_df(docket_id:str):

    console = Console()

    path_template = f"/users/kriarm/data/mirrulations/specific/{docket_id}/raw-data/comments"

    all_json = glob(str(Path(path_template, "*.json")))

    data_json = []
    skipped_count = 0
    for jsonf in all_json:
        try:
            data = load_data_json(jsonf)
            data_json.append(data)
        except (KeyError, json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Skipping {jsonf}: {e}")
            skipped_count += 1
            continue

    total_files = len(all_json)
    processed_files = len(data_json)
    
    console.print(f"Processed {processed_files}/{total_files} comments. Skipped 0!")
    if skipped_count > 0:
        console.print(f"Skipped {skipped_count} comments due to errors")

    if not data_json:
        console.print("No valid JSON files found")
        return pl.DataFrame()

    try:
        df = pl.DataFrame(data_json, infer_schema_length=None)
        # Drop columns that are entirely null
        cols_to_keep = [col for col in df.columns if not df[col].is_null().all()]
        
    except pl.ComputeError as e:
        print(f"Schema error: {e}")
        print("Attempting to normalize data types...")
        
        # Normalize all values to strings to handle mixed types
        normalized_data = []
        for record in data_json:
            normalized_record = {k: str(v) if v is not None else None for k, v in record.items()}
            normalized_data.append(normalized_record)

        df = pl.DataFrame(normalized_data)
        # Drop columns that are entirely null
        cols_to_keep = [col for col in df.columns if not df[col].is_null().all()]

    TIME_COLUMNS = ["modifyDate", "receiveDate", "postedDate"]
    
    # Cast time columns to datetime if they exist in the dataframe
    existing_time_cols = [col for col in TIME_COLUMNS if col in df.columns]
    
    df = df.select(cols_to_keep)
    
    for col in existing_time_cols:
        df = df.with_columns(pl.col(col).str.to_datetime(format=None, strict=False))
    
    return df

if __name__ == "__main__":

    df = fetch_comments_df(docket_id="DEA-2016-0015")