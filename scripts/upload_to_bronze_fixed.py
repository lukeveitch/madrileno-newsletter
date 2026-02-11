import json
from google.cloud import bigquery
import pandas as pd
from datetime import datetime
import os

# Initialize BigQuery client
client = bigquery.Client(project='madrid-newsletter')

def extract_data_from_file(json_file):
    """Extract the actual data array from your JSON structure"""
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle different JSON structures
    if isinstance(data, dict):
        # For newsdata files
        if 'newsdata' in data and 'results' in data['newsdata']:
            return data['newsdata']['results']
        # For events files that might have 'events' or 'data' key
        elif 'events' in data:
            return data['events']
        elif 'data' in data:
            return data['data']
        elif 'results' in data:
            return data['results']
        # If it's a dict but contains the data directly
        else:
            # Try to find the largest list in the dict
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 0:
                    return value
    elif isinstance(data, list):
        # If it's already a list, return as-is
        return data
    
    # Fallback - return empty list
    return []

def upload_json_to_bigquery(json_file, table_id, table_description):
    """Upload JSON data to BigQuery table"""
    
    if not os.path.exists(json_file):
        print(f"❌ File not found: {json_file}")
        return 0
    
    # Extract the actual data array
    data = extract_data_from_file(json_file)
    
    if not data:
        print(f"❌ No data found in {json_file}")
        return 0
    
    print(f"📊 Found {len(data)} records in {json_file}")
    
    # Add extraction timestamp to each record
    for record in data:
        if isinstance(record, dict):  # Make sure it's a dictionary
            record['extracted_at'] = datetime.now().isoformat()
    
    # Convert to DataFrame
    df = pd.json_normalize(data)
    
    # Configure job
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True,
        description=table_description
    )
    
    # Upload to BigQuery
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    
    print(f"✅ Uploaded {len(data)} rows to {table_id}")
    return len(data)

def main():
    print("🚀 Uploading sample data to bronze layer...\n")
    
    uploads = [
        {
            'file': 'data/raw/sample_data_all_sources.json',
            'table': 'madrid-newsletter.bronze.news_articles_raw',
            'description': 'Raw news articles from various Madrid sources'
        },
        {
            'file': 'data/raw/sample_data_cultural_events.json', 
            'table': 'madrid-newsletter.bronze.cultural_events_raw',
            'description': 'Raw cultural events data from Madrid'
        },
        {
            'file': 'data/raw/sample_data_general_events.json',
            'table': 'madrid-newsletter.bronze.general_events_raw', 
            'description': 'Raw general events data from Madrid'
        },
        {
            'file': 'data/raw/sample_data_newsdata.json',
            'table': 'madrid-newsletter.bronze.newsdata_raw',
            'description': 'Additional raw news data'
        }
    ]
    
    total_rows = 0
    successful_uploads = 0
    
    for upload in uploads:
        try:
            rows = upload_json_to_bigquery(
                upload['file'], 
                upload['table'], 
                upload['description']
            )
            if rows > 0:
                total_rows += rows
                successful_uploads += 1
        except Exception as e:
            print(f"❌ Error uploading {upload['file']}: {str(e)}")
    
    print(f"\n🎉 Summary:")
    print(f"   - Files uploaded: {successful_uploads}/{len(uploads)}")
    print(f"   - Total rows: {total_rows}")
    print(f"   - Bronze layer populated!")

if __name__ == "__main__":
    main()
