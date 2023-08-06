from . import tools as tl
import os
import csv
from . import theme
from . import task
class BenchTrack:
    '''
    This class contains the structure of the BenchTrack

    :cvar str __path:the relative path that contains the infrastructure.which is also the first parameter of input
    :cvar str __name:name of bench
    :cvar dict __dictTargets:a dictionnaire contains keys of target's name and values of object Target
    :cvar list __listThemes:a list contains of object theme
    :cvar list __allTarget:a list of all targets must be tested
    :cvar list __allTask:a list of all tasks must be tested
    :cvar str __path_benchTrack:path of BenchTrack.py
    :cvar str __outputFile:path of output.csv
    '''
    def __init__(self, path_inf, path_benchTrack):

        '''
        constructor of class BenchTrack

        :param str path_inf:the relative path that contains the infrastructure.which is also the first parameter of input
        :param str path_benchTrack : the absolu path that contains the BenchTrack.

        :return:no return

        '''
        self.__display_mode={} #three types of modes: line, tabular, histogram
        self.__path = path_inf
        self.__name = path_inf.split('/')[-1]
        self.__dictTargets={}
        self.__listThemes=[]
        self.__allTarget=[]
        self.__allTask = []
        self.__path_benchTrack = path_benchTrack
        self.__construct()
        self.__outputFile = self.__path+"/output"+tl.getDate()+".csv"
        self.__outputHtml = ""
        self.__pelican = False

    def __str__(self):
        '''
        Output list of all the themes of the infrastructure

        return str: infos of the bench

        '''
        string = self.getName()
        string += ":list Themes["
        if len(self.__listThemes) != 0:
            string += self.__listThemes[0].__str__()
        for i in range(1,len(self.__listThemes)):
            string += "," + self.__listThemes[i].__str__()
        string += "]"
        return string
    def getDisplay(self):
        return self.__display_mode
    def __construct(self):
        """
        construct all theme,target,task
        """
        path_current = ""
        file_current = ""
        try:
            path = self.__path
            path += self.__name
            path += '/tasks'
            
            path = self.__path+"/targets"
            path_current = path
            for targetName in os.listdir(path):
                file_current = targetName
                if targetName[0] == '.' :
                    continue
                self.__allTarget.append(targetName)
            path = self.__path+'/tasks'
            path_current = path
            for themeName in os.listdir(path):
                file_current = themeName
                if themeName[0] == '.' :
                    continue
                themes = theme.Theme(themeName)
                #for every task in the folder theme
                pathT = path + '/' + themeName
                path_current = pathT
                for taskName in os.listdir(pathT):
                    file_current = taskName
                    if taskName[0] == '.' :
                        continue
                    #set in the list alltask
                    if taskName not in self.__allTask:
                        self.__allTask.append(taskName)
                    pathTs = pathT+'/'+taskName +'/'
                    path_config = pathTs + 'config.ini'
                    #resd config.ini and construct task
                    sample_size = 20
                    args = ''
                    file_current = path_config
                    if os.path.exists(path_config):
                        sample_size,args,display = tl.ConfigFileTask(path_config)
                        self.__display_mode[taskName]=display
                    tasks = task.Task(taskName, tl.generateArgsList(args), sample_size)
                    for targetName in self.__allTarget:
                        if tl.existFile(targetName,pathTs):
                            tasks.addTarget(targetName)
                    themes.addTask(tasks)
                self.__listThemes.append(themes)
        except IOError:
            print("Error of path in construct")
            exit(0)
    def getName(self):
        '''
        Getter of parameter __name

        :return:name of Bench

        '''
        return self.__name

    def ToCsv(self):
        '''
        write infos of the infrastructure to csv file

        :return:no return

        '''
        with open(self.__outputFile, "w",newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["theme", "task", "target","args","run_time"])
            for theme in self.__listThemes:
                theme.ToCsv(writer)

    def getPathInf(self):
        return self.__path
    def getPathOutputFile(self):
        return self.__outputFile
    def setPathOutputHtml(self,path):
        self.__outputHtml = path
    def getPathOutputHtml(self):
        return self.__outputHtml
    def isPelican(self):
        return self.__pelican
    def setPelican(self,b):
        self.__pelican = b

    def addTargets(self,name_target,lang_target):
        '''
        Add targets at the dictionay dictTargets

        :param: str name_target:targets of the infrastructure.
        :param: str lang_target:programming languague of the target.

        :return:no return
        '''
        self.__dictTargets[name_target] = lang_target

    def __addThemes(self,theme):
        '''
        Add themes of the infrastructure to the listThemes

        :param Object_Theme theme:

        :return: no return

        '''
        self.__listThemes.append(theme)

    # execution of bench
    def exe_bench(self):
        '''
        Execution of the programme

        :return: no return

        '''
        print("Execution of "+self.__name)
        try:
            for i in range(len(self.__listThemes)):
                self.__listThemes[i].exe_theme(self.__allTask,self.__allTarget,self.__path)
        except:
            print("Error during execution")
            exit(0)

    def filter_target(self,lis,model):
        '''
        delet the target has been excluded from the command
        of user

        :param:list lis:list of targets will be excluded/included.
        :param bool model :if true, all the targets selected will be added in the list of execution.
                            else, delet those targets excluded

        :return: The number of targets to be tested

        '''
        if model:
            self.__allTarget = lis
        else:
            self.__allTarget = [x for x in self.__allTarget if x not in lis]
        return len(self.__allTarget)

    def filter_task(self,lis,model):
        '''
        delet the task has been excluded from the command
        of user

        :param list lis:list of tasks will be excluded/included.
        :param bool model:if true, all the tasks selected will be added in the list of execution.
                            else, delet those tasks excluded

        :return: no returnThe number of targets to be tested
        '''
        if model:
            self.__allTask = lis
        else:
            self.__allTask = [x for x in self.__allTask if x not in lis]
        return len(self.__allTask)

    def show_list_target(self):
        '''
        Output the list of targets that will be executed

        :return: no return

        '''
        print("List of targets:")
        for i in range(len(self.__allTarget)):
            print(self.__allTarget[i])

    def showInfoTarget(self,nomTarget):
        '''
        Output infos (readme) of the target 

        :param str nomTarget :target's name.

        :return: no return

        '''
        print("Information of " + nomTarget + " in the test " + self.__name +":")
        tl.file_read(self.__path,nomTarget,"targets")

    def showListTasks(self):
        '''
        output all the tasks that will be executed

        :return: no return

        '''
        print("List of tasks:")
        for i in range(len(self.__listThemes)):
            self.__listThemes[i].showlistTasks()

    def showInfoTask(self,nameTask):
        '''
        output info(readme) of the task

        :param str nameTask :task's name.

        :return: no return
        '''
        for i in self.__listThemes:
            if i.showInfoTask(nameTask,self.__name,self.__path):
                return 1
        print("Task "+nameTask+" doesn't exite")
        return -1

    def get_structure_tasks(self):
        '''
        get all infos of targets,tasks

        :return: the structure of the tasks
        '''
        list_structure_theme = {}
        for theme in self.__listThemes:
            list_structure_theme[theme.getName()] = theme.get_structure_tasks(self.__path)
        return list_structure_theme
