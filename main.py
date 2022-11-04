from morse_code import ascii_to_morse, morse_to_ascii
from generate_wav import generate_audio_data, generate_wav_file

from os import getcwd, name, system
from sys import exit
import json


def clear():
    # Clears the screen.
    if name == 'nt':
        return system('cls')
    else:
        return system('clear')


def change_filepath(filepath):
    # Takes an input and deliver an appropriate filepath for the operating system.
    if name == 'nt':
        return filepath.replace('/', '\\')
    else:
        return filepath.replace('\\', '/')


def create_wav_file(filepath, morse_text, dit_length, frequency, volume, sample_rate, waveform='sine'):
    filename = input('Enter a name for your wav file: ')
    print('Please wait while your audio file is being generated...')
    filename = filepath + slash() + filename + '.wav'
    audio_data = generate_audio_data(morse_text,
                                     dit_length,
                                     frequency,
                                     volume,
                                     sample_rate,
                                     waveform)
    generate_wav_file(filename, sample_rate, audio_data)
    print(f'File created at {filename}')
    print('Press "Enter" to return to the main screen.')
    command = input('')
    if command:
        return main()


def get_settings():
    with open('settings.json') as f_obj:
        data = json.load(f_obj)
    f_obj.close()
    return data


def slash():
    if name == 'nt':
        return '\\'
    else:
        return '/'


def home_screen():
    clear()
    print('Welcome to Morse Code Console Application. Please enter a command.')
    print('1 > ASCII to Morse')
    print('2 > Morse to ASCII')
    print('3 > Settings')
    print('4 > About')
    print('Q > Exit')
    command = input('')
    return command


def ascii_to_morse_screen(settings):
    clear()
    filepath = settings["filepath"]
    frequency = settings["frequency"]
    dit_length = settings["dit_length"]
    sample_rate = settings["sample_rate"]
    volume = settings["volume"]
    print('Enter text to convert to morse code.')
    ascii_text = input('')
    morse_text = ascii_to_morse(ascii_text)
    print(morse_text)
    print()
    print('Enter "1" to generate a .wav file.')
    print('Press "Enter" to return to the main screen.')
    command = input('')
    if command == '1':
        create_wav_file(filepath, morse_text, dit_length, frequency, volume, sample_rate, waveform='sine')
    return main()


def morse_to_ascii_screen(settings):
    clear()
    filepath = settings["filepath"]
    frequency = settings["frequency"]
    dit_length = settings["dit_length"]
    sample_rate = settings["sample_rate"]
    volume = settings["volume"]
    print('Please enter a series of morse code tokens to be converted to ASCII, '
          'with intra-letter spaces separated by one space and inter-word spaces '
          'seperated by three spaces.')
    morse_text = input('')
    print(morse_to_ascii(morse_text))
    print('Enter "1" to generate a .wav file.')
    print('Press "Enter" to return to the main screen.')
    command = input('')
    if command == '1':
        create_wav_file(filepath, morse_text, dit_length, frequency, volume, sample_rate, waveform='sine')
    return main()


def settings_screen():
    clear()
    with open('settings.json') as f_obj:
        settings = json.load(f_obj)
        f_obj.read()
    if not settings['filepath']:
        settings['filepath'] = str(getcwd() + '/wav_files').replace('\\', '/')
    settings = dict(settings)
    print('To change a setting, type in the number followed by a space and the new value.')
    print('For example, to change the sample rate to 8000, enter "4 8000".')
    print('1 > Filepath: ' + settings['filepath'].replace('\\\\', '/'))
    print('2 > Frequency: ' + str(settings['frequency']) + ' Hz')
    print('3 > Dit Length: ' + str(settings['dit_length']) + ' ms')
    print('4 > Sample Rate: ' + str(settings['sample_rate']) + ' Hz')
    print('5 > Volume: ' + str(int(settings['volume']) * 100))
    print('R > Reset all settings to default.')
    print('Q > Return to the main screen.')
    print('')
    command = input('')
    if command.upper() == 'Q':
        return main()
    elif command.upper() == 'R':
        with open('default_settings.json', 'r') as default_f_obj:
            default_settings = json.load(default_f_obj)
        settings = dict(default_settings)
    else:
        command = command.split(' ')
        try:
            if command[0] == '1':
                settings['filepath'] = change_filepath(command[1])
            if command[0] == '2':
                settings['frequency'] = int(command[1])
            if command[0] == '3':
                settings['dit_length'] = int(command[1])
            if command[0] == '4':
                settings['sample_rate'] = int(command[1])
            if command[0] == '5':
                if 0 < float(command[1]) < 100:
                    settings['volume'] = float(command[1]) / 100
                elif float(command[1]) == '5' and float(command[1]) > 100:
                    settings['volume'] = 1
                else:
                    settings['volume'] = 0
        except TypeError:
            return settings_screen()
    with open('settings.json', 'w') as f_obj:
        json.dump(settings, f_obj)
    return settings_screen()


def about_screen():
    clear()
    print('          Morse Code Console Application')
    print('Version:      1.0')
    print('Repository:   https://www.github.com/EMitchell44/morse_code_console_application')
    print('Written by:   Ethan Israel Mitchell')
    print('Github:       https://www.github.com/EMitchell44')
    print('Website:      Pending')
    print('Motto:        "Good enough" is not good enough.\n')
    command = input('Press "Enter" to return to the main screen.')
    return main()


def main():
    settings = get_settings()
    settings = dict(settings)
    # Create a filepath for .wav files if there isn't one.
    if not settings['filepath']:
        settings['filepath'] = getcwd() + slash() + 'wav_files'
    clear()
    command = home_screen()
    if command == '1':
        ascii_to_morse_screen(settings)
        main()
    elif command == '2':
        morse_to_ascii_screen(settings)
    elif command == '3':
        settings_screen()
    elif command == '4':
        about_screen()
    if command.upper() == 'Q':
        exit()


main()
