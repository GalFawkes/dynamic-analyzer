import subprocess

import consts

'''
D:\Android\Sdk\emulator> avdmanager create avd -p '<PATH>' -n '<NAME>' -k 'system-images;android-16;google_apis;x86' -d 21 -f
D:\Android\Sdk\emulator> .\emulator.exe -avd <NAME> (-verbose) -tcpdump '<PATH TO FILE (all folders must exist)>'
D:\Android\Sdk\platform-tools> .\adb.exe install '<PATH TO APK>'
<TODO: OPEN APP>
<TODO: monkey inputs>
D:\Android\Sdk\platform-tools> .\adb.exe emu kill
'''


def make_avd(name):
    subprocess.run([consts.AVDMANAGER, 'create', 'avd',
                    '-n', name,
                    '-k', 'system-images;android-16;google_apis;x86',
                    '-d', '21', '-f'], shell=True)


def start_emulator(device_name, pcap_path='netcap.pcap'):
    daemon = subprocess.Popen([consts.EMULATOR,
                               '-avd', device_name,
                               '-tcpdump', pcap_path], shell=True)
    return daemon


def install_apk(apk):
    subprocess.run([consts.ADB, 'install', apk], shell=True)


def kill_emu(daemon=None):
    subprocess.run([consts.ADB, 'emu', 'kill'], shell=True)
    if daemon is not None:
        daemon.wait()
