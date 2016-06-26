#!/usr/bin/env python3
import argparse
import time
import requests
import applescript
from requests.auth import HTTPBasicAuth
from pythonosc import osc_message_builder
from pythonosc import udp_client

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
hdr = {"Authorization": "Bearer " + auth}

# Loop 5ever
while True:
    # Applescript to retrieve current playing track ID from Spotify
    scpt = applescript.AppleScript('''
        tell application "Spotify"
            set currentTrackID to id of current track as string
            return currentTrackID
        end tell''')
    track_id = scpt.run()
    track_id = track_id[14:]
    track_id = track_id.rstrip()
    print("Track ID: " + track_id)

    # Request bpm information from Spotify Web API
    response = requests.get("https://api.spotify.com/v1/audio-features/" + track_id, headers=hdr)
    if response.status_code != 200:
        # If token timed out, re-authorise
        auth_response = requests.post("https://accounts.spotify.com/api/token",
                                      auth=login_hdr,
                                      data={"grant_type": "client_credentials"})
        if auth_response.status_code != 200:
            print("AUTH ERROR: ", auth_response.status_code)
        auth = auth_response.json()["access_token"]
        hdr = {"Authorization": "Bearer " + auth}

        # Try again
        response = requests.get("https://api.spotify.com/v1/audio-features/" + track_id, headers=hdr)
        if response.status_code != 200:
            print("REQUEST ERROR: ", response.status_code)
            print('{}\n{}\n{}\n\n{}'.format(
                '-----------START-----------',
                response.request.method + ' ' + response.request.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in response.request.headers.items()),
                response.request.body,
            ))

    bpm = response.json()["tempo"]
    print(bpm)

    # Construct and send OSC Packet
    msg = osc_message_builder.OscMessageBuilder(address="/tempo")
    msg.add_arg(bpm)
    msg = msg.build()
    endpoint.send(msg)

    # Wait and go again
    time.sleep(1)
