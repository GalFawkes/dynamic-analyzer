import subprocess

import consts

'''
<TODO: OPEN APP>
<TODO: monkey inputs>
'''
# shell=True is some hackery to make this stuff play nice on Windows, I think


def make_avd(name, system_image='system-images;android-16;google_apis;x86'):
    subprocess.run([consts.AVDMANAGER, 'create', 'avd',  # Standard create AVD
                    '-n', name,  # Name of the AVD
                    '-k', system_image,  # system image type, default is 16 x86
                    '-d', '21',  # Using Google Pixel 3a
                    '-f'],
                    shell=True)  # Override existing


def start_emulator(device_name, pcap_path='netcap.pcap'):
    daemon = subprocess.Popen([consts.EMULATOR,
                               '-avd', device_name,  # the name of the device
                               '-tcpdump', pcap_path],  # Where we want the net capture
                               shell=True)
    return daemon


def install_apk(apk):
    subprocess.run([consts.ADB, 'install', apk], shell=True)


def kill_emu(daemon=None):
    subprocess.run([consts.ADB, 'emu', 'kill'], shell=True)
    if daemon is not None:
        daemon.wait()
