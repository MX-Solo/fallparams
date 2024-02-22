import argparse
import re
import requests
import os

ext = ['php','jsp']

def remove_duplicates():
    lines_seen = set() 

    with open('param.txt', 'r') as input_f, open('params.txt', 'w') as output_f:
        for line in input_f:
            if ':' in line :
                continue
            if line not in lines_seen:  
                output_f.write(line)
                lines_seen.add(line)  

    os.remove('param.txt')

def main():
    pattern = '[\w-]+\.(?:'
    for i, item in enumerate(ext):
        if i == 0:
            pattern += item
            continue
        pattern += '|'+item

    pattern += ')(?=")'

    parser = argparse.ArgumentParser(description='Fetch messages from URL if regex pattern found')
    parser.add_argument('-u', '--url', type=str, required=True, help='URL')
    args = parser.parse_args()

    response = requests.get(args.url)
    if response.status_code == 200:
        with open('param.txt', 'w') as file:
            messages = re.findall('<(?!meta\s).*?(id|name)="([^"]+)"', response.text)
            for message in messages:
                for id in message:
                    file.write(id+'\n')


            messages = re.findall('(?:let|var|const)\s+(\w+(?:,\s*\w+)*)', response.text)
            for message in messages:
                for varible in message:
                    file.write(varible+'\n')

            messages = re.findall('"(\w+)":', response.text)
            for json in messages:
                file.write(json+'\n')


            messages = re.findall(pattern, response.text)
            for message in messages:
                for e in ext :
                    if e in message :
                        filename = message.replace('.'+e,'')
                        file.write(filename+'\n')
        remove_duplicates()

    else:
        print(f'Failed to fetch messages. Status code: {response.status_code}')

if __name__ == '__main__':
    main()
