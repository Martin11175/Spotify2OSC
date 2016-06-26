# Spotify2OSC
Simple python daemon to poll for the currently playing track in spotify 
    using applescript and output the info in OSC format.

Runs in python3 only. Requires `requests`, `py-applescript` and 
`python-osc` as direct pip3 dependencies and `pyobjc` for applescript 
support. Be warned that to install `pyobjc` you will also need x-code
installed on your mac.

Current bpm is polled once per second and output to the `/tempo` OSC
address on `localhost:8000` by default, use the `--ip` and `--port`
input arguments to change.
