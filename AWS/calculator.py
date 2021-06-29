#!/usr/bin/env python3

# **************************************************
# AWS logs storage calculator
# Author: Roy Feintuch | Check Point SW Technologies
# See LICENSE and README files
# **************************************************

import boto3
import time
import statistics
from datetime import datetime, timedelta, date
import logging
import sys


def main():
    stats = []
    relevant_s3 = []
    relevant_trails = []
    ec2 = boto3.client('ec2')
#Comment to speed testing only
    all_regions = [x['RegionName'] for x in ec2.describe_regions()['Regions']]

#    all_regions = ["us-west-2"]

    for region in all_regions:
        print('\nRegion: %s\n---------------------------' % region)
        vpcs = list_vpcs(region)
        print('VPCs: %s' % vpcs)
        all_flows_in_region = list_flow_logs(region)
        relevant_flows = list(filter(lambda x: x['FlowLogStatus']=='ACTIVE' and x['TrafficType']=='ALL' and x['ResourceId'] in vpcs, all_flows_in_region))
        #print('RELEVANT FLOWS:%s' % relevant_flows)
        flows_cwl = [fl for fl in relevant_flows if fl['LogDestinationType']=='cloud-watch-logs']
        flows_s3 = [fl for fl in relevant_flows if fl['LogDestinationType']=='s3']

        vpcs_with_cwl = list(set([fl['ResourceId'] for fl in flows_cwl ])) # project and dedup
        print('VPCs with FL (CWL): %s' % vpcs_with_cwl)
        vpcs_with_s3 = [fl['ResourceId'] for fl in flows_s3 ]
        print('VPCs with FL (S3): %s' % vpcs_with_s3)
        vpcs_with_s3 = list(set(vpcs_with_s3) - set(vpcs_with_cwl)) #do not include in s3 if already in CWL as this test is more accurate

        #Do better here to find Bucket names and prefixes

        relevant_s3.extend([ x['LogDestination'][len('arn:aws:s3:::'):] for x in flows_s3 ])
        vpcs_without = list(set(vpcs) - set(vpcs_with_cwl) - set (vpcs_with_s3))
        print('VPCs without FlowLogs: %s' % vpcs_without )

        # Analyzing Logs
        relevant_CWL_groups = list(set([ fl['LogGroupName'] for fl in flows_cwl])) # project and dedup
        print("Relevant CW Log Groups: %s" % relevant_CWL_groups)

        for log_group in relevant_CWL_groups:
            count = query_cwl_group_ev_per_day(region, log_group)
            sizeGB = count * 110 / 1024 ** 3 # vpfl event size ~ 110 bytes
            stats.append(('CWL','(%s) %s' % (region,log_group),count,sizeGB) )

        # Analyzing CloudTrails per account per region(which are only ever stored in S3 buckets)

        # get the S3 buckets used by all cloud Trails in the account
        cloudTrailS3 = list_cloudTrails()

        print('Relevant CloudTrail S3 Buckets  %s' % cloudTrailS3)

        #add the CloudTrail Buckets to VPC Log Buckets
        relevant_trails.extend(cloudTrailS3)

    # Analyzing S3 Flow Log buckets - no need to do it per region as s3 is a global service
    COMPRESSION_RATIO = 8
    relevant_s3 = list(set(relevant_s3)) # dedup s3 list

    print('\nRelevant S3 buckets: %s' % relevant_s3)
    for s3 in relevant_s3:
        size = query_vpcfl_daily_size_s3(s3, "flow")
        stats.append(('S3',s3,'NA',size* COMPRESSION_RATIO / 1024 /1024/1024))

    # Analyzing S3 CloudTrail buckets - no need to do it per region as s3 is a global service
    relevant_trails = list(set(relevant_trails)) # dedup trails list

    print('\nRelevant CloudTrail S3 buckets: %s' % relevant_trails)
    for trail in relevant_trails:
        size = query_vpcfl_daily_size_s3(trail, "trail")
        stats.append(('Trail',trail,'NA',size* COMPRESSION_RATIO / 1024 /1024/1024))





    print('\n---------------------------- Final Report -------------------------------\n')
    headers=('Type','Destination','Ev/day','GB/day')
    frmt = '%s\t%-40s\t%-10s\t%s'
    print(frmt % headers)
    agg = 0
    for stat in stats:
        print(frmt % stat)
        agg += stat[3]

    print('\nTotal: %.2f GB/day' % agg)
    print('Total: %.2f GB/month' % (agg * 30))
    




# AWS Functions 
# ---------------------
def list_vpcs(region):
    client = boto3.client('ec2', region_name = region)
    response = client.describe_vpcs()
    # TODO: handle paged results
    return [vpc['VpcId'] for vpc in response['Vpcs']]

def list_flow_logs(region):
    client = boto3.client('ec2', region_name=region)
    response = client.describe_flow_logs()
    # TODO: handle paged results
    return response['FlowLogs']

def query_cwl_group_ev_per_day(region,log_group):
    print("Querying CloudWatch Log Group: %s" % log_group, end=' ', flush=True)
    try:
        client = boto3.client('logs', region_name=region)
        now = int(time.time())
        query = 'stats count() by bin(24h)'
        response = client.start_query(
            logGroupName=log_group,
            startTime=now - 5 * 24 * 3600,
            endTime=now,
            queryString=query
        )
        queryId = response['queryId']
        # now we wait until query result is ready
        status = 'Running'
        while True:
            response = client.get_query_results(queryId=queryId)
            status = response['status']
            if status == "Running":
                print('.', end='', flush=True)
                time.sleep(5)
            else:
                break

        # TODO: handle query error
        # TODO: do not iterate forever. Limit number of iterations / time

        # now we have result. values are a *list* of : [{u'field': u'bin(24h)', u'value': u'2019-05-22 00:00:00.000'}, {u'field': u'count()', u'value': u'4411'}]
        results = [int(res[1]['value']) for res in response['results']]
        results = results[1:-1] # first and last items might be partial
        avg = int(statistics.mean(results))
        print('\tGot results: %s Average: %s events/day' % (results,avg ))
    except Exception as e:
        print("Error.", str(e))
        return 0
    return avg

def query_vpcfl_daily_size_s3(bucket, trailorflow):
    d = datetime.today() - timedelta(days=1) # today might be partial, we'll take a look at yesterday to have a full day

    #handle VPC flow logs stored in folders within an root S3 bucket

    #split the bucket name at the first / only
    bucket_name = bucket.split("/", 1)

    #Handle optional prefix names and retain any additional prefixes (folders)
    if bucket_name[1] == "":
        prefix = "AWSLogs/"
    else:
        prefix = bucket_name[1] + "/AWSLogs/"
    print ("Bucket Name: " + bucket_name[0])
    print ("Prefix: " + prefix)
    accounts =  get_folders_in_s3(bucket_name[0],prefix)

    #print(accounts)
    work_list = []
    regions = []
    for acc in accounts:
        if trailorflow == "trail":
            regions = get_folders_in_s3(bucket_name[0],acc + "CloudTrail/")
        elif trailorflow == "flow":
            regions = get_folders_in_s3(bucket_name[0],acc + 'vpcflowlogs/')

        for region in regions:
            work_list.append('%s%s/%s/%s/' % (region,d.year,"{:02d}".format(d.month),"{:02d}".format(d.day)) )

    total_bytes = 0
    print('Analysing S3 bucket %s, discovered %i relevant subfolders' % (bucket_name[0], len(work_list)))
    for item in work_list:
        bucket_size = get_s3_folder_size(bucket_name[0],item)
        total_bytes += bucket_size
        print(' - %s/%s \tsize:%s ' % (bucket_name[0],item,bucket_size))

    print('Total %i bytes (compressed)' % total_bytes)
    return total_bytes

def get_s3_folder_size(bucket, prefix):
    #print('get_s3_folder_size', bucket,prefix)
    total_size = 0
    for obj in boto3.resource('s3').Bucket(bucket).objects.filter(Prefix=prefix):
        total_size += obj.size
    return total_size

def get_folders_in_s3(bucket,prefix):
    #print ("get_folder_in_s3", bucket, prefix)
    res = []
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects')

    try:
        for result in paginator.paginate(Bucket=bucket,Prefix=prefix, Delimiter='/'):
            for prefix in result.get('CommonPrefixes'):
                res.append(prefix.get('Prefix'))

    except Exception as e:
        logging.error('Exception: %s' % e, exc_info=True)
#        logger.info("Problem Reading the Bucket name or Prefix! for: " + bucket + prefix)
        print("Error.", str(e))




    return res

def list_cloudTrails():
    # return a list of all trail names in the account
    client = boto3.client('cloudtrail')
    response = client.list_trails()
    # TODO: handle paged results


    trails = [trail["TrailARN"] for trail in response["Trails"]]

    s3 = []

    response = client.describe_trails(trailNameList=trails, includeShadowTrails = True)

    for trail in response["trailList"]:
        bucket_name = trail["S3BucketName"]
        bucket_prefix = ""

        try:
            bucket_prefix = trail("S3KeyPrefix")
        except Exception as e:
            logging.error('Exception: %s' % e, exc_info=True)
#            logger.info("Problem Reading the Bucket name or Prefix! for: " + bucket + prefix)

        s3.append(bucket_name + "/" + bucket_prefix)
        print ("CloudTrail Bucket: " + bucket_name)

    return s3


if __name__ == "__main__":
    import os
    profile = os.environ['AWS_PROFILE'] if 'AWS_PROFILE' in os.environ else '-NA-'
    print("Starting script. AWS_PROFILE env variable: ", profile)
    main()