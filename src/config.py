# -*- coding: utf-8 -*-

import configparser
import re
import time
import datetime


class Config(object):
    def __init__(self, arguments):
        self.dateNow = str(datetime.date.today())
        self.timeNow = str(time.strftime("%H-%M-%S"))

        self.configLoaded = configparser.ConfigParser()
        self.configLoaded.read(arguments.config)
        configGeneral = self.configLoaded["DEFAULT"]

        self.debug = configGeneral.getboolean("debug", fallback=False)
        
        if (arguments.debug):
            self.debug = True
        
        self.verbose = configGeneral.getboolean("verbose", fallback=True)
        if (arguments.verbose):
          self.verbose = True  
  
        self.nameBackup = self.replaceVarInconfig("nameBackup")
        self.command = self.replaceVarInconfig("command")

        self.keepBakup = configGeneral.getint("keepBakup", fallback=5)
        self.destinationPath = configGeneral["destinationPath"]

        self.logPath = configGeneral["logPath"]
        self.prefixFolder = configGeneral["prefixFolder"]

        self.mail = self.configLoaded["MAIL"]
        self.commandTimeout = configGeneral.getint("commandTimeout", fallback=15)

    def replaceListVar(self, varValue):
        # Regex get %{string}
        regex = re.compile(r'\$\{([a-z, A-Z]{1,20})\}')
        listVars = regex.findall(varValue)
        for field in listVars:
            if(field == "date"):
                varValue = self.replaceStr(varValue, field, self.dateNow)
                continue

            if(field == "time"):
                varValue = self.replaceStr(varValue, field, self.timeNow)
                continue

            newValue = self.configLoaded.get("DEFAULT", field)
            varValue = varValue.replace("${%s}" % field, newValue)

        serchMoreVar = regex.findall(varValue)
        if serchMoreVar:
            return self.replaceListVar(varValue)

        return varValue

    def replaceVarInconfig(self, option):
        varValue = self.configLoaded.get("DEFAULT", option)
        varValue = self.replaceListVar(varValue)
        return varValue

    def replaceStr(self, value, field, newValue):
        return value.replace("${%s}" % field, newValue)
