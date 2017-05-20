#!/usr/bin/env python

# Simple utility to automatically create a memo template from the command line
# autofills some of the entries, or get them from the command line
#
# Author: Maxime Gariel

import argparse
import datetime
import dateparser
import os
import pystache
import subprocess


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y/%m/%d") or datetime.datetime.strptime(s, "%Y-%m-%d") 
    except ValueError:
        msg = "Not a valid date: '{0} - valid date is YYYY-MM-DD or YYYY/MM/DD'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def valid_time(s):
    try:
        return datetime.datetime.strptime(s, "%H:%M") or datetime.datetime.strptime(s, "%H-%M") 
    except ValueError:
        msg = "Not a valid date: '{0} - valid date is YYYY-MM-DD or YYYY/MM/DD'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def main():

    parser = argparse.ArgumentParser(
        description="Utility to take memos. ")

    parser.add_argument('-n', '--name', required=True, default=None, dest='meeting_name', 
                        help='Name of the meeting will be used as file name')
    parser.add_argument('-d', '--date', required=False, default=None, dest='meeting_date', type=valid_date, 
                        help='Date of the meeting (YYYY-MM-DD or YYYY/MM/DD) - Default: today\'s date')
    parser.add_argument('-t', '--time', required=False, default=None, dest='meeting_time', type=valid_time, 
                        help='Time of the meeting (H-M or H:M) - Default: now')
    parser.add_argument('-type', '--type', required=False, default='',
                        help='Type of the meeting - Default: blank')
    parser.add_argument('-l', '--location', required=False, default='',
                        help='Location of the meeting - Default: blank')
    parser.add_argument('-a', '--attendance', required=False, default='',
                        help='Attendance - Default: blank')


    args = parser.parse_args()
    if args.meeting_date is None:
        args.meeting_date = datetime.date.today()

    if args.meeting_time is None:
        args.meeting_time = datetime.datetime.now()

    create_memo(args)

def create_memo(args):
    
    if args.meeting_date is None:
        meeting_date =  0
    else:
        meeting_date =  0
    dic={
    'meeting_name': args.meeting_name,
    'date': datetime.date.today().isoformat(),
    'date_of_meeting': args.meeting_date.isoformat(),
    'time_of_meeting': args.meeting_time.strftime("%H:%M"),
    'location': args.location,
    'type': args.type,
    'attendance': args.attendance,
    }

    script_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(script_path, 'Templates', 'memo_template.txt')

    with open(template_path, 'r') as myfile:
        template_str=myfile.read()
    
    out = pystache.render(template_str, dic)

    directory = os.path.join(script_path,
                             args.meeting_date.strftime("%Y"),
                             args.meeting_date.strftime("%m"),
                             args.meeting_date.strftime("%d"))

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = args.meeting_name.replace(' ', '_') + '.txt'
    filepath = os.path.join(directory, filename)

    with open(filepath, 'w') as fp:
        fp.write(out)

    print "Created new memo " + filepath

    subprocess.Popen(['subl', filepath])



if __name__ == '__main__':
    main()
