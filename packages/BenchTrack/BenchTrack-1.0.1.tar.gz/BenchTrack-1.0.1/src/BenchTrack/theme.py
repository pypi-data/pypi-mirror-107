from . import tools as tl
#theme

class Theme:
    '''
    This class contains the structure of the theme of Task

    :cvar str __themeName:name of the theme
    :cvar list __listTasks: list of object task in the theme
    '''
    def __init__(self,name):
        '''
        construtor of the class theme

        :param str name :name of the theme.

        :return: no return

        '''
        self.__themeName = name
        self.__listTasks = []

    def __str__(self):
        '''
        get the string that contains all the tasks of the theme.

        :return: string : string a string that contains all the tasks of the theme.

        '''
        string = self.getName()
        string += "["+self.__listTasks[0].__str__()
        for i in range(1,len(self.__listTasks)):
            string += "," + self.__listTasks[i].__str__()
        string += "]"
        return string

    def addTask(self,task):
        '''
        add task to the listTasks of the theme

        :param Object_Task task:the task to add

        :return:no return

        '''
        self.__listTasks.append(task)
    def getName(self):
        '''
        getter of parameter Name of the theme

        :return: string:name of the theme

        '''
        return self.__themeName

    def exe_theme(self,listTask,listTarget,path):
        '''
        execution of the theme

        :param list listTask :all the tasks of the theme.
        :param list listTarget :all the targets of the task in the theme.
        :param str path :the path contains the theme.

        :return: no return

        '''
        print("\nIn theme " + self.getName() + ":")
        for i in range(len(self.__listTasks)):
            if self.__listTasks[i].getName() in listTask:
                self.__listTasks[i].exe_task(listTarget,self.__themeName,path)

    def showlistTasks(self):
        '''
        Output the list of tasks of the theme

        :return: no return

        '''
        print("In the theme " + self.getName() + ",there are tasks:")
        for i in self.__listTasks:
            print(i.getName())
    def showInfoTask(self,nameTask,nameTest,path):
        '''
        Output the Info(readme) file of the task in the theme

        :param str nameTask :name of task
        :param str nameTest : name of the Bench
        :param str path : the path contains the theme.

        :return: no return
        '''
        for i in self.__listTasks:
            if i.getName() == nameTask:
                tl.file_read(path,nameTask,'tasks')
                return 1
    def ToCsv(self,writer):
        '''
        To write list of tasks of the theme in csv file

        Returns
        -------
        None.

        '''
        for task in self.__listTasks:
            task.ToCsv(writer,self.__themeName)

    def get_structure_tasks(self,path):
        '''
        Get the structure of every task

        :param str path :the path of the infrastructure

        :return: a dictionnaire
        '''
        list_structure_task = {}
        for task in self.__listTasks:
            list_structure_task[task.getName()] =task.get_structure_tasks(path)
        return  list_structure_task

