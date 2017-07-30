#!/bin/python
# ------------------------------------------------------------------
# Author: Patrick Byrne
# Copywrite: Patrick Byrne (2017)
# License: Apache 2.0
# Title: check_freenas.py
# Description:
#      Nagios type plugin to check Freenas health status
#
# ------------------------------------------------------------------
#  Todo:
#   Add option for timeout with sane default
#   Add exception handling so the check returns unknown
#   Add option to specify check type
#   Add storage utilization check
#   Cleanup request method and remove post option
# ------------------------------------------------------------------

__version__ = "0.1.0"

# ------------------------------------------------------------------

import argparse
import json
import sys
import requests

class FreenasAPI(object):

    def __init__(self, hostname, user, secret):
        self._hostname = hostname
        self._user = user
        self._secret = secret
        self._url = 'http://%s/api/v1.0' % hostname

    def request(self, resource, method='GET', data=None):
        if data is None:
            data = ''
        r = requests.request(
            method,
            '%s/%s/' % (self._url, resource),
            data=json.dumps(data),
            headers={'Content-Type': "application/json"},
            auth=(self._user, self._secret),
            timeout=1,
        )
        if r.ok:
            try:
                return r.json()
            except:
                return r.text

        raise ValueError(r)

    def _get_volumes(self):
        # Function returns a list of volumes on device
        volumes = self.request('storage/volume')
        return [volume['name'] for volume in volumes]

    def check_disks(self):
        # Get a list of volumes on the device
        volumes = self._get_volumes()
        # Get the status of each volume
        for volume in volumes:
            volstatus = self.request('storage/volume/' + volume + '/status')
            # Unpack the nested status result
            for subvol in volstatus:
                vdevs = subvol['children']
                for vdev in vdevs:
                    disks = vdev['children']
                    for disk in disks:
                        # Check the disk status
                        if disk['status'] != 'ONLINE':
                            return (2, "Disk " + disk['name'] + " is offline", None)

        # If all the disks are online, return "OK"
        return (0, "All disks are online", None)

def output_results(*exitstatus):
    # Map our incomming variables
    for exitcode, message, perfdata in exitstatus:
        # If we get no perfdata, set an empty string
        if perfdata == None:
            perfdata = ""
        else:
            # Format perfdata to a comma seperated string and prepend a pipe
            perfdata = ','.join(str(elm) for elm in perfdata)
            perfdata = " | " + perfdata

        # Parse our exit code and return the proper result
        if exitcode == 0:
            print ("OK - " + message + perfdata)
            sys.exit(0)
        elif exitcode == 1:
            print ("WARNING - " + message + perfdata)
            sys.exit(1)
        elif exitcode == 2:
            print ("CRITICAL - " + message + perfdata)
            sys.exit(2)
        else:
            print ("UNKNOWN - " + message + perfdata)
            sys.exit(3)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--hostname', required=True, type=str)
    parser.add_argument('-u', '--user', required=True, type=str)
    parser.add_argument('-p', '--passwd', required=True, type=str)

    args = parser.parse_args(sys.argv[1:])

    startup = FreenasAPI(args.hostname, args.user, args.passwd)
    output_results(startup.check_disks())

if __name__ == '__main__':
    main()
