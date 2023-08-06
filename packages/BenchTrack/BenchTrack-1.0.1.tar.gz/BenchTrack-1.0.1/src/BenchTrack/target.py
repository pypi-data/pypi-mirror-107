from . import tools as tl

class Target:
    """
    This class contains the structure of the Target

    :cvar str __Name :name of the target.
    :cvar dict __result:a dictionnaire contains keys of parameter and values of result
    """
    def __init__(self,name):
        """
        Constructor of class Target

        :param str name :name of the Target.

        """
        self.__name =name
        self.__result = {}

    def getName(self):
        """
        get name of the task

        :return:name of the task.

        """
        return self.__name

    def getResult(self):
        """
        get result of the target

        :return:the dictionnaire of result.

        """
        return self.__result

    def addResult(self,arg,value):
        """
        add a result of test

        :param str arg:the parameter of test
        :param float value:the result

        """
        self.__result[arg] = value

    def exe_before_test(self, themeName,task, path,args):
        """
        execute some before-task file like imports

        :param str themeName:name of theme
        :param str task:name of task
        :param str path :path of the infrastructure
        :param str args:args of execution

        """
        path_File = path  + "/tasks/" + themeName + "/" + task
        path_ConfigFile = path  + "/targets/" + self.getName() + "/config.ini"
        if tl.existFile("before_"+self.getName(),path_File):
            self.exe_file(path_ConfigFile, path_File,args,self.getName()+"_before")

    def exe_target(self, themeName, task,path,args):
        """
        drive infos from configure file of target and transforme these infos

        :param str themeName:name of theme
        :param str task:name of task
        :param str path :path of the infrastructure
        :param str args:args of execution

        """
        path_ConfigFile = path  + "/targets/" + self.getName() + "/config.ini"
        path_File = path  + "/tasks/" + themeName + "/" + task
        self.exe_file(path_ConfigFile, path_File,args,self.getName()+"_run")

    def exe_file(self, path_configFile, path_file, args,target):
        """
        execution of a target

        :param str path_configFile:path of file config of target
        :param str path_file:file to execute
        :param str args:args of execution
        :param str target :name of target

        """
        command, language = tl.ConfigFileTarget(path_configFile)
        tl.exeCmd(path_file, args, command, language,target)