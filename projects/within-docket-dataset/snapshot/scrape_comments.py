# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 12:22:32 2025

@author: skama
"""

import os
import pandas as pd
import json

#%%
def list_subdirectories(folder_path):
    subdirectories = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    return subdirectories

def list_files(folder_path):
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(file_path)
    return files

def create_dataframe(folder_path):
    data = []
    subdirectories = list_subdirectories(folder_path)
    for subdir in subdirectories:
        subdir_path = os.path.join(folder_path, subdir)
        subsubdirs = list_subdirectories(subdir_path)
        for subsubdir in subsubdirs:
            subsubdir_path = os.path.join(subdir_path, subsubdir)
            files = list_files(subsubdir_path)
            for file in files:
                file_name, file_extension = os.path.splitext(os.path.basename(file))
                data.append({'ID': len(data) + 1, 'RootFolder':subdir, 'FolderName': subsubdir, 'FileName': file_name, 'FileExtension': file_extension})
    df = pd.DataFrame(data)
    return df


import json
import pandas as pd

def load_nested_json(file_path, record_key):
    """
    Loads a nested JSON file and returns a selected list of records as a DataFrame.

    Parameters:
    - file_path (str): Path to the JSON file.
    - record_key (list of str): Keys to navigate through the nested structure
                                to reach the list of records.

    Returns:
    - pd.DataFrame: DataFrame containing the selected records.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Navigate through nested keys
        for key in record_key:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                raise KeyError(f"Key '{key}' not found in the JSON structure.")

        # Convert to DataFrame
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            return pd.DataFrame([data])
        else:
            raise ValueError("Selected data is neither a list nor a dict.")
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return pd.DataFrame()
    
def safe_load_json(filepath):
    """
    Safely loads a JSON file. Returns None if the file is empty or invalid.
    """
    try:
        if os.path.getsize(filepath) == 0:
            print(f"Skipped empty file: {filepath}")
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    except json.JSONDecodeError as e:
        print(f"JSON decode error in file {filepath}: {e}")
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

#%%
#Docket File Path
raw_comment_directory = r"C:\Users\skama\Downloads\Mirrulations Dockets\CMS-2019-0039\raw-data\comments"
pdf_comment_directory = r"C:\Users\skama\Downloads\Mirrulations Dockets\CMS-2019-0039\derived-data"

#Data Inventory DF
comment_inventory = list_files(raw_comment_directory)

pdf_comment_inventory = list_files(pdf_comment_directory) 



#Get all raw text comments
raw_text_comments = []
for file in comment_inventory:
    
    json_file = safe_load_json(file)
    
    comment_id = json_file['data']['id'] 
    
    comment_attributes = load_nested_json(file, record_key=['data', 'attributes'])
    comment_attributes['comment_id'] = comment_id
    
    raw_text_comments.append(comment_attributes)
    

#get PDF comments
pdf_text_comments = {}
for filepath in pdf_comment_inventory:
    
    comment_id = filepath.rsplit('\\', 1)[1].split('_', 1)[0]
    
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    pdf_text_comments[comment_id] = content
    

comments_df = pd.concat(raw_text_comments)
pdf_comments_df = pd.DataFrame.from_dict(pdf_text_comments, orient = 'index', columns = ['comment_text']).reset_index().rename(columns={'index': 'comment_id'})

comments_df = comments_df.merge(pdf_comments_df, on = 'comment_id', how = 'left')


comments_df_slim = comments_df[['docketId', 'commentOnDocumentId',  'comment_id', 'modifyDate', 'postedDate', 'receiveDate', 'comment', 'comment_text']]