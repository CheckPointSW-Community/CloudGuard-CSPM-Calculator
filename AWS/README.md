# AWS Logs calculator (WIP)
This little tool helps to estimate the amount of AWS logs your AWS account is generating.
Currently it supports:
- VPC Flow Logs (via CloudWatch Logs or S3)
- CloudTrail 

It tries to guestimate the VPCFL traffic using 2 heuristics:
1. Calculate it from CloudWatch & CloudTrail Logs (using the new CWL Insights query lang) - OR-
2. Estimate it from (zipped) S3 daily sample (using an 8X COMPRESSION_RATIO constant)

## Pre-requisites
### Python3
The tool is written in python3 and requires a working python3 environment. To verify:
```
python3 --version
```
If your default python installation is python3 then you can replace `python3` with just `python`

### AWS Credentials
The tool assumes that a working AWS cli / profile was already set. If in doubt - please consult boto guide : https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html <br/>
Your AWS user / role should have some readonly permissions to perfrom a few EC2 describe operations, CloudWatchLogs Insight queries, and to read relevant S3 buckets. This is the list of IAM permissions that is required. It can be added to the relevant user / role as an independant policy.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "storagecalculator",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVpcs",
                "ec2:DescribeRegions",
                "ec2:DescribeFlowLogs",
                "s3:ListBucket",
                "s3:GetObject",
                "logs:StartQuery",
                "logs:GetQueryResults"
            ],
            "Resource": "*"
        }
    ]
}
```



## Using the tool
the tool assumes the standard AWS (boto) SDK setup. All authentication setup should be done externally using environment variables.
If you wish to use the *default* AWS profile (or your AWS instance's role):
```
python3 calculator.py
```

If you wish to use a different profile, use the relevant environment variable as follows:
```bash
export AWS_PROFILE=<MY PROFILE_NAME> && python3 calculator.py
```
Similarly, it is possible to set the `AWS_ACCESS_KEY_ID` (and `AWS_SECRET_ACCESS_KEY`) variables, but it is left out of this readme.

## Results
Pretty self explanatory. The scripts enumerates relevant CWL groups and relevant S3 buckets and estimates the daily/monthy data volume (non compressed).

### Credit
This project originated on the Dome9 github by froyke.
