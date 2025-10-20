import requests
from datetime import datetime
import boto3
import json
import sys

def lambda_api_extractor():
    """
    Fetch transaction data from public API
    """

    # s3 = boto3.client('s3')

    urls = [ 
        'https://fakestoreapi.com/products',
        'https://fakestoreapi.com/users',
        'https://fakestoreapi.com/carts'
    ]


    for url in urls:
        response = requests.get(url)
        data = response.json()
        

        # Add metadata
        for record in data:
            dateTimeNow = datetime.now()
            record['ingestion_timestamp'] = dateTimeNow.isoformat()
            source = url.split('/')[-1].strip()
            record['source'] = source


        # # Store in S3
        # date_partition = dateTimeNow.strftime('%Y/%M/%d')
        # file_key = f"raw/{source}/{date_partition}/data_{dateTimeNow.strftime('%H%M%S')}.json"

        # s3.put_object(
        #     Bucket='etl-pipeline-raw',
        #     Key=file_key,
        #     Body=json.dumps(data)
        # )


        # Save results to local JSON file
        with open(
            'fakeStore' + source + 'APIData.json', "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    print(f"Scraping completed")

if __name__ == "__main__":
    lambda_api_extractor()
