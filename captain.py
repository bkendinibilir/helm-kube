#!/usr/bin/env python3

try:
    import configparser
except:
    import ConfigParser as configparser
import json
import os
import subprocess as sp
import sys
import yaml

def execute(cmd, verbose=False):
    if verbose:
        print(cmd)
    process = sp.Popen(cmd, stdout=sp.PIPE)
    return process.wait()

def get_chart(release_filename):
    stream = open(release_filename, 'r')
    release_data = yaml.load(stream)
    return release_data.get('chart', None)

config = configparser.ConfigParser()
config.read('captain.cfg')

charts_dir = config.get('helm', 'local_charts_dir')
k8s_context = config.get('kubernetes', 'context')
releases_dir = "releases"

print("switching kubernetes context to: {}".format(k8s_context))
exitcode = execute(["kubectl", "config", "use-context", k8s_context])

if exitcode != 0:
    sys.exit(exitcode)

with open('secrets.json') as json_secrets:
    secrets = json.load(json_secrets)

value_files = {}

print("apply: manifests")
execute(["kubectl", "apply", "-f", "manifests"])

for path, _, files in os.walk(releases_dir):
    if files:
        dirs = path.split('/')
        if len(dirs) == 2 and dirs[0] == releases_dir:
            namespace = dirs[1]
            for name in files:
                if name.endswith('.yaml'):
                    value_files[name] = namespace

for file_name, namespace in value_files.items():
    release_file = "{}/{}/{}".format(releases_dir, namespace, file_name)

    chart = get_chart(release_file)
    if not chart:
        print("no chart set in: {}".format(release_file))
        continue
    release = file_name.split('.yaml')[0]
    
    print("apply: namespace={}, chart={}, name={}".format(namespace, chart, release))

    set_string = ""
    for (key, val) in secrets.get(namespace, {}).get(release, {}).items():
        set_string += "{}={},".format(key, val)
    
    c = chart.split('/')
    if(len(c) == 2 and c[0] == 'local'):
        chart="{}/{}".format(charts_dir, c[1])

    execute(
        [
            "helm", "upgrade", "-i", release, chart, 
            "--namespace", namespace, 
            "--set", set_string[:-1], 
            "-f", release_file
        ], 
        verbose=False
    )
