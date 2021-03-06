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
    network = 'lan'
    required_parameters = [
        executable,
        f'/u:{user}',
        f'/d:{domain}',
        f'/v:{hostname}:{port}',
        f'/t:RDP: {name}',
        '/from-stdin',
        '+toggle-fullscreen',
        '+auto-reconnect',
        '/auto-reconnect-max-retries:20',
        '+clipboard',
        '+mouse-motion',
        '/gdi:hw',
        '/ipv6',
        '+multitransport',
        '+multitouch',
        '/geometry',
        '+gestures',
        '+offscreen-cache',
        '+bitmap-cache',
        '+glyph-cache',
        '/jpeg',
        '+async-channels',
        '+async-update',
        '+async-input',
        '/frame-ack:1',
        '+fonts',
        '-grab-keyboard',
        f'/floatbar:sticky:on,default:visible,show:{floatbar}',
        '/cert:tofu',
        '/log-level:WARN'
    ]
    optional_parameters = []

    if 'Fullscreen' in session and session['Fullscreen'] == True:
        optional_parameters.append('/f')

    if 'DefaultWindowSize' in config and 'x' in config["DefaultWindowSize"] and 'y' in config["DefaultWindowSize"]:
        optional_parameters.append(f'/size:{config["DefaultWindowSize"]["x"]}x{config["DefaultWindowSize"]["y"]}')

    if 'DynamicResolution' in config and config["DynamicResolution"] == True:
        optional_parameters.append('/dynamic-resolution')

    if 'Network' in session:
        network = session['Network']
        if session['Network'] == 'wan':
            optional_parameters.append(f'/network:{network}')
            optional_parameters.append(f'-wallpaper')
            optional_parameters.append(f'-themes')
            optional_parameters.append(f'-decorations')
            optional_parameters.append(f'-aero')
            optional_parameters.append(f'-menu-anims')
            optional_parameters.append(f'-window-drag')
        else:
            optional_parameters.append(f'/network:{network}')
    else:
        optional_parameters.append(f'/network:{network}')
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

