![AWS](https://img.shields.io/badge/AWS-Serverless-orange)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Lambda](https://img.shields.io/badge/AWS-Lambda-yellow)
![S3](https://img.shields.io/badge/Amazon-S3-red)
![SNS](https://img.shields.io/badge/AWS-SNS-green)
![EventBridge](https://img.shields.io/badge/AWS-EventBridge-purple)

# AutoJobTracker-AWS-Serverless
Serverless automated DevOps job tracking system using AWS Lambda, S3, SNS and EventBridge.

## 🚀 Deployment Guide

### 1️⃣ Create S3 Bucket
- Create an S3 bucket
- Create folder: job-data/

### 2️⃣ Create IAM Role
Attach policies:
- AmazonS3FullAccess
- AmazonSNSFullAccess
- AWSLambdaBasicExecutionRole

### 3️⃣ Create Lambda Function
- Runtime: Python 3.12
- Upload lambda_function.py
- Assign IAM role

### 4️⃣ Create SNS Topic
- Create topic
- Add email subscription
- Confirm subscription

### 5️⃣ Create EventBridge Rule
- Schedule expression: rate(6 hours)
- Target: Lambda function

## 🧠 Challenges & Solutions

- HTTP 403 Error → Solved using User-Agent header
- S3 AccessDenied → Fixed IAM role permissions
- SNS AuthorizationError → Added SNS publish policy
- Duplicate entries → Implemented URL deduplication logic

## 🎯 Skills Demonstrated

- Serverless Architecture
- AWS IAM Debugging
- Event-Driven Design
- REST API Integration
- Data Deduplication
- Cloud Automation
