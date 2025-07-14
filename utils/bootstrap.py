"""Bootstrapping how to start a shadowsocks server.

If you don't use shadowsocks server often,
you forget how to configure it and end up relearning it everytime.
This script guides you through the process by asking questions in the console.
It is built on top of the knowledge from
https://iceberg.bitbucket.io/markdown.html?doc=shadowsocks/shadowsocks-installation.md

Prerequisite:

1. You already have Python 3.x installed in your system

2. Recommended to use "pipx" or "uv install tool" or a virtual environment

   pip install -r requirements-bootstrap.txt

3. Download this script from the repository and run it

   python bootstrap.py
"""

import base64
import getpass
import json


def get_user_input(prompt, default=None, example=None):
    """Get user input with optional default value and example.

    If no default value is provided, user must input something.
    """
    if default and example:
        user_input = input(f"{prompt} [default: {default}, example: {example}]: ")
    elif default:
        user_input = input(f"{prompt} [default: {default}]: ")
    elif example:
        user_input = input(f"{prompt} [example: {example}]: ")
    else:
        user_input = input(f"{prompt}: ")

    # If there's no default and user didn't enter anything, keep asking
    while not default and not user_input:
        print("Input is required. Please enter a value.")
        user_input = input(f"{prompt}: ")

    return user_input if user_input else default


def generate_outline_accesskey(
    *,
    password,
    ip,
    method="chacha20-ietf-poly1305",
    port=443,
):
    part = base64.b64encode(f"{method.lower()}:{password}".encode()).decode()
    return f"ss://{part}@{ip}:{port}"


def main():
    """Main function to collect user configuration."""
    print("Shadowsocks Server Configuration")
    print("--------------------------------")
    print(__doc__)

    config = {
        "server": "0.0.0.0",
        "server_port": int(get_user_input(
            "Enter the port that server listens to. This is also the port that you will configure your router to forward TO",
            example="8388",
        )),
        "local_address": "127.0.0.1",  # Not typically changed
        "local_port": 1080,  # Not typically changed
        "password": getpass.getpass(
            "Enter the password for the shadowsocks server (will not be displayed): "
        ),
        "timeout": 300,
        "method": "chacha20-ietf-poly1305",  # Recommended method
        "fast_open": False,  # TCP Fast Open (TFO) is only available on Windows 10, 1607 or later version (precisely, build >= 14393)
    }
    with open('shadowsocks.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
    print("""Configuration saved to shadowsocks.json.
You can now manage your shadowsocks server by:

    ssserver -c shadowsocks.json -d start
    ssserver -c shadowsocks.json -d restart
    ssserver -c shadowsocks.json -d stop

You may also need to specify the server's pid file and log file location.

    ... -pid-file /tmp/shadowsocks.pid --log-file /tmp/shadowsocks.log

Make sure to configure your router to forward the internet port
to the server's internal IP address and port.""")

    print("\nIf you need an outline Access Key, you can generate it now.")
    print(generate_outline_accesskey(
        password=config["password"],
        ip=get_user_input(
            "Enter publicly accessible server host, i.e. your internet IP address or domain name",
            default=None,
            example="such as example.com or 12.34.56.78",
        ),
        method=config["method"],
        port=int(get_user_input(
            "Enter publicly accessible server port. This is the port that your router will forward FROM. Recommended: 80 or 443",
            default="443",
        )),
    ))

if __name__ == "__main__":
    main()
