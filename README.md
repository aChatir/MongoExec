MongoExec
=========

A Plugin for running Mongo commands in Sublime Text.


## Authors
----------

* Abdelaziz CHATIR

# Usage:
--------

![mongoexec screenshot](https://github.com/aChatir/MongoExec/raw/master/mongoexec.gif)

# Commands Available:
---------------------
1. [Ctrl+Alt+w]    => List all databases.
2. [Ctrl+w Ctrl+c] => List all collections.
3. [Ctrl+w Ctrl+w] => Execute a selected querie.
4. [Ctrl+w Ctrl+h] => List Queries history.
5. [Ctrl+w Ctrl+q] => Execute a specific query.
6. [Ctrl+w Ctrl+f] => Execute a specific file (js).
7. [Ctrl+w Ctrl+v] => Execute a specefic view (from sublime even if not saved).

## How to Install

### Package Control *(Recommended)*

1. Package Control: **Install Package** `MongoExec`
2. **Restart** Sublime Text

### Git

1. **Clone** to your packages folder `git clone git@github.com:aChatir/MongoExec.git`
2. **Restart** Sublime Text

### Download

1. **Download** this **[ZIP file](https://github.com/aChatir/MongoExec/archive/master.zip)**
2. Move to packages folder *(In the **Sublime Text 3** menu → **Preferences** → **Browse Packages…**)*
3. **Restart** Sublime Text

# Configuration
---------------

Settings
--------

'Preferences' -> 'Package Settings' -> 'MongoExec'

```json
{
    "mongo_exec.commands": {
        "mongo" : "/usr/bin/mongo"
    },
    "connections": {
        "Localhost": {
            "type"    : "mongo",
            "host"    : "localhost",
            "port"    : "27017",
            "username": "",
            "password": "",
            "databases": ""
        }
    }
}
```


Inspired and Based on [SQLExec](https://sublime.wbond.net/packages/SQLExec)

