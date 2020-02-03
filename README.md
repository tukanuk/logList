# logList Readme

Uses the Dynatrace API to build a list of log files that are being monitored.

Outputs to `host_logs[datetime].csv` and `process_group_logs[datetime].csv`


## Usage

`usage: loglist.py [-h] [-q] [-m] [-g | -p] url token`

Get the process groups and host groups of a folder

```positional arguments:
  url                  tennant url with format
                       https://[tennant_key].live.dynatrace.com
  token                Your API Token generated with Access

optional arguments:
  -h, --help           show this help message and exit
  -q, --quiet          no output printed to terminal
  -g, --hosts          only gives host log information. If neither -g or -p is
                       specified, outputs both
  -p, --processgroups  only gives process group log info. If neither -g or -p
                       is specified, outputs both
```
