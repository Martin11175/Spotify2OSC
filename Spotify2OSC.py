#!/usr/bin/env python3
import argparse
import time
import requests
from pythonosc import osc_message_builder
from pythonosc import udp_client
from subprocess import Popen, PIPE

# Endpoint specification
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=1604, help="The port the OSC server is listening on")
args = parser.parse_args()

endpoint = udp_client.UDPClient(args.ip, args.port)

# Loop 5ever
while True:
    # Applescript to retrieve current playing track ID from Spotify
    scpt = '''
        tell application "Spotify"
            set currentTrackID to id of current track as string
            return currentTrackID
        end tell'''
    args = []

    # Run Applescript and process output
    p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(scpt)
    track_id = stdout.decode()

    # Request bpm information from Spotify Web API
    auth = {"Authorization": "Bearer BQDEXKDMBLGhSU1sULRnmeO1aM9fkRhncog4fjfCMD9-"
                             "Gw4dkb7qRPYU-aFwmF7kVDDIXMLk4eJNzt47Ecgww8SkYYy0Q1R"
                             "3PqQyBbkBLG8NZ3qRTsmS8WYYQc3ZMEU4Fk_dr7Fsg77M"}
    response = requests.get("https://api.spotify.com/v1/audio-features/" + track_id, headers=auth)
    bpm = response.json()["tempo"]

    # Construct and send OSC Packet
    msg = osc_message_builder.OscMessageBuilder(address="/filter")
    msg.add_arg(bpm)
    msg = msg.build()
    endpoint.send(msg)

    # Wait and go again
    time.sleep(1)
