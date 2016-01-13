# TypogrArtlebedev
Typorgaph prugin for [Sublime Text](http://www.sublimetext.com/) by Artlebedev typograph [web-sercice](http://www.artlebedev.ru/tools/typograf/webservice/)

## Installation

### Manually

Go to your Packages subdirectory:

* Windows: `%APPDATA%\Sublime Text 3\Packages`
* OS X: `~/Library/Application Support/Sublime Text 3/Packages`
* Linux: `~/.config/sublime-text-3/Packages`
* Portable `Installation: Sublime Text 3/Data/Packages`

Then clone this repository:

```
git clone https://github.com/nim579/TypogrArtlebedev.git
```

That's it!

### Package Control

*Comming soon...*

## Useage

You can use plugin from "Command Palette", context menu (right click, Typogr Artlebedev) or bing key for useage.

## Options

### Key bindings

Go to `Preferences > Package Settings > Typogr Artlebedev > Key bindings - User`, and set keys:

```
[
    {
        "keys": ["ctrl+shift+t"],
        "command": "typogr_artlebedev",
        "args": {...}
    }
]
```

Arguments (see on Artlebedev site):
* **text_encoding** — encoding. Default UTF-8
* **entity_type** — number of type for special symbols. Default — 1 (HTML)
* **use_br** — user \<br\> (1 or 0). Default 0
* **use_p** — user \<p\> (1 or 0). Default 0
* **max_nobr** — maximum characters for no breaking (count). Default 3

### Settings

Sets default arguments.

Go to `Preferences > Package Settings > Typogr Artlebedev > Settings`, and set settings.
