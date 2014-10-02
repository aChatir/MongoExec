MongoExec

A Plugin for running Mongo commands in Sublime Text.


## Authors

* Abdelaziz CHATIR

# Installation and Configuration

## Package Control

The preferred method of installation is via Sublime Package Control.

Install Sublime Package Control

* From inside Sublime Text, open Package Control's Command Pallet: CTRL SHIFT P (Windows, Linux) or CMD SHIFT P on Mac.
* Type install package and hit Return. A list of available packages will be displayed.
* Type MongoExec and hit Return. The package will be downloaded to the appropriate directory.
* Restart Sublime Text to complete installation.

## Manual Installation

Download or clone this repository to a directory MongoExec in the Sublime Text Packages directory for your platform:

* Mac: git clone git@github.com:kalo7791/MongoExec.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/MongoExec
* Windows: git clone git@github.com:kalo7791/MongoExec.git %APPDATA%\Sublime/ Text/ 3/\MongoExec
* Linux: git clone git@github.com:kalo7791/MongoExec.git ~/.Sublime\ Text\ 3/Packages/MongoExec
* Restart Sublime Text to complete installation.

# Configuration
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
[Inspired and Based on](http://lubriciousdevelopers.github.io/projects/sublime-sql-exec/)

