#!/usr/bin/python
# -*- coding: utf-8 -*-
# example: python cron_dups.py -u <username> -p passwd -v

import cli
import elisaviihde

def main():
    parser = cli.init_argparser()
    params = parser.parse_args()

    username = cli.read_input(params.user, 'Elisa Viihde Username')
    password = cli.read_password(params.passfile, 'Elisa Viihde Password')

    e = elisaviihde.Elisaviihde(params.verbose)

    if not e.login(username, password):
        exit(-1)

    # From root up
    folder = e.find_folder_by_id(0)

    recordings = e.ls_recordings_recursive(folder, [])
    found_duplicates = find_duplicates(recordings, params.verbose)

    # If nothing to delete, end
    if len(found_duplicates) < 1:
        return

    # Loop-de-loop
    for key, recordings in found_duplicates.iteritems():
        if params.verbose > 0:
            print 'Processing:', key[0], ';', key[1]
        first = True
        for recording in recordings:
            if first:
                if params.verbose > 1:
                    print 'Kept first', recording['startTime'], recording['channel']
                first = False
            else:
                status = e.delete(recording['programId'])
                if params.verbose > 2:
                    print 'DELETED', status, recording['startTime'], recording['channel']
    if params.verbose > 0:
        print 'Delete duplicates done.'
        
    
def find_duplicates(recordings, verbosity):
    # arrange programs as hastable {(name, description): [recording, recording], ...}
    recordings_dict = {}
    for recording in recordings:
        key = (recording['name'].strip(), recording.get('description', '').strip())
        value = recordings_dict.get(key, [])
        value.append(recording)
        recordings_dict[key] = value
    
    # hastable {(name, description): [recording, recording], ...}
    # where recordings ordered by not-HD, startTimeUTC timestamp
    duplicate_recordings_dict = {}
    for key, recordings in recordings_dict.iteritems():
        if len(recordings) > 1:
            recordings.sort(key=lambda r: (not r['channel'].endswith('HD'), r['startTimeUTC']))
            duplicate_recordings_dict[key] = recordings
            if verbosity > 1:
                print 'Found duplicates for:', key[0]
            for recording in recordings:
                if verbosity > 2:
                    print '*', recording['startTime'], recording['channel']
    if verbosity > 0:
        print 'Total', len(duplicate_recordings_dict)
    return duplicate_recordings_dict

if __name__ == '__main__':
    main()
