# check_rq

> Icinga/Nagios check for RQ (Redis Queue)

## Usage

```
usage: check_rq/check_rq.py [-h] [--queue QUEUE] [--host HOST] [--port PORT] [--password PASSWORD]
                            -w WARNING -c CRITICAL [-v]

Nagios/icinga plugin for checking a RQ redis queues

optional arguments:
  -h, --help            show this help message and exit
  --queue QUEUE         RQ Queue
  --host HOST           Redis host
  --port PORT           Redis port
  --password PASSWORD   Redis password
  -w WARNING, --warn WARNING
                        WARNING trigger
  -c CRITICAL, --critical CRITICAL
                        CRITICAL triger
  -v, --version         Print version
```

## License

Released under the [MIT license](https://github.com/crafterwerkbon/check_rq/blob/main/LICENSE).
