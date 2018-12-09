# check_freenas
[![GitHub issues](https://img.shields.io/github/issues/patricknbyrne/check_freenas.svg)](https://github.com/PatrickNByrne/check_freenas/issues)
[![license](https://img.shields.io/github/license/patricknbyrne/check_freenas.svg)](https://github.com/PatrickNByrne/check_freenas/blob/master/LICENSE)

##### A Nagios type plugin to query the Freenas API for volume and disk status

## Requirements

* Python 2.6+
* Python Requests

## Installation

* Copy the check_freenas.py file to your Nagios plugins directory.
* Create a check command to reference the plugin. 
* Create a service check on your Freenas host using the new check command. 

#### Nagios Example

```
# 'check_freenas-disks' command definition
define command{
	command_name	check_freenas-disks
	command_line	$USER1$/check_freenas.py -H $HOSTADDRESS$ -c disks -u root -p $ARG1$
	}

# 'check_freenas-volumes' command definition
define command{
	command_name	check_freenas-volumes
	command_line	$USER1$/check_freenas.py -H $HOSTADDRESS$ -c volumes -u root -p $ARG1$
	}
```

## Usage

```
check_freenas.py  [-h] 
                  -H HOSTNAME 
                  -u USER 
                  -p PASSWD 
                  [-t TIMEOUT] 
                  [-v]
                  [-i] 
                  -c {disks,volumes,alerts}
```

#### Notes

* Due to a lack of authentication methods in the Freenas V1.0 API you must use your root user to authenticate.

## History

* V1.0 - Initial production release
* V1.2 - Add verbose and ignore SSL options. Add additional handling for SSL Errors.

## License

* Apache 2.0

