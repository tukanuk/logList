#!/usr/bin/env python3


##TODO: use argparse to make arguments on weather you want it to be printed or not. 
import json
import requests
import csv

# Required API permissions
# Access problem and event feed, metrics, and topology 
# Access logs >> Read log content

# API docs
# GET all hosts >> https://www.dynatrace.com/support/help/shortlink/api-hosts-get-all
# GET logs >> https://www.dynatrace.com/support/help/shortlink/api-log-analytics-host-get-logs

# dynatrace variables
# not to be stored in script
api_token = "RZH_HX6BRDSpYF2thaLKG"
tennant = "https://kqw28951.dev.dynatracelabs.com"
environment_id = ""

# is the tennat Saas?
saas = True

# set the host endpoint
if saas:
    host_endpoint = tennant + "/api/v1/entity/infrastructure/hosts?includeDetails=false"
else:
    host_endpoint = tennant + "/e/" + environment_id + "/api/v1/entity/infrastructure/hosts?includeDetails=false"

# make the host request

payload = {'Api-token': api_token}
response = requests.get(host_endpoint, params=payload)

if response.status_code != 200:
    raise Exception('Error on GET /hosts/ code: {}'.format(response.status_code))

# collect the hosts

hosts = json.loads(response.text)
host_list = []
# host_list = hosts_response['']['entityId']

print('`\nHost Perspective')
print("=================")

# a list of hosts
host_list = [host['entityId'] for host in hosts]

# query the logs

with open('hosts.csv','w', newline='') as csvfile:
    linewriter = csv.writer(csvfile, delimiter=',')
    linewriter.writerow(["Host", "Path", "Size", "AvailableForAnalysis"])
    for host in host_list:
        log_endpoint = tennant + "/api/v1/entity/infrastructure/hosts/" + host + "/logs"
        response = requests.get(log_endpoint, params=payload)

        if response.status_code != 200:
            raise Exception('Error on GET /hosts/ code: {}'.format(response.status_code))

        log_info = json.loads(response.text)

        print("\n{}".format(host))
        
        for log in log_info['logs']: 
            linewriter.writerow([host, log['path'], log['size'], log['availableForAnalysis']]) #honestly not too sure if this works lol. I think it should, otherwise you put it into a list. 
            print("\t{:30} {:>9} Analysis: {}".format(log['path'], log['size'], log['availableForAnalysis']))

    # Try the same thing with process groups

    pg_endpoint = tennant + "/api/v1/entity/infrastructure/process-groups?includeDetails=false"

    response = requests.get(pg_endpoint, params=payload)

    if response.status_code != 200:
        raise Exception('Error on GET /process-groups/ code: {}'.format(response.status_code))

    # collect the pg

    process_groups = json.loads(response.text)
    process_groups_list = []
    # host_list = hosts_response['']['entityId']

with open('process_group_logs.csv', 'w', newline='') as csvfile1:
    linewriter = csv.writer(csvfile1, delimiter=',') 
    linewriter.writerow(["Process Group", "Path", "Size"])
    print('\nProcess Group Perspective')
    print('=========================')
   
    pg_list = {pg['entityId']: pg['displayName'] for pg in process_groups}

    for pg in pg_list:
        # print("\n\n\nTEST " + pg)
        # print(type(pg))
        log_endpoint = tennant + "/api/v1/entity/infrastructure/process-groups/" + pg + "/logs"
        response = requests.get(log_endpoint, params=payload)

        if response.status_code != 200:
            raise Exception('Error on GET /hosts/ code: {}'.format(response.status_code))

        log_info = json.loads(response.text)

        print("\n{}".format(pg_list[pg]))
        #ls = [i['path'] for log_info in log_info['logs'][i]]
        #print(ls)
        # print(log_info) 
        for log in log_info['logs']:
            linewriter.writerow([pg, log['path'], log['size']])
            print("\t{:110} {:>9}".format(log['path'], log['size']))