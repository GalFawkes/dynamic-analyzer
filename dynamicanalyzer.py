import argparse
import subprocess
import time

import consts

'''
<TODO: OPEN APP>
<TODO: monkey inputs>
'''
# shell=True is some hackery to make this stuff play nice on Windows, I think


def make_avd(name: str,
             system_image='system-images;android-16;google_apis;x86'):
    '''
    '''
    subprocess.run([consts.AVDMANAGER, 'create', 'avd',  # Standard create AVD
                    '-n', name,  # Name of the AVD
                    '-k', system_image,  # system image type, default is 16 x86
                    '-d', '21',  # Using Google Pixel 3a
                    '-f'],
                   shell=True)  # Override existing


def start_emulator(device_name: str,
                   pcap_path='netcap.pcap') -> subprocess.Popen:
    '''
    Start_emulator uses subprocess.Popen instead of subprocess.run
    The Emulator task doesn't terminate and run is a blocking call.
    To get around this, we start the process as a Popen called "daemon"
    and return it for future use.
    '''
    daemon = subprocess.Popen([consts.EMULATOR,
                               '-avd', device_name,  # the name of the device
                               '-tcpdump', pcap_path,  # pcap location
                               '-no-window'],
                              shell=True)
    return daemon


def install_apk(apk: str):
    '''
    Installs the APK at (string filepath)
    '''
    subprocess.run([consts.ADB,
                    'install', apk],
                   shell=True)


def kill_emu(daemon: subprocess.Popen):
    '''
    Kills emulator process. This is built to take the daemon from
    start_emulator and make sure the process terminates clearly.
    Please maintain the daemon, it's a bit safer
    '''
    subprocess.run([consts.ADB, 'emu', 'kill'], shell=True)
    if daemon is not None:
        daemon.wait()  # Waits for daemon to end before terminating


def clean_and_start_emulator(name: str,
                             apk_location=None) -> subprocess.Popen:
    '''
    Clean encapsulation for startup process. Defaults used.
    '''
    make_avd(name)
    daemon = start_emulator(name)
    time.sleep(60)
    if type(apk_location) is str:
        install_apk(apk_location)
    return daemon


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    commands = parser.add_mutually_exclusive_group()
    parser.add_argument('APK',
                        help='APK to install')
    parser.add_argument('-n', '--name',
                        help='name of emulator',
                        default='dynamic_testbed')
    commands.add_argument('-d', '--demo',
                          action='store_true',
                          help="run demo")
    commands.add_argument('-b', '--bulk', action='store_true')

    args = parser.parse_args()
    # print(args)
    if args.demo:
        print('Starting system...')
        daemon = clean_and_start_emulator('demo')
        time.sleep(120)
        print('killing system...')
        kill_emu(daemon)
        print('Done!')
    elif args.bulk:
        print('bulk processing...')
    else:
        print('Starting system...')
        daemon = clean_and_start_emulator(args.name, args.APK)
        time.sleep(120)  # Swap out for Monkey stuff
        print('killing system...')  # Swap out for Monkey stuff
        kill_emu(daemon)
        print('Done!')
