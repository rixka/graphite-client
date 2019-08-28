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


# Notes

# Future Work
