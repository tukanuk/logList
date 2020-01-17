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

hosts_response = json.loads(response.text)
# host_list = hosts_response['entityId']

print('\n')
print(hosts_response)