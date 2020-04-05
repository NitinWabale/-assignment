# -assignment


A python log parser to perform 3 functions 

1. List Unique IP addresses with frequency of their occurrences.
2. For a given IP address, list the top 10 API / URL endpoints hit by the IP address
3. For a given duration of X minutes, list top API /URL endpoint hit, and the related IP addresses.  Ex: From `17/May/2015:09:05:00` to `17/May/2015:09:15:00`


**USAGE**:

```parser.py [-h] -f FILE [-ip IP_ADDRESS] [-from FROM_TIME] [-to TO_TIME]

Input options

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The file for log analysis
  -ip IP_ADDRESS, --ip_address IP_ADDRESS
                        The IP address for top 10 endpoint hits
  -from FROM_TIME, --from_time FROM_TIME
                        Starting time for log analysis in the format
                        date/month/year:hour:minute:seconds example:-
                        17/May/2015:09:05:00
  -to TO_TIME, --to_time TO_TIME
                        Starting time for log analysis in the format
                        date/month/year:hour:minute:seconds example:-
                        17/May/2015:09:15:00
```

1) For listing Unique IP address with frequency
Example:
python parser.py  -f nginx_logs

2) For a given IP address, list the top 10 API / URL endpoints hit by the IP address
Example:
python parser.py -ip 74.63.142.188 -f apache_logs

3)  For a given duration of X minutes, list top API /URL endpoint hit, and the related IP addresses.
Example: 
python3 parser.py -f nginx_logs -from 17/May/2015:21:06:15 -to 18/May/2015:10:05:03


**IP is printed in blue and Frequency in yellow for clarity**

Thanks
