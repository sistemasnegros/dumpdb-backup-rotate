# /bin/python3
import logging
import argparse
import sys
from config import Config
from log import Log
import subprocess
import os
import shutil
import shlex

from mail import Mail


def notify(config, typeSubject, outCommandAll):
    if(config.mail["enable"] == "yes"):
        mail = Mail(**config.mail)

        with open(config.logPath, encoding='utf-8') as logfile:
            body = logfile.read() + ("\n Output: \n") + outCommandAll

            mail.send(subject=config.mail[typeSubject], body=body, **config.mail)
            logging.info("Send email successfully")
        return

    logging.info("Sending mail is not enabled in the configuration")


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="show all output", action="store_true")
    parser.add_argument("-d", "--debug", help="show enbale debug all output", action="store_true")     
    parser.add_argument("-c", "--config", help="set path the file config", default="config.ini")

    arguments = parser.parse_args()
    config = Config(arguments)
    Log(config)
    logging.info("init with config %s" % arguments.config)

    if (not os.path.exists(config.destinationPath)):
        logging.error("DestinationPath not exists")
        notify(config, "subjectError", "")
        sys.exit(1)

    logging.debug("Execute command %s" % config.command)

    sp = subprocess.Popen(shlex.split(config.command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        outCommand, outCommandErr = sp.communicate(timeout=config.commandTimeout)
    except subprocess.TimeoutExpired:
        logging.error("Executed command timeout out")
        sp.kill()
        outCommand, outCommandErr = sp.communicate()

    isSuccessCommand = sp.returncode == 0
    outCommandAll = outCommand.decode() + "\n" + outCommandErr.decode()

    if not isSuccessCommand:
        logging.error("Error executing command")
        logging.error(outCommandAll)

    if isSuccessCommand:
        logging.info("Command executed successfully")

    backupCreated = config.destinationPath + "/" + config.nameBackup
    if (not os.path.exists(backupCreated)):
        logging.error("Backup file is not available")
        notify(config, "subjectError", outCommandAll)
        sys.exit(1)

    lastBackupPath = config.destinationPath + "/" + config.prefixFolder + str(config.keepBakup - 1) + "/"
    #  delete lastest folder rotation
    if (os.path.exists(lastBackupPath)):
        shutil.rmtree(lastBackupPath)

    rangeRotation = range(0, config.keepBakup - 1)

    for numBackup in reversed(rangeRotation):
        nameBackup = config.destinationPath + "/" + config.prefixFolder + str(numBackup)

        if (not os.path.exists(nameBackup)):
            os.mkdir(nameBackup)

        newNameBackup = config.destinationPath + "/" + config.prefixFolder + str(numBackup + 1)

        os.rename(nameBackup, newNameBackup)

    firstBackupPath = config.destinationPath + "/" + config.prefixFolder + str(1) + "/"
    shutil.move(backupCreated, firstBackupPath)

    notify(config, "subjectOk", outCommandAll)


if __name__ == "__main__":
    main()
