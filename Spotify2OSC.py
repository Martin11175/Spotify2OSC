from subprocess import Popen, PIPE

# TODO: Port specification / default

# TODO: Loop

# TODO: Applescript to retrieve current playing track ID from Spotify
scpt = '''
    on run {x, y}
        return x + y
    end run'''
args = ['2', '2']

# TODO: Run Applescript and process output
p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
stdout, stderr = p.communicate(scpt)
print (p.returncode, stdout, stderr)

# TODO: Request bpm information from Spotify Web API

# TODO: Process Spotify Web API response

# TODO: Create OSC Packet

# TODO: Send OSC packet to specified port
