""" Python program to parse
    logs from nginx and apache files
    Author: Shivankar
"""

import argparse
from datetime import datetime
import time
from collections import Counter


def valid_date(s):
    """ Function to validate to and from parameters """
    try:
        time_stmp = datetime.strptime(s, '%d/%B/%Y:%H:%M:%S')
        time_stmp = time.mktime(time_stmp.timetuple())
        return time_stmp
    except:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def get_uniq_ips(file):
    """ Unique IP addresses with frequency of their occurrences """
    print('\033[1;32;48m' + "List of Unique IP addresses along with their frequency\n" + '\033[1;37;0m')
    uniq_ip = {}
    with open(file) as file_pointer:
        for line in file_pointer.readlines():
            ip = line.split(' ')[0]
            try:
                uniq_ip[ip] += 1
            except KeyError:
                uniq_ip[ip] = 1
    for ip, freq in uniq_ip.items():
        print('\033[1;34;48m' + ip + '\033[1;37;0m' + " - " '\033[1;33;48m' + str(freq) + '\033[1;37;0m')


def get_endpoints_ip_based(file, ip):
    """  Top 10 API / URL endpoints hit by the IP address """
    endpoint = {}
    with open(file) as file_pointer:
        for line in file_pointer.readlines():
            if line.split(' ')[0] == ip:
                url = (line.split('"')[1])
                try:
                    endpoint[url] += 1
                except KeyError:
                    endpoint[url] = 1
    if not bool(endpoint):
        print('\033[1;31;48m'+ "%s IP is not found in the logs" %ip + '\033[1;37;0m')
        exit(0)
    print('\033[1;32;48m' + "Top 10 API / URL endpoints hit by the IP address\n" + '\033[1;37;0m')
    endpoint = Counter(endpoint)
    highest = endpoint.most_common(10)
    for i in highest:
        api = i[0]
        freq = i[1]
        print('\033[1;34;48m' + ip + '\033[1;37;0m' + ' --- ' + api + ' --- ' + '\033[1;33;48m' + str(freq) + '\033[1;37;0m')

def get_endpoints_time_based(file, start, end):
    """ For a given duration, get top API /URL
        endpoint hit with the related IP addresses """
    if start > end:
        print('\033[1;31;48m' + "Please enter the start time smaller than end time" + '\033[1;37;0m')
        exit(0)

    """ Finding first timestamp and last timestamp from the file """
    with open(file) as file_pointer:
        first_line = file_pointer.readline()
        date_string = first_line.split(' ')[3]
        file_start_time_stamp = datetime.strptime(date_string, '[%d/%b/%Y:%H:%M:%S')
        file_start_time_stamp = time.mktime(file_start_time_stamp.timetuple())
        for last_line in file_pointer:
            pass
        date_string = last_line.split(' ')[3]
        file_end_time_stamp = datetime.strptime(date_string, '[%d/%b/%Y:%H:%M:%S')
        file_end_time_stamp = time.mktime(file_end_time_stamp.timetuple())

    """ Comparing start time with last time_stamp and
        end time with first time_stamp """
    if start - file_end_time_stamp >= 60:
        #Last line is not lastest time_stamp, there is difference of 60

        print('\033[1;31;48m' + "The start time entered is greater than finish time in the log file\
                \nPlease enter start time lesser than finish time\
                \nAnalysis Aborting" + '\033[1;37;0m')
        exit(0)
    if file_start_time_stamp - end >= 60:
        #First line is not newest time_stamp, there is difference of 60

        print('\033[1;31;48m' + "The end time entered is lesser than the start time in the log file\
                \nPlease enter end time more than start time\
                \nAnalysis Aborting" + '\033[1;37;0m')
        exit(0)

    with open(file) as file_pointer:
        api_endpoint = {}
        for line in file_pointer.readlines():
            line_time_stamp = line.split(' ')[3]
            line_time_stamp = datetime.strptime(line_time_stamp, '[%d/%b/%Y:%H:%M:%S')
            line_time_stamp = time.mktime(line_time_stamp.timetuple())
            if line_time_stamp >= start and line_time_stamp <= end:
                api = line.split('"')[1]
                ip = line.split(' ')[0]
                api_endpoint.setdefault(api, [])
                api_endpoint[api].append(ip)
        sorted_endpoints = sorted(api_endpoint, key=lambda key: len(api_endpoint[key]))
        sorted_endpoints = sorted_endpoints[::-1]
        print('\033[1;32;48m' + "Top 10 most hit endpoints along with their associated IP's are\n\n" + '\033[1;37;0m')
        for counter in range(0, min(10, len(sorted_endpoints))):
            api = sorted_endpoints[counter]
            print(api + ":- HIT count " + '\033[1;33;48m' + str(len(api_endpoint[api])) + '\033[1;37;0m')
            print("Associated IP list")
            print('\033[1;34;48m')
            print(set(api_endpoint[api]))
            print('\033[1;37;0m')
            print("\n\n")



def main():
    """ main function """
    parser = argparse.ArgumentParser(description='Input options')
    parser.add_argument('-f', '--file', required=True, help='The file for log analysis')
    parser.add_argument('-ip', '--ip_address', required=False,
                        help='The IP address for top 10 endpoint hits')
    parser.add_argument('-from', '--from_time', type=valid_date,
                        help='Starting time for log analysis in the format\
                        date/month/year:hour:minute:seconds example:- 17/May/2015:09:05:00')
    parser.add_argument('-to', '--to_time', type=valid_date,
                        help='Starting time for log analysis in the format\
                        date/month/year:hour:minute:seconds example:- 17/May/2015:09:15:00')
    args = parser.parse_args()
    if (args.ip_address is None) and (args.from_time is None) and (args.to_time is None):
        get_uniq_ips(args.file)
    if (args.from_time is None) and (args.to_time is None) and (args.ip_address is not None):
        get_endpoints_ip_based(args.file, args.ip_address)
    if (args.from_time is not None) and (args.to_time is not None):
        get_endpoints_time_based(args.file, args.from_time, args.to_time)


if __name__ == '__main__':
    main()
