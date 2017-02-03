#!/usr/bin/env python

import ConfigParser
import json
import os
import subprocess as sp
import sys

def execute(cmd, verbose=False):
    if verbose:
        print cmd
    process = sp.Popen(cmd, stdout=sp.PIPE)
    return process.wait()

config = ConfigParser.ConfigParser()
config.read('captain.cfg')

charts_dir = config.get('helm', 'charts_dir')
k8s_context = config.get('kubernetes', 'context')

print "switching kubernetes context to: {}".format(k8s_context)
exitcode = execute(["kubectl", "config", "use-context", k8s_context])

if exitcode != 0:
    sys.exit(exitcode)

with open('secrets.json') as json_secrets:
    secrets = json.load(json_secrets)

value_files = {}

print "apply: manifests"
execute(["kubectl", "apply", "-f", "manifests"])

for path, _, files in os.walk("values/"):
    if files:
        dirs = path.split('/')
        if len(dirs) == 2 and dirs[0] == 'values':
            namespace = dirs[1]
            for name in files:
                if name.endswith('.yaml'):
                    value_files[name] = namespace

for file_name, namespace in value_files.iteritems():
    release_chart = file_name.split('.yaml')[0]
    (release, chart) = release_chart.split('_')

    print "apply: namespace={}, chart={}, name={}".format(namespace, chart, release)
    set_string = ""
    for (key, val) in secrets.get(namespace, {}).get(release_chart, {}).iteritems():
        set_string += "{}={},".format(key, val)
    
    execute(
        [
            "helm", "upgrade", "-i", release, 
            "{}/{}".format(charts_dir, chart), 
            "--namespace", namespace, 
            "--set", set_string[:-1], 
            "-f", "values/{}/{}".format(namespace, file_name)
        ], 
        verbose=False
    )
