# Graphite Client

## Introduction
This is a python application which captures output data from a bpftrace script streaming to a specific log file and ships that data to a graphite service.

_Notes: This project assumes python-pip and virtualenv is installed._


### Requirements
We'd like to monitor the cpu latency distribution over a longer time-period and roll out this script to a number of other machines. Data must be captured and shipped in a suitable format to be stored by the graphite service.

Graphite listens for connections on TCP port 2003 and data is fed via a line-based ASCII protocol:
`<key>\s<value>\s<timestamp>\n`

Where the key is a dotted string and should take the form `<hostname>.cpu-lat.<bucket>`, value is a numeric value and the timestamp is a unix integer epoch value. The value for `<bucket>` should be the lower bound of each bucket. From the example output above the buckets would be 0, 1, 2, 4, 8, 16, ... etc.

The graphite instances expects a value for each key every 15 seconds.

### Quick testing

```shell
make venv
make test
```

All tests are run using pytest:
```shell
pytest --vvra tests
```

# How to

The graphite-client script tails a bpftrace log file for updates and ships the data to a graphite service.

Expected bpftrace data in log file:
```
@usecs: 
[1]                    1 |@@@@@                                               |
[2, 4)                 1 |@@@@@                                               |
[4, 8)                 2 |@@@@@@@@@@                                          |
[8, 16)                3 |@@@@@@@@@@@@@@@                                     |
[16, 32)              10 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
```

### Getting Started

This code has dependencies which will need to be installed alongside the script or tested using virtualenv.

To run manually either install the dependencies locally using `pip install -r requirements.txt -t .` or activate the virtual environment `source ./venv/bin/activate`. The script can be ran using the following command `python ./graphite_client.py` or `./graphite_client.py` and hit Ctrl-C to end.

The script supports the following arguments:

| Variable | Option       | Description                     | Default                |
|----------|--------------|---------------------------------|------------------------|
| File     | -f, --file   | File path of log file           | `/var/log/cpu-lat.log` |
| Metric   | -m, --metric | Graphite metric to generate key | 'cpu-lat'              |
| URI      | --uri        | Graphite URI                    | 'localhost'            |

**Example**
`./graphite_client.py -f /var/log/bpftrace.log -m bpftrace -h graphite.example.com`


# Notes
In order for this script to be effective, it requires to be running continuously in the background along with the bpftrace script. The graphite-client script expects the bpftrace to output data to a log somewhere to be consumed, captured, and shipped. I employed a loosley coupled approach to achieving the desired result, this will ensure that both scripts can run or break independently without interfering with the other. I recommend using a process contorl system like supervisord to ensure that both scripts aare continuously running in addition to configuring log rotate to clean up the logs - this will ensure that the script can run non-interactively.

I decided to tail the log and stream incomming data in "real-time" to the graphite server. Another option could be to batch 15 seconds worth of data and trigger the script via a cronjob but additional work would need to be completed to prevent duplicate data. 

While it may be over kill, I decided to start using a TDD approach and include a few tests in this package. If this script was a standalone piece of work the tests may not be neccessary, however, since the intention is to deploy this code on to a fleet of instances the risk of an incident is higher and therefore testing is preferred.

### Deployment

I recommend either deploying this code using a config management tool like puppet, ansible, or chef, or by baking the scripts into a golden AMI if an immutable approach is prefered.

**Configuration:**
By using a config management tool, the scripts can be copied over from the master service to a specified location which will trigger an update to all servers should the master script be modified or improved. The master server can also be configured to verify the scripts on the individual servers remain unmodified by overwriting them periodically. This is one of the easiest methods in ensuring that there is consistency across a fleet of services.

**Imutibility:**
For peace of mind, many companies strive for immutibility across all of there services and lock down access to prevent modification. This works particularly well with cloud computing and the conceept of treating servers like cattle rather then pets. Servers can be pre-configured using tools like packer and snapshots can be taken to create AMIs that will later be used for an unlimited number of services. One of the drawbacks of this method is that whenever anything on the AMI needs updated, a whole new AMI needs to be created regardless of how minor the changes may be.

# Future Work

* **Logging!!!!!**
* **Logging!!!!!**
* And more **logging**
* Performance review to speed up the script
* Testing integration with graphite server
* Integration testing, perhaps with a docker graphite server for local testing
* A deployment strategy and configuration
* Installation artifact to bundle the dependencies
* Documentation on how to configure a process control system and configure log rotate

