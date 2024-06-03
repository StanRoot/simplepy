import pathlib
import re

workdir = pathlib.Path.home() / 'slink' / 'wsld'


def parserInterfaceDescription(configfile):
    
    with configfile.open(mode='r', encoding='utf-8') as file:
        for line in file.readlines():
            interface_match = re.search(r'interface\s\S+', line)
            
            description_match = re.search(r'description\s(\S+)', line)
            description = description_match.group() if description_match else None
            print(configfile.name, '--', interface, '--', description)

for file in workdir.glob('*FL.txt'):
    parserInterfaceDescription(file)
