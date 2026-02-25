import json
import urllib.request
import boto3
from datetime import datetime

# AWS Clients
s3 = boto3.client('s3')
sns = boto3.client('sns')

# Configuration
BUCKET_NAME = "parashurama-autojobtracker"
FILE_NAME = "job-data/jobs_data.csv"
SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:954096903603:AutoJobTrackerNotification"


def lambda_handler(event, context):

    print("🚀 AutoJobTracker execution started")

    try:
        # ----------------------------
        # STEP 1: Fetch Jobs from API
        # ----------------------------
        url = "https://arbeitnow.com/api/job-board-api"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())

        jobs = data.get('data', [])[:10]
        print(f"Fetched {len(jobs)} jobs from API")

        # -----------------------------------
        # STEP 2: Read Existing S3 CSV (if exists)
        # -----------------------------------
        existing_urls = set()
        existing_content = ""

        try:
            s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
            existing_content = s3_object['Body'].read().decode('utf-8')

            lines = existing_content.split("\n")[1:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split(",")
                    if len(parts) >= 4:
                        existing_urls.add(parts[3])

            print(f"Loaded {len(existing_urls)} existing job URLs")

        except s3.exceptions.NoSuchKey:
            print("No existing file found. Creating new file.")
            existing_content = "Date,Company,Title,URL\n"

        # -----------------------------------
        # STEP 3: Append Only New Jobs
        # -----------------------------------
        new_jobs_count = 0
        updated_content = existing_content

        for job in jobs:
            job_url = job.get('url', 'N/A')

            if job_url not in existing_urls:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                company = job.get('company_name', 'N/A')
                title = job.get('title', 'N/A')

                updated_content += f"{date},{company},{title},{job_url}\n"
                new_jobs_count += 1

        print(f"New jobs added: {new_jobs_count}")

        # -----------------------------------
        # STEP 4: Upload Updated CSV to S3
        # -----------------------------------
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=FILE_NAME,
            Body=updated_content
        )

        print("S3 file updated successfully")

        # -----------------------------------
        # STEP 5: Send Notification If New Jobs Found
        # -----------------------------------
        if new_jobs_count > 0:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="🚀 New DevOps Jobs Added",
                Message=f"{new_jobs_count} new DevOps jobs were added to your tracker."
            )
            print("SNS notification sent")
        else:
            print("No new jobs found. No notification sent.")

        return {
            "statusCode": 200,
            "body": f"{new_jobs_count} new jobs added successfully."
        }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": str(e)
        }
