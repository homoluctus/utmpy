import sys
import json
import yaml
import struct
import argparse
from datetime import datetime
from collections import namedtuple
from ctypes import *
from enum import Enum

class UTMP(Structure):
    _fields_ = [("ut_type", c_short),
                ("ut_pid", c_int),
                ("ut_line", c_char*32),
                ("ut_id", c_char*4),
                ("ut_user", c_char*32),
                ("ut_host", c_char*256),
                ("e_termination", c_short),
                ("e_exit", c_short),
                ("ut_session", c_int32),
                ("tv_sec", c_int32),
                ("tv_usec", c_int32),
                ("ut_addr_v6", c_char*4),
                ("__unused", c_char*20),]

class UTMPStatus(Enum):
    empty       = 0
    run_level   = 1
    boot_time   = 2
    new_time    = 3
    old_time    = 4
    init        = 5
    login       = 6
    user        = 7
    dead        = 8
    accounting  = 9

class UtmpHandler:
    def __init__(self):
        self._data = {}

    def load(self, path):
        count = 1

        fd = open(path, 'rb')
        while True:
            utmp = UTMP()
            if fd.readinto(utmp) is None:
                break
            convertd_data = dict((field, getattr(utmp, field)) for field, _ in utmp._fields_)
            #convertd_data['ut_type'] = UTMPStatus(convertd_data['ut_type'])
            #convertd_data['tv_sec']  = str(datetime.fromtimestamp(convertd_data['tv_sec']))
            self._data[count] = convertd_data
            count += 1

        fd.close()
        return self._data

    def _normalize_data(self, raw_data, fmt='utf-8'):
        if isinstance(raw_data, bytes):
            return raw_data.rstrip(b'\0').decode(fmt)
        else:
            return raw_data

    def dump(self, data=None, dst="stdout", fmt="json", append=False):
        if data:
            self._data = data

        try:
            formatted_data = self.format_data(fmt)
        except ValueError as err:
            sys.exit(err)

        if dst == "stdout":
            print(formatted_data)
        else:
            try:
                write_file(formatted_data, dst, append)
            except Exception as err:
                sys.exit(err)
        
        return

    def format_data(self, fmt):
        """
        Supported format is json (default) and yaml
        """

        if fmt in ["yaml", "yml"]:
            formatted_data = yaml.dump(self._data, default_flow_style=False)
        elif fmt == "json":
            formatted_data = json.dumps(self._data, indent=4)
        else:
            raise ValueError("{}: Not supported the format".format(fmt))

        return formatted_data

def write_file(self, data, dst, append=False):
    if append:
        mode = "a"
    else:
        mode = "w"

    with open(dst, mode) as f:
        f.write(data)

def dump(src, **kwargs):
    utmp = UtmpHandler()
    utmp.load(src)
    return utmp.dump(**kwargs)

def get_args():
    parser = argparse.ArgumentParser(
            prog='utmpy',
            description='Parse utmp file and Dump',
        )
    parser.add_argument('src', metavar='FILE1', help='utmp file')
    parser.add_argument('-d', '--dst', metavar='FILE2', default="stdout", \
                        nargs='?', help='output file (dump stdout if not specified)')
    parser.add_argument('-f', '--format', choices=['json', 'yaml', 'yml'], \
                        default='json', nargs='?', help='supported format is yaml and json')                        
    parser.add_argument('-a', '--append', action='store_true', help='append data to the given file')

    return parser.parse_args()

def main():
    args = get_args()
    dump(src=args.src, dst=args.dst, fmt=args.format,append=args.append)

if __name__ == '__main__':
    #main()
    utmp_handler = UtmpHandler()
    utmp = utmp_handler.load("/root/app/tests/utmp1.log")
    print(utmp)
