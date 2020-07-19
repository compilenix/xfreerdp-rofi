# Requirements
- python 3.8+
- xfreerdp 2
  - Ubuntu: `freerdp2-x11`
  - fedora: either of
    - `https://git.compilenix.org/CompileNix/dotfiles/-/raw/master/home/bin_dotfiles/build-xfreerdp.sh`
    - dnf package `xfreerdp` or `freerdp-2:2.0.0`
- rofi
- xargs

# Installation
```bash
git clone https://git.compilenix.org/CompileNix/xfreerdp-rofi.git
cd xfreerdp-rofi
sudo ln -sfv "$PWD/xfreerdp-rofi.sh" /usr/bin/rdp-rofi
mkdir -pv "$HOME/.config/xfreerdp"
cp -v config.example.json "$HOME/.config/xfreerdp/config.json"
$EDITOR "$HOME/.config/xfreerdp/config.json"
```

# Config Reference
## Floatbar
One of:
- always
- fullscreen
- window

## ExecutableOverwride (optional)
Use this specific xfreerdp executable instead of `xfreerdp`.

## DefaultWindowSize (optional)
### w (optional)
The custom window weight in pixel.

### h (optional)
The custom window height in prixel.

## DisableSound (optional)
set to `true` if you want to disable sound redirection to your client.

## Session
### Name
Displayname of the RDP Session.

### HostName
The DNS Hostname or host ip address.

### Port (optional)
The RDP TCP port of the server.

### Domain
The Domain to logon to. If you want to perform a local user logon use "`.`" (without the quotes).

### User
The local or domain username.

### Password
The base64 encoded password.

Create with: `echo "password" | base64`

### Fullscreen (optional)
Set to `true` if you want to start the session in fullscreen.

### Network (optional)
One of:
- modem
- broadband
- broadband-low
- broadband-high
- wan
- lan
- auto

### Compression (optional)
One of:
- 0
- 1
- 2

Which level does what isn't documented by FreeRDP, so im guessing that `2` enables the strongest compression.

### Admin (optional)
Request admin (or console) session.

