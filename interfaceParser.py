import pathlib
import re
from time import sleep


def parseInterfaceConfig(config):
    interfaces = {}
    current_interface = None

    for line in config.splitlines():
        line = line.strip()
        
        # Detect interface line
        match = re.match(r'^interface (\S+)', line)
        if match:
            current_interface = match.group(1)
            interfaces[current_interface] = {
                'description': None,
                'ip_address': None,
                'port_mode': None
            }
            continue
        
        if current_interface:
            # Detect description line
            match = re.match(r'^description (.+)', line)
            if match:
                interfaces[current_interface]['description'] = match.group(1)
                continue

            # Detect IP address line
            match = re.match(r'^ip address (\S+ \S+)', line)
            if match:
                interfaces[current_interface]['ip_address'] = match.group(1)
                continue

            # Detect port mode line
            match = re.match(r'^switchport mode (\S+)', line)
            if match:
                interfaces[current_interface]['port_mode'] = match.group(1)
                continue

    return interfaces


def main():
    # Script description
    print('\n' + '='*32 + ' DESCRIPTION ' + '='*32 + '\n' +
          'Это простой парсер конфигурационных файлов сетевого оборудования.\n' +
          'Скрипт анализирует конфигурационные файлы по заданному пути и\n' +
          'извлекает настройки интерфейсов, такие как описание, IP-адрес и режим порта.\n' +
          '='*77 + '\n')
    # Script delay before requesting user input
    sleep(0.5)

    # Requesting the path to the folder containing configuration files and verifying its existence
    while True:
        user_input_path = input('Введите путь к папке с конфигурационными файлами относительно домашней директории: ')
        workdir = pathlib.Path.home() / user_input_path
        if workdir.exists():
            break
        else:
            print('Указанная директория не существует.\n')

    # Requesting a wildcard pattern for the glob() method
    user_input_glob_tpl = input('\nВведите шаблон с подстановочным символом: ')
    while user_input_glob_tpl.strip() == '':
        user_input_glob_tpl = input("\nВы ввели пустую строку. Пожалуйста, маску для поиска: ")

    # Iterate over files in the specified directory matching the glob pattern.
    for file in workdir.glob(user_input_glob_tpl):
        print(f"\n{'-' * 30} {file.name} {'-' * 30}\n")

        with open(file, 'r') as openfile:
            config = openfile.read()
        
            interfaces = parseInterfaceConfig(config)
        
            for intf, details in interfaces.items():
                print(f"Interface: {intf}")
                print(f"  Description: {details['description']}")
                print(f"  IP Address: {details['ip_address']}")
                print(f"  Port Mode: {details['port_mode']}")
                print()

if __name__ == "__main__":
    main()
