# DUMPDB-BACKUP-ROTATE

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

This python script is used to make backup copies of your databases: MySQL, Postgress, MongoDB, etc. Also with features to keep previous versions and notifications via email.

## Getting Started <a name = "getting_started"></a>


### Prerequisites

```
python 3.6 or higher
```
Optional
```
pip 
virtalenv
```

Command for Ubuntu 20.04
```
sudo apt update
sudo apt install python3-pip
pip3 install virtualenv
```

### Installing

We get source code from github!

```
git clone https://github.com/sistemasnegros/dumpdb-backup-rotate
```

With virtualenv

```
cd dumpdb-backup-rotate
virtualenv .pyenv
source .pyenv/bin/activate
```

### Config
We define our configuration in the file config.ini, example using mongodump.
```
[DEFAULT]
logPath = backup.log
debug = no
verbose = no
destinationPath = /mnt/backup/db
keepBakup = 10
nameBackup = database_${date}--${time}
prefixFolder = nosql
command = mongodump --uri="mongodb+srv://user:password@mydatabase.mongodb.net" --db=mydatabase --gzip --archive="${destinationPath}/${nameBackup}"
commandTimeout = 60

[MAIL]
enable = yes
subjectOk = Backup database Prod Ok ✔
subjectError = Backup database Prod Err ✖
from = notify@midomain.com
username = notify@midomain.com
password = *****
to = user1@othedomain.com,user2@othedomain.com
server = smtp.office365.com
port = 587
tls = yes

```


## Usage <a name = "usage"></a>

Run Manual backup
```
python3 main.py
```
Run with set file config 
```
python3 main.py -c custom_config.ini
```

Output:
```
2022-03-03 09:36:19,268 INFO: init with config config.ini
2022-03-03 09:36:19,268 INFO: Execute command mongodump --uri="myuri" --db=mydatabase --gzip --archive="/mnt/backup/database_2022-03-03--09-36-19"
2022-03-03 09:36:28,622 INFO: Command executed successfully
2022-03-03 09:36:31,217 INFO: Send email successfully

```

Structure Backup

```
mongo
├── nosql1
│   └── database_2022-03-03--09-36-19
├── nosql2
│   └── database_2022-03-03--09-34-48
├── nosql3
│   └── database_2022-03-03--09-32-37
├── nosql4
│   └── database_2022-03-03--09-27-06
├── nosql5
│   └── database_2022-03-03--08-58-10
├── nosql6
│   └── database_2022-03-03--08-56-44
├── nosql7
│   └── database_2022-03-03--08-32-58
├── nosql8

```


