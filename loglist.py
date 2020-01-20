import json
import requests

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

print('\n')
# print(hosts)

for host in hosts:
    host_list.append(host['entityId'])

# a list of hosts
print(host_list)

# query the logs

for host in host_list:
    log_endpoint = tennant + "/api/v1/entity/infrastructure/hosts/" + host + "/logs"
    response = requests.get(log_endpoint, params=payload)

    if response.status_code != 200:
        raise Exception('Error on GET /hosts/ code: {}'.format(response.status_code))

    log_info = json.loads(response.text)

    print("\nHost: {}".format(host))
    print(log_info['logs'])

# Try the same thing with process groups

pg_endpoint = tennant + "/api/v1/entity/infrastructure/process-groups?includeDetails=false"

response = requests.get(pg_endpoint, params=payload)

if response.status_code != 200:
    raise Exception('Error on GET /process-groups/ code: {}'.format(response.status_code))

# collect the pg

process_groups = json.loads(response.text)
process_groups_list = []
# host_list = hosts_response['']['entityId']

print('\n')


# pg = "PROCESS_GROUP-C915B59DE278E602"
# pg_logs_endpoint = tennant + "/api/v1/entity/infrastructure/process-groups/{}/logs".format(pg)

