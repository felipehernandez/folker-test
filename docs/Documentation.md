# Folker

## Intro

## Build

```docker
# Dockerfile

FROM  folkertest/folkertest

COPY  ./  ./


```

> docker build -t IMAGE --pull .

## Execution

> docker run IMAGE [PARAMETERS]

The following table shows the parameters available and its usage.

| Parameter           | Description                                                                                    | Usage                                                 | Example                                                                                                                       |
| ------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| -c <br> --context   | Set predefined key:value in the **Test context**                                               | -c KEY VALUE <br> --context KEY VALUE                 | -c key1 value1 -c key2 value2 <br> --context key1 value1                                                                      |
| -d <br> --debug     | Run on Debug log mode                                                                          | -d <br> --debug                                       | -d <br> --debug                                                                                                               |
| --help              | Show list of available parameters                                                              | --help                                                | --help                                                                                                                        |
| -lf <br> --log-file | Specify a file where output the logs (console by default)                                      | -lf FILE <br> --log-file=FILE                         | -lf logs.log <br> --log-file=logs.log                                                                                         |
| --log-type          | Specify the logger type ({PLAIN, COLOR}) - default: COLOR                                      | --logger-type=TYPE                                    | --logger-type=plain                                                                                                           |
| -n                  | Specify the expected number of tests to be run                                                 | -n NUMBER                                             | -n 42                                                                                                                         |
| -p <br> --profile   | Specify a profile file to load test context data                                               | -p PROFILE[,PROFILE] <br> --profile=PROFILE[,PROFILE] | -p profile1 -p profile2 <br> -p profile1,profile2 <br> --profile=profile1,profile2 <br> --profile=profile1 --profile=profile2 |
| --trace             | Run on Trace log mode                                                                          | --trace                                               | --trace                                                                                                                       |
| -t <br> --tags      | Run tests that matches all specified tags                                                      | -t TAG[,TAG] <br> --tags=TAG[,TAG]                    | -t tag1 -t tag2 <br> -t tag1,tag2 <br> --tag=tag1,tag2 <br> --tag=tag1 --tag=tag2                                             |
| -tf, --test-file    | Execute all tests whose file name are listed. Use quotes ("") if neccesary                     | -tf FILE[,FILE] <br> --test-file=FILE                 | -tf test_test1.yaml <br> --test-file=test_1.yaml                                                                              |
| -TF, --TEST-FILES   | execute all tests whose file name matches the regular expression. Use quotes ("") if neccesary | -F FILE_RE <br> --FILE=FILE_RE                        | -TF f_t_test1.yaml <br> --TEST-FILES=f_t_*.yaml                                                                               |
