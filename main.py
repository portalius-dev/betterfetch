#!/usr/bin/env python3
import argparse
import configparser
import os
import platform
import shutil
import sys
import time
from pathlib import Path
import subprocess

# Попытка импорта библиотек; установка при отсутствии
try:
    import psutil
    import colorama
    from PIL import Image
except ImportError:
    print("Требуемые библиотеки не найдены. Установка...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", "psutil", "colorama", "pillow"])
    import psutil
    import colorama
    from PIL import Image

# Инициализация цвета для Windows/Linux
colorama.init()

# ANSI цвета
class Colors:
    RESET = colorama.Style.RESET_ALL
    BOLD = colorama.Style.BRIGHT
    RED = colorama.Fore.RED
    GREEN = colorama.Fore.GREEN
    YELLOW = colorama.Fore.YELLOW
    BLUE = colorama.Fore.BLUE
    MAGENTA = colorama.Fore.MAGENTA
    CYAN = colorama.Fore.CYAN
    WHITE = colorama.Fore.WHITE

# Пути к конфигурации
CONFIG_DIR = os.path.join(
    os.path.expanduser("~"),
    ".config" if platform.system() != "Windows" else "AppData\\Roaming",
    "betterfetch"
)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")
DEFAULT_ART_DIR = os.path.join(CONFIG_DIR, "art")

# Создание директорий, если их нет
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(DEFAULT_ART_DIR, exist_ok=True)

# ASCII-арт по умолчанию
DEFAULT_ASCII_ART = {
    "Windows": r"""Dear Windows User, i am sorry but it's VERY HARD to build CLI app on windows (for me ig)""",
    "Linux": r"""
{white}              a8888b.
{white}             d888888b.
{white}             8P"YP"Y88
{white}             8|o{||o|88
{white}             8'    .88
{white}             8`._.' Y8.
{yellow}            d/      `8b.
{yellow}           dP   .    Y8b.
{yellow}          d8:'  "  `::88b
{yellow}         d8"         'Y88b
{yellow}        :8P    '      :888
{yellow}         8a.   :     _a88P
{yellow}       ._/"Yaa_:   .| 88P|
{cyan}       \    YP"    `| 8P  `.
{cyan}       /     \.___.d|    .'
{cyan}       `--..__)8888P`._.'
    """,
    "Darwin": r"""
    {green}                    c.'
    {green}                 ,xNMM.
    {green}               .OMMMMo
    {green}               lMM"
    {green}     .;loddo:.  .olloddol;.
    {green}   cKMMMMMMMMMMNWMMMMMMMMMM0:
    {green} .KMMMMMMMMMMMMMMMMMMMMMMMWd.
    {green} XMMMMMMMMMMMMMMMMMMMMMMMX.
    {green};MMMMMMMMMMMMMMMMMMMMMMMM:
    {green}:MMMMMMMMMMMMMMMMMMMMMMMM:
    {green}.MMMMMMMMMMMMMMMMMMMMMMMMX.
    {green} kMMMMMMMMMMMMMMMMMMMMMMMMWd.
    {green} .XMMMMMMMMMMMMMMMMMMMMMMMMMMk
    {green}  .XMMMMMMMMMMMMMMMMMMMMMMMMK.
    {green}    kMMMMMMMMMMMMMMMMMMMMMMd
    {green}     ;KMMMMMMMWXXWMMMMMMMk.
    {green}       .cooc,.    .,coo:.
    """,
    "Default": r"""
    {cyan}       /\         /\
    {cyan}      /  \       /  \
    {cyan}     /    \     /    \
    {blue}    /      \   /      \
    {blue}   /        \ /        \
    {blue}  /          V          \
    {blue} /                       \
    {green}/__________________________\
    {yellow}|                          |
    {yellow}|                          |
    {yellow}|                          |
    {yellow}|                          |
    {yellow}|                          |
    {yellow}|                          |
    {yellow}|                          |
    {yellow}|                          |
    {red}|__________________________|
    """
}

def create_default_config():
    config = configparser.ConfigParser()
    config['General'] = {
        'use_color': 'true',
        'custom_art_path': '',
        'default_mode': 'normal',
        'ascii_char': '='
    }
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    return config

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return create_default_config()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def get_system_info(verbose=False):
    info = {}
    info['os_name'] = platform.system()
    # OS Version
    if info['os_name'] == 'Windows':
        info['os_version'] = platform.version()
        info['os_release'] = platform.release()
    elif info['os_name'] == 'Linux':
        try:
            with open('/etc/os-release') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith('PRETTY_NAME='):
                        info['os_version'] = line.split('=')[1].strip().strip('"')
                        break
        except:
            info['os_version'] = platform.version()
        info['os_release'] = platform.release()
    elif info['os_name'] == 'Darwin':
        info['os_version'] = f"macOS {platform.mac_ver()[0]}"
        info['os_release'] = platform.release()
    else:
        info['os_version'] = platform.version()
        info['os_release'] = platform.release()
    # Hostname
    info['hostname'] = platform.node()
    # CPU
    info['cpu_model'] = platform.processor()
    if not info['cpu_model'] and platform.system() == 'Linux':
        try:
            with open('/proc/cpuinfo') as f:
                for line in f:
                    if line.startswith('model name'):
                        info['cpu_model'] = line.split(':')[1].strip()
                        break
        except:
            pass
    info['cpu_cores'] = psutil.cpu_count(logical=False)
    info['cpu_threads'] = psutil.cpu_count(logical=True)
    # Memory
    mem = psutil.virtual_memory()
    info['total_memory'] = f"{mem.total / (1024**3):.2f} GB"
    info['used_memory'] = f"{mem.used / (1024**3):.2f} GB"
    info['memory_percent'] = f"{mem.percent}%"
    # Disk
    disk = psutil.disk_usage('/')
    info['total_disk'] = f"{disk.total / (1024**3):.2f} GB"
    info['used_disk'] = f"{disk.used / (1024**3):.2f} GB"
    info['disk_percent'] = f"{disk.percent}%"
    # Verbose info
    if verbose:
        uptime_seconds = int(time.time() - psutil.boot_time())
        days, remainder = divmod(uptime_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        info['uptime'] = f"{days}d {hours}h {minutes}m {seconds}s"
        info['network'] = []
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family.name == 'AF_INET':
                    info['network'].append(f"{interface}: {addr.address}")
        info['gpu'] = ["GPU information unavailable"]
        info['python_version'] = platform.python_version()
        info['shell'] = os.getenv('SHELL', 'cmd.exe' if platform.system() == 'Windows' else 'Unknown')
    return info

def format_system_info(info, compact=False, use_color=True):
    color_map = {
        '{red}': Colors.RED if use_color else '',
        '{green}': Colors.GREEN if use_color else '',
        '{yellow}': Colors.YELLOW if use_color else '',
        '{blue}': Colors.BLUE if use_color else '',
        '{magenta}': Colors.MAGENTA if use_color else '',
        '{cyan}': Colors.CYAN if use_color else '',
        '{white}': Colors.WHITE if use_color else '',
        '{reset}': Colors.RESET if use_color else ''
    }
    lines = []
    if compact:
        lines.append(f"{color_map['{cyan}']}OS:{color_map['{reset}']} {info['os_name']}")
        lines.append(f"{color_map['{green}']}CPU:{color_map['{reset}']} {info['cpu_model']}")
        lines.append(f"{color_map['{yellow}']}Memory:{color_map['{reset}']} {info['used_memory']} / {info['total_memory']} ({info['memory_percent']})")
        lines.append(f"{color_map['{blue}']}Disk:{color_map['{reset}']} {info['used_disk']} / {info['total_disk']} ({info['disk_percent']})")
    else:
        lines.append(f"{color_map['{cyan}']}OS:{color_map['{reset}']} {info['os_name']} {info['os_version']}")
        lines.append(f"{color_map['{cyan}']}Kernel:{color_map['{reset}']} {info['os_release']}")
        lines.append(f"{color_map['{cyan}']}Hostname:{color_map['{reset}']} {info['hostname']}")
        lines.append(f"{color_map['{green}']}CPU:{color_map['{reset}']} {info['cpu_model']}")
        lines.append(f"{color_map['{green}']}Cores:{color_map['{reset}']} {info['cpu_cores']} (Physical), {info['cpu_threads']} (Logical)")
        lines.append(f"{color_map['{yellow}']}Memory:{color_map['{reset}']} {info['used_memory']} / {info['total_memory']} ({info['memory_percent']})")
        lines.append(f"{color_map['{blue}']}Disk:{color_map['{reset}']} {info['used_disk']} / {info['total_disk']} ({info['disk_percent']})")
        if 'uptime' in info:
            lines.append(f"{color_map['{magenta}']}Uptime:{color_map['{reset}']} {info['uptime']}")
            for net in info['network']:
                lines.append(f"  {net}")
            for gpu in info['gpu']:
                lines.append(f"  {gpu}")
            lines.append(f"{color_map['{magenta}']}Python:{color_map['{reset}']} {info['python_version']}")
            lines.append(f"{color_map['{magenta}']}Shell:{color_map['{reset}']} {info['shell']}")
    return lines

def get_ascii_art(config, use_color=True):
    custom_art_path = config['General'].get('custom_art_path', '')
    if custom_art_path and os.path.exists(custom_art_path):
        return image_to_ascii(custom_art_path, use_color, config)
    else:
        art = DEFAULT_ASCII_ART.get(platform.system(), DEFAULT_ASCII_ART['Default'])
        if not use_color:
            for key in ['{red}', '{green}', '{yellow}', '{blue}', '{magenta}', '{cyan}', '{white}', '{reset}']:
                art = art.replace(key, '')
        else:
            color_map = {
                '{red}': Colors.RED,
                '{green}': Colors.GREEN,
                '{yellow}': Colors.YELLOW,
                '{blue}': Colors.BLUE,
                '{magenta}': Colors.MAGENTA,
                '{cyan}': Colors.CYAN,
                '{white}': Colors.WHITE,
                '{reset}': Colors.RESET
            }
            for key, val in color_map.items():
                art = art.replace(key, val)
        return art.splitlines()

def image_to_ascii(image_path, use_color=True, config=None):
    try:
        ascii_char = '█'
        if config and 'General' in config:
            char = config['General'].get('ascii_char', '█')
            if char and len(char) == 1:
                ascii_char = char
        img = Image.open(image_path).convert('RGBA')
        width, height = img.size
        min_x, min_y = width, height
        max_x = max_y = 0
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                if pixel[3] > 50 and sum(pixel[:3]) > 30:
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
        if max_x > min_x and max_y > min_y:
            padding = 2
            img = img.crop((max(0, min_x - padding), max(0, min_y - padding), min(width, max_x + padding), min(height, max_y + padding)))
        width, height = img.size
        terminal_aspect_correction = 0.5
        aspect_ratio = height / width * terminal_aspect_correction
        new_width = min(40, width)
        new_height = int(aspect_ratio * new_width)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        alpha_threshold = 50
        brightness_threshold = 30
        ascii_art = []
        for y in range(new_height):
            ascii_row = ''
            last_color = None
            has_content = False
            for x in range(new_width):
                r, g, b, a = img.getpixel((x, y))
                if a < alpha_threshold:
                    ascii_row += ' '
                    continue
                brightness = (0.299 * r + 0.587 * g + 0.114 * b)
                if brightness < brightness_threshold:
                    ascii_row += ' '
                    continue
                has_content = True
                if use_color:
                    current_color = get_ansi_color_256(r, g, b)
                    if current_color != last_color:
                        ascii_row += current_color
                        last_color = current_color
                ascii_row += ascii_char
            if use_color and last_color:
                ascii_row += Colors.RESET
            if has_content:
                ascii_art.append(ascii_row)
        return ascii_art if ascii_art else ["No visible content found."]
    except Exception as e:
        return [f"Error loading image: {str(e)}"]

def get_ansi_color_256(r, g, b):
    r = max(0, min(5, r * 6 // 256))
    g = max(0, min(5, g * 6 // 256))
    b = max(0, min(5, b * 6 // 256))
    color_code = 16 + (36 * r) + (6 * g) + b
    return f"\033[38;5;{color_code}m"

def display_output(ascii_art, system_info):
    def visible_length(s):
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return len(ansi_escape.sub('', s))
    art_width = max(visible_length(line) for line in ascii_art) if ascii_art else 0
    info_start_pos = art_width + 5
    combined_output = []
    info_index = 0
    for art_line in ascii_art:
        vis_len = visible_length(art_line)
        padding = max(0, info_start_pos - vis_len)
        if info_index < len(system_info):
            combined_output.append(f"{art_line}{' ' * padding}{system_info[info_index]}")
            info_index += 1
        else:
            combined_output.append(art_line)
    while info_index < len(system_info):
        combined_output.append(f"{' ' * info_start_pos}{system_info[info_index]}")
        info_index += 1
    for line in combined_output:
        print(line)

def show_help():
    help_text = """
BetterFetch - A system information display tool
Usage: betterfetch [OPTIONS]
Options:
  -h, --help         Show this help message
  --nocolor          Disable colors
  --config           Show config file path
  --art PATH         Set custom ASCII art image
  --delete-art       Remove custom art
  --compact          Compact output
  --verbose          Verbose output
    """
    print(help_text)

def main():
    parser = argparse.ArgumentParser(description='BetterFetch - System Info Tool', add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument('--nocolor', action='store_true')
    parser.add_argument('--config', action='store_true')
    parser.add_argument('--art', metavar='PATH')
    parser.add_argument('--delete-art', action='store_true')
    parser.add_argument('--compact', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    if args.help:
        show_help()
        return

    config = load_config()

    if args.config:
        print(f"Config file: {CONFIG_FILE}")
        return

    if args.art:
        art_path = os.path.abspath(args.art)
        if os.path.exists(art_path):
            config['General']['custom_art_path'] = art_path
            with open(CONFIG_FILE, 'w') as f:
                config.write(f)
            print(f"Custom art set to: {art_path}")
        else:
            print(f"File not found: {art_path}")
        return

    if args.delete_art:
        if config['General'].get('custom_art_path', ''):
            config['General']['custom_art_path'] = ''
            with open(CONFIG_FILE, 'w') as f:
                config.write(f)
            print("Custom art removed.")
        else:
            print("No custom art configured.")
        return

    use_color = not args.nocolor and config['General'].getboolean('use_color', True)
    verbose = args.verbose or config['General'].get('default_mode', 'normal') == 'verbose'
    compact = args.compact or config['General'].get('default_mode', 'normal') == 'compact'

    system_info = get_system_info(verbose)
    formatted_info = format_system_info(system_info, compact, use_color)
    ascii_art = get_ascii_art(config, use_color)
    display_output(ascii_art, formatted_info)

if __name__ == "__main__":
    main()
