#!/usr/bin/env python3



import json
import requests
import csv
import argparse
import time
from shutil import copyfile

# Required API permissions
# Access problem and event feed, metrics, and topology 
# Access logs >> Read log content

# API docs
# GET all hosts >> https://www.dynatrace.com/support/help/shortlink/api-hosts-get-all
# GET logs >> https://www.dynatrace.com/support/help/shortlink/api-log-analytics-host-get-logs

def main():
    parser = argparse.ArgumentParser(description="Get the process groups and host groups of a folder")

    
    parser.add_argument("url", 
                        help="tennant url with Saas: format https://[tennant_key].live.dynatrace.com OR Managed: https://{your-domain}/e/{your-environment-id")
    parser.add_argument("token", type=str,
                        help="Your API Token generated with Access",)
    parser.add_argument("-q", "--quiet",
                        help="no output printed to terminal",
                        action="store_true")
    parser.add_argument("-m", "--managed",
                        help="is the tenant managed?(not saas)",
                        action="store_true")
    # parser.add

    ## A mutually exclusive group so you can only ask for pgs or hosts, otherwise without you get none.
    group = parser.add_mutually_exclusive_group()
    #can't use -h because that's help
    group.add_argument("-g", "--hosts",
                        help="only gives host log information. If neither -g or -p is specified, outputs both",
                        action="store_true")
    group.add_argument("-p", "--processgroups", 
                        help="only gives process group log info. If neither -g or -p is specified, outputs both",
                        action="store_true")
    
    args = parser.parse_args()

    # dynatrace variables
    # not to be stored in script
    
    tennant = args.url

    api_token = args.token

    environment_id = ""
    
    #The time string #YEARMONTHDAY-Hours-Minutes-Seconds
    #making it at the start, so both files have same timestamp for sure. 
    timestr = time.strftime("%Y%m%d_%H%M%S")


    
    payload = {'Api-token': api_token}

    if args.hosts:
        get_host_logs(tennant=args.url, saas=not args.managed, quiet=args.quiet, payload=payload, timestr=timestr, environment_id=environment_id)
    elif args.processgroups:
        get_process_group_logs(tennant=args.url, quiet=args.quiet,timestr=timestr, payload=payload)
    else:
        get_host_logs(tennant=args.url, saas=not args.managed, quiet=args.quiet, payload=payload,timestr=timestr, environment_id=environment_id)
        get_process_group_logs(tennant=args.url, quiet=args.quiet,timestr=timestr, payload=payload)
    

def get_hosts(tennant, quiet, payload, timestr, environment_id=""):
    host_endpoint = tennant + "/api/v1/entity/infrastructure/hosts?includeDetails=false"

    # make the host request

    response = requests.get(host_endpoint, params=payload)

    if response.status_code != 200:
        raise Exception('Error on GET /hosts/ code: {}'.format(response.status_code))

    # collect the hosts

    hosts = json.loads(response.text)

    return hosts

def get_host_logs(tennant, saas, quiet, payload, timestr, environment_id=""):

# is the tennat `Saas?
# set the host endpoint
    if saas:
        host_endpoint = tennant + "/api/v1/entity/infrastructure/hosts?includeDetails=false"
    else:
        host_endpoint = tennant + "/e/" + environment_id + "/api/v1/entity/infrastructure/hosts?includeDetails=false"

    # make the host request

    response = requests.get(host_endpoint, params=payload)

    if response.status_code != 200:
        raise Exception('Error on GET /hosts/ code: {}'.format(response.status_code))


    # collect the hosts

    hosts = json.loads(response.text)
    host_list = []
    # host_list = hosts_response['']['entityId']
    if not quiet:

        print('`\nHost Perspective')
        print("=================")

    # a list of hosts
    # host_list = [host['entityId'] for host in hosts]
    host_list = {host['entityId']: host['displayName'] for host in hosts}
    #   pg_list = {pg['entityId']: pg['displayName'] for pg in process_groups}
    # query the logs
    f_name = "host_logs_" + timestr + ".csv"
    with open(f_name,'w', newline='') as csvfile:
        linewriter = csv.writer(csvfile, delimiter=',')
        linewriter.writerow([tennant])
        linewriter.writerow(["Host", "Entity Id", "Path", "Size", "AvailableForAnalysis"])
        for host in host_list:
            log_endpoint = tennant + "/api/v1/entity/infrastructure/hosts/" + host + "/logs"
            # time.sleep(0.5) # slow the script to keep under API limit
            response = requests.get(log_endpoint, params=payload)

            if response.status_code != 200:
                raise Exception('Error on GET /hosts/ code: {}'.format(response.status_code))

            log_info = json.loads(response.text)

            if not quiet:
                print("\n{}".format(host))
            
            for log in log_info['logs']: 
                if log['availableForAnalysis'] == True:
                    linewriter.writerow([host_list[host], host, log['path'], log['size'], log['availableForAnalysis']])
                    if not quiet:
                        print("\t{:30} {:>9} Analysis: {}".format(log['path'], log['size'], log['availableForAnalysis']))

    print(f_name, " Created")
    copyfile(f_name, "host_logs.csv")


# Try the same thing with process groups


def get_process_group_logs(tennant, quiet, payload,timestr):


    hosts = get_hosts(tennant, quiet, payload, timestr, environment_id="")
    host_list_label = {host['entityId']: host['displayName'] for host in hosts}
    
    # for entity, display in host_list_label.items():
    #     print(entity + ": " + display)

    pg_endpoint = tennant + "/api/v1/entity/infrastructure/process-groups?includeDetails=false"

    response = requests.get(pg_endpoint, params=payload)

    if response.status_code != 200:
        raise Exception('Error on GET /process-groups/ code: {}'.format(response.status_code))

    # collect the pg

    process_groups = json.loads(response.text)
    process_groups_list = []
    # host_list = hosts_response['']['entityId']

    f_name = "process_group_logs_" + timestr + ".csv"
    with open(f_name, 'w', newline='') as csvfile1:
        linewriter = csv.writer(csvfile1, delimiter=',') 
        linewriter.writerow([tennant])
        linewriter.writerow(["Process Group", "Entity ID", "Path", "Size", "Host", "Host Entity ID", "Analysis"])

        if not quiet:
            print('\nProcess Group Perspective')
            print('=========================')
    
        pg_list = {pg['entityId']: pg['displayName'] for pg in process_groups}

        for pg in pg_list:
            # print("\n\n\nTEST " + pg)
            # print(type(pg))
            log_endpoint = tennant + "/api/v1/entity/infrastructure/process-groups/" + pg + "/logs"
            # time.sleep(0.5) # slow the script to keep under API limit
            response = requests.get(log_endpoint, params=payload)

            if response.status_code != 200:
                raise Exception('Error on GET /hosts/ code: {}'.format(response.status_code))

            log_info = json.loads(response.text)

            if not quiet:
                print("\n{}".format(pg_list[pg]))
            #ls = [i['path'] for log_info in log_info['logs'][i]]
            #print(ls)
            # print(log_info) 
            for log in log_info['logs']:
                host_list = log['hosts']
                for host in host_list:
                    if host['hostId'] in host_list_label:
                        displayName = host_list_label[host['hostId']]
                    else:
                        displayName = "Unknown"
                    if host['availableForAnalysis'] == True:
                        linewriter.writerow([pg_list[pg], pg, log['path'], host['logSize'], displayName, host['hostId'], host['availableForAnalysis']])
                    if not quiet:
                        print("\t{:<132} {:>9} {:>25} {:5}".format(log['path'], host['logSize'], host['hostId'], host['availableForAnalysis']))

    print(f_name," created")
    copyfile(f_name, "process_group_logs.csv")

if __name__ == "__main__":
    main()