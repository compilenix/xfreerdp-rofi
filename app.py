#!/usr/bin/env python3

import json
import os
import sys
import base64
import time
from subprocess import PIPE, Popen

config_file = open(os.environ['HOME'] + '/.config/xfreerdp/config.json', 'r')
config = json.loads(config_file.read())
config_file.close()

if len(sys.argv) < 2:
    print('ERROR: a parameter is required!', file=sys.stderr)
    exit(1)

action = sys.argv[1]
if len(sys.argv) > 2:
    session_name = sys.argv[2][:-1] # remove linebrak at the end
else:
    session_name = ''

sessions = config['Sessions']
sessions = sorted(sessions, key=lambda session: session['Name'])

def run_command(command, input):
    process = Popen(
            args=command,
            stdin=PIPE,
            stdout=sys.stdout,
            stderr=sys.stderr,
            encoding='utf-8',
        )
    process.stdin.write(input)
    process.stdin.flush()
    process.communicate()
    return process.returncode

def start_session(session):
    port = session['Port'] if 'Port' in session else 3389
    executable = config['ExecutableOverwride'] if 'ExecutableOverwride' in config else 'xfreerdp'
    password = base64.b64decode(session['Password']).decode('utf-8')
    user = session['User']
    domain = session['Domain']
    name = session['Name']
    hostname = session['HostName']
    floatbar = session['Floatbar'] if 'Floatbar' in session else config['Floatbar']
    required_parameters = [
        executable,
        f'/u:{user}',
        f'/d:{domain}',
        f'/v:{hostname}:{port}',
        f'/t:RDP: {name}',
        f'/from-stdin',
        f'+toggle-fullscreen',
        f'+auto-reconnect',
        f'/auto-reconnect-max-retries:20',
        f'+drives',
        f'+home-drive',
        f'/dynamic-resolution',
        f'+clipboard',
        f'+mouse-motion',
        f'/rfx',
        f'/gdi:hw',
        f'/video',
        f'/ipv6',
        f'+multitransport',
        f'+multitouch',
        f'/geometry',
        f'+gestures',
        f'+offscreen-cache',
        f'/async-update',
        f'/async-input',
        f'/frame-ack:1',
        f'+fonts',
        f'/floatbar:sticky:on,default:visible,show:{floatbar}',
        f'-encryption',
        f'/cert-ignore',
    ]
    optional_parameters = []

    if 'Fullscreen' in session and session['Fullscreen'] == True:
        optional_parameters.append('/f')
    else:
        optional_parameters.append(f'/w:{config["DefaultWindowSize"]["w"]}')
        optional_parameters.append(f'/h:{config["DefaultWindowSize"]["h"]}')

    if 'Network' in session:
        if session['Network'] == 'wan':
            optional_parameters.append(f'/network:{session["Network"]}')
            optional_parameters.append(f'-wallpaper')
            optional_parameters.append(f'-themes')
            optional_parameters.append(f'-decorations')
            optional_parameters.append(f'-aero')
            optional_parameters.append(f'-menu-anims')
            optional_parameters.append(f'-window-drag')
        else:
            optional_parameters.append(f'/network:{session["Network"]}')
    else:
        optional_parameters.append(f'/network:{session["Network"]}')
        optional_parameters.append(f'+wallpaper')
        optional_parameters.append(f'+themes')
        optional_parameters.append(f'+decorations')
        optional_parameters.append(f'+aero')
        optional_parameters.append(f'+menu-anims')
        optional_parameters.append(f'+window-drag')

    if 'Compression' in session:
        optional_parameters.append(f'+compression')
        optional_parameters.append(f'/compression-level:{session["Compression"]}')

    if 'DisableSound' in config and config['DisableSound'] == True:
        optional_parameters.append(f'/audio-mode:2')
    else:
        optional_parameters.append(f'/audio-mode:0')

    if 'Admin' in session:
        optional_parameters.append(f'/admin')

    print(f'echo "{password}" | {" ".join(required_parameters + optional_parameters)}')

    return run_command(required_parameters + optional_parameters, password)

if action == 'list':
    for i, session in enumerate(sessions, start=1):
        print(session['Name'], end='')
        if i < len(sessions):
            print()

if action == 'run':
    for session in sessions:
        if session['Name'] == session_name:
            start_session(session)

