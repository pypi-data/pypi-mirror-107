from . import tools as tl
import os
from . import target
class Task:
    """
    This class contains the structure of the Task

    :cvar str __Name :name of the task.
    :cvar str __args :parameters of the task.
    :cvar int __sample_size :optional,the times of execution. The default is 20.
    :cvar dict __dictTargets:a dictionnaire contains keys of target's name and values of object Target
    """
    def __init__(self, name, args, sample_size=20):
        """
        Constructor of class Task

        :param str name :name of the task.
        :param str args :parameters of the task.
        :param int sample_size :optional,the times of execution. The default is 20.

        :return: no return

        """
        self.__Name = name
        self.__dictTargets = {}
        self.__sample_size = int(sample_size)
        self.__args = args



    def __str__(self):
        """
        Return a string of all the targets from the task

        :return: stirng:all the targets from the task.

        """
        string = self.getName() + "["
        for i,_ in self.__dictTargets:
            string += i + " "
        return string + "]"

    def addTarget(self, name_Target):
        '''
        Add targets to targets dictionary of the task

        param str name_Target :name of target.

        '''
        self.__dictTargets[name_Target] = target.Target(name_Target)

    def modifyTarget(self, name_Target, res_Target):
        """
        Add execution time of targets of the task

        :param str name_Target :the target.
        :param float res_Target : execution time.

        :return: no return

        """
        self.__dictTargets[name_Target] = res_Target

    def exe_task(self, lis, themeName, path):
        """
        Execution of the tasks

        :param list lis :list of targets.
        :param str themeName : name of theme of the task.
        :param str path :the path contains the theme

        :return: no return

        """
        print("-In Task " + self.getName() + ":")
        for target_name,target in self.__dictTargets.items():
            if target_name in lis:
                # try :
                #     self.__dictTargets[self.__args[0]].exe_target(themeName, self.getName(), path)
                # except ModuleNotFoundError:
                #     self.upgrade_for_target(path,target)
                for arg in self.__args:
                    # time to execute before_test
                    times_before = tl.time.time()
                    for _ in range(self.__sample_size):
                        target.exe_before_test(themeName, self.getName(), path,arg)
                    times_before = tl.time.time() - times_before

                    # time to execute test
                    start = tl.time.time()
                    for _ in range(self.__sample_size):
                        target.exe_target(themeName, self.getName(), path,arg)
                    time_mean = (tl.time.time() - start - times_before) / self.__sample_size
                    self.__dictTargets[target_name].addResult(arg,time_mean)
                    print("--execute target " + target_name + ' ' + self.__sample_size.__str__() + ' times with arg:' + arg)
                    print("Execution time:" + time_mean.__str__())

    def getName(self):
        '''
        get name of the task

        :return:name of the task.

        '''
        return self.__Name

    def ToCsv(self, writer, theme):
        '''
        generetor the csv file which contains some
        infos about results of execution

        '''
        targetNames = dict.keys(self.__dictTargets)
        for target in targetNames:
            result = self.__dictTargets[target].getResult()
            for arg in self.__args:
                if arg in result:
                    run_time = result[arg]
                    writer.writerow([theme, self.__Name, target,arg, run_time])

    def get_structure_tasks(self,path):
        """
        get targets of tasks

        :return: list_target : TYPE DESCRIPTION.

        """
        list_target=[]
        for target in list(self.__dictTargets.keys()):
            path_configFile = path + "/targets/" + target + "/config.ini"
            if os.path.exists(path_configFile):
                command, language = tl.ConfigFileTarget(path_configFile)
                target += "_run"+tl.get_suffixe(language)
                list_target.append(target)
        return list_target

    def upgrade_for_target(self,path,target):
        """

        """
        path_ConfigFile = path  + "/targets/" + target + "/config.ini"
        config = tl.ConfigParser()
        config.read(path_ConfigFile)
        upgrade = config.get('execution', 'upgrading')
        os.system(upgrade)