#!/usr/bin/env python3
import argparse
import time
import requests
import string
from requests.auth import HTTPBasicAuth
from pythonosc import osc_message_builder
from pythonosc import udp_client
from subprocess import Popen, PIPE

# Endpoint specification
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=8000, help="The port the OSC server is listening on")
args = parser.parse_args()

CLIENT_ID = 'e90e8c6232b74444901ce298d64d28c9'
CLIENT_KEY = 'df92dda22b4c4645af2991175a6ad62a'

endpoint = udp_client.UDPClient(args.ip, args.port)
login_hdr = HTTPBasicAuth(CLIENT_ID, CLIENT_KEY)
auth = ""

# Loop 5ever
while True:
    # Applescript to retrieve current playing track ID from Spotify
    #scpt = '''
    #    tell application "Spotify"
    #        set currentTrackID to id of current track as string
    #        return currentTrackID
    #    end tell'''
    #args = []

    # Run Applescript and process output
    #p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    #stdout, stderr = p.communicate(scpt)
    #track_id = stdout.decode()
    #track_id = track_id[14:]
    track_id = "2fmIPKZ6dpko0N4MQuzH4N"

    # Request bpm information from Spotify Web API
    hdr = {"Authorization": "Bearer " + auth}
    response = requests.get("https://api.spotify.com/v1/audio-features/" + track_id, headers=hdr)
    if response.status_code != 200:
        # If token timed out, re-authorise
        auth_response = requests.post("https://accounts.spotify.com/api/token",
                                      auth=login_hdr,
                                      data={"grant_type": "client_credentials"})
        auth = auth_response.json()["access_token"]
        hdr = {"Authorization": "Bearer " + auth}
        response = requests.get("https://api.spotify.com/v1/audio-features/" + track_id, headers=hdr)

    bpm = response.json()["tempo"]
    print(bpm)

    # Construct and send OSC Packet
    msg = osc_message_builder.OscMessageBuilder(address="/tempo")
    msg.add_arg(bpm)
    msg = msg.build()
    endpoint.send(msg)

    # Wait and go again
    time.sleep(1)
