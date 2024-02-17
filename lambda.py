import concurrent.futures
import json

from tools.scraper import Scraper
from constants import comp_code_dict, bucket_name
from assemble import calculate_stats, s3


def lambda_handler(event, context):
    queryStrings = event["queryStringParameters"]
    league = queryStrings['league']
    season = queryStrings['season']
    comp_code =  comp_code_dict[league]
    
    json_response = None

    try:
        response = s3.get_object(Bucket=bucket_name, Key=f'{season}/{league}.json')
    
    except Exception as e:
        print('No such data on S3. Webscraping starting.......')
        scraper = Scraper(comp_code, league, season)
        club_names = scraper.get_fixtures()
        data = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            results = executor.map(calculate_stats, club_names)

            for club, pts in results:
                data.update({club:pts})
        
        json_response =  json.dumps(data)
        s3.put_object(Bucket=bucket_name, Key=f'{season}/{league}.json', Body=json_response)
    
    else:
        print('data already present on s3')
        data = response['Body'].read().decode('utf-8')
        json_response = data
    
    finally:
        return json_response