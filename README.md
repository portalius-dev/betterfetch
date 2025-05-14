<div style="text-align:center">
<img src="https://github.com/portalius-dev/betterfetch/blob/main/readme/mainLogo.png?raw=true" alt="BetterFetch Logo" width="400"/>
</div>

---

## 🚀 About BetterFetch

BetterFetch is an enhanced recreation of **NeoFetch**, a command-line system information tool that displays comprehensive details about your system hardware and software configuration.

### Key Improvements:
1. **Advanced Customization** - Personalize output appearance and information
2. **Extended System Details** - More comprehensive hardware/software information
3. **Custom ASCII Art** - Convert your own PNG/JPG images into ASCII art displays
4. **Easter Eggs** - Fun hidden features to discover

---

## 📥 Installation Guide

### Linux (Debian/Ubuntu)
```bash
sudo apt update && sudo apt install betterfetch-linux
```

### Linux (Arch-based)
```bash
sudo pacman -S betterfetch
```

### Manual Installation (All Linux)
```bash
git clone https://github.com/portalius-dev/betterfetch.git
cd betterfetch
make
sudo make install
```

### Windows
1. Download the latest `.exe` installer from [Releases](https://github.com/portalius-dev/betterfetch/releases)
2. Run the installer
3. Launch from Command Prompt/PowerShell

---

## 🛠 Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `betterfetch` | Show default system info | `betterfetch` |
| `--help` | Display all available commands | `betterfetch --help` |
| `--nocolor` | Display output without colors | `betterfetch --nocolor` |
| `--config` | Show config file location | `betterfetch --config` |
| `--art [path]` | Use custom image as ASCII art | `betterfetch --art ~/Pictures/my_logo.png` |
| `--compact` | Show compact output format | `betterfetch --compact` |
| `--verbose` | Show detailed system information | `betterfetch --verbose` |

---

## 🖼 Custom ASCII Art

To create custom ASCII art displays:
1. Prepare a PNG/JPG image (simpler images work best)
2. Run:

   ```bash
   betterfetch --art path/to/your/image.png
   ```
3. The image will be automatically converted and saved for future use

---

## 🐛 Reporting Issues

Found a bug? Please open an issue on our [GitHub repository](https://github.com/portalius-dev/betterfetch/issues) with:
- Your system information
- Steps to reproduce
- Expected vs actual behavior

---

## 📜 License

BetterFetch is released under the GNU General Public License v3.0. See [LICENSE](https://github.com/portalius-dev/betterfetch/blob/main/LICENSE) for details.
