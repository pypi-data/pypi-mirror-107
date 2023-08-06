import datetime
from configparser import ConfigParser
import os
import re
import time
import csv

def execute(path, cmd):
    '''
    This fonction is made to run  files

    :param str path :the path that contains the task need to be execute.
    :param str cmd :command of executing based on terminal.
    '''
    CurrentPath = os.getcwd()
    PathAbsolu = CurrentPath + "/" + path+"/"

    os.chdir(PathAbsolu)
    #res = os.system("cd"+path+"&&"+cmd)
    res=os.system(cmd)
    # if res != 0:
    #     if os.path.exists('../errorInfo.txt'):
    #         with open('../errorInfo.txt', mode='w', encoding='utf-8') as ff:
    #             #print(ff.read())
    #             ff.write(str(res))
    #     else:
    #         with open("../errorInfo.txt", mode='w+', encoding='utf-8') as ff:
    #             #print(ff.read())
    #             ff.write(str(res))

    os.chdir(CurrentPath)

def exeCmd(path,parameter,cmd,language,target):
    """
    exeCmd is a fonction that switch the task to
    other specific fonction to execute them

    :param str path : the path that contains the task need to be execute.
    :param str parameter : the parameter of the task.
    :param str cmd : command of executing based on terminal.
    :param str language : the programming languague of task .
    :param str target: the name of target

    """
    target += get_suffixe(language)
    new_cmd=cmd.replace("{script}",target)
    new_cmd2=new_cmd.replace("{arg}",parameter)
    try:
        execute(path,new_cmd2)
    except ImportError:
        print("ModuleNotFoundError")
    # except:
    #     print("Error for execution")
    return True

def get_suffixe(language):
    """
    This method return the suffixe of programming language

    :param str language:language to get a suffixe

    :return: suffixe of the fichier in language input
    """
    if language == "python":
        return ".py"
    if language == "r":
        return ".r"

def ConfigFileTarget(path_target):
    """
    This method trait configure file and return their command and
    programming language of the target.


    :param str path_target:path of the config.ini for the target

    :return:run:the command of executing the target
            language:the programming language of the target
    """
    config = ConfigParser()
    config.read(path_target)
    language = config.get('execution', 'language')
    run = config.get('execution', 'run')
    return run,language

def ConfigFileTask(file):
    """
    This method trait configure file of task and return their sample_size and
    parameters of the task.

    :param str file:path of the the config.ini for the task

    :return:sample_size:sample size for execute all targets in this task
           :arg:all args of the target
    """
    try:
        config = ConfigParser()
        config.read(file)
        sample_size = config.get('running', 'sample_size')
        if config.has_option('running', 'display'):
            display_mode = config.get('running', 'display')
        else:
            display_mode = 'tabular'
        if config.has_option('running', 'args'):
            arg = config.get('running', 'args')
        else:
            arg = ''
        return sample_size,arg,display_mode
    except IOError:
        print("Can't find the file config:" + file)

# pour trouver tous les fichers de repertoire de BASE.
def find_all_file(base):
    """
    Find all files in base

    :param str base : the system path.

    :yield str f : all files found in base.

    """
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f


def existFile(fileName, path):
    """
    To test if a Path contain a file

    :param str fileName:name of the file
    :param str path:the path that contains the file

    :returns:bool:True for Found a file name filename in path
                    esle False
    """
    for files in os.listdir(path):
        if re.match(fileName,files):
            return True
    return False



def exe_python(target_name):
    '''
    for calculating time of executing of python file
    Parameters :
        target_name:path et nom pour target
    :returns :temp d'execution
    '''
    start = datetime.datetime.now()
    print("Test " + target_name + " start")
    os.system("python " + target_name)
    timeUsed = (datetime.datetime.now() - start).microseconds * 1e-6
    print("Test " + target_name + " finished using time:" + timeUsed.__str__())
    return timeUsed


def to_txt(list_res):
    '''
    Turns the results to txt file

    Parameters
    ----------
    list_res : float list 
        time of executing.

    '''
    with  open('PGM/result.txt', 'w') as f:
        for i in list_res:
            f.write(i.benchName + '\n')
            for target in i.listTargets:
                f.write(target)
            f.write('\n')
            for targetTime in i.listTemps:
                f.write(targetTime.__str__() + '\n')
            f.write('|' + '\n')
        f.close()


# print a file
def file_read(nameTest, nameTarget, typeF):
    '''
    To read readme file and print the contents

    Parameters
    ----------
    nameTest : string
        name of task.
    nameTarget : string
        name of target.
    typeF : string
        task/target.

    :return:int:succeded print the content of readme.

    '''
    for files in os.listdir(nameTest):
        if files == typeF:
            file_dir = nameTest + "/" + files
            for files_sous in os.listdir(file_dir):
                if files_sous == nameTarget and files_sous!=".DS_Store":
                    filesRead = nameTest + "/" + typeF + "/" + nameTarget + "/" + "README.rst"
                    with open(filesRead, 'r') as f:
                        content = f.read()
                        print("==============")
                        print(content)
                        print("==============")

                        return 1
                if existFile(files_sous, file_dir):
                    dir = file_dir + "/" + files_sous
                    if dir!=".DS_Store":
                        for file_task in os.listdir(dir):
                            if file_task == nameTarget:
                                filesRead = nameTest + "/" + typeF + "/" + files_sous + "/" + file_task + "/" + "README.rst"
                                with open(filesRead, 'r') as f:
                                    content = f.read()
                                    print("==============")
                                    print(content)
                                    print("==============")
                                    return 1


def flagTasks(argv, bench, flag):
    '''
    gestion of flags of the tasks

    :param str argv :name of the benchmark.
    :param str bench :name of bench for testing.
    :param str flag : type of flags.
    '''
    if flag == 'info':
        if len(argv) < 3:
            print('Without' + 'parameter')
            return - 1
        bench.showInfoTask(argv[1])
    if flag == 'list':
        if len(argv) < 2:
            print('Without a parameter')
            return -1
        bench.showListTasks()
    if flag == 'include':
        list_Include = argv[1].split(',')
        bench.filter_task(list_Include, True)

    if flag == 'exclude':
        list_Exclude = argv[1].split(',')
        bench.filter_task(list_Exclude, False)


def flagTargets(argv, bench, flag):
    '''
    gestion of flags of the targets


    :param str argv : name of the benchmark.
    :param str bench : name of bench for testing.
    :param str flag : type of flags.
    '''

    if flag == 'info':
        if len(argv) < 3:
            print('Without' + str((3 - len(argv)).__init__()) + 'parameter')
            return -1
        bench.showInfoTarget(argv[1])
    if flag == 'list':
        if len(argv) < 2:
            print('Without a parameter')
            return -1
        bench.show_list_target()
    if flag == 'include':
        list_Include = argv[1:len(argv) - 1]
        bench.filter_target(list_Include, True)

    if flag == 'exclude':
        list_Include = argv[1:len(argv) - 1]
        bench.filter_target(list_Include, False)

def generateArgsIter(listIter):
    argsIter = []
    begin = listIter[0]
    end = listIter[1]
    step = listIter[2]
    if step > 0:
        while begin <= end:
            argsIter.append(begin.__str__())
            begin += step
    else:
        while begin >= end:
            argsIter.append(begin.__str__())
            begin += step
    return argsIter

def generateAgrs2D(list2D):
    args = [""]
    for listArgs in list2D:
        aux = []
        for i in listArgs:
            for j in args:
                aux.append(j+' '+str(i))
        args = aux
    return args

def generateArgsList(string):
    '''
    gernerate the list of args from a string

    :param str string : string of args from config.

    :return list:list of all args
    '''
    if '*' in string:
        str_args = []
        list_args_2d = []
        string = string.split('*')
        for i in string:
            str_args.append(i.strip(' ( )'))
        for i in str_args:
            if ':' in i:
                if '.' in i:
                    aux = list(map(float, i.split(':')))
                else:
                    aux = list(map(int, i.split(':')))
                list_args_2d.append(generateArgsIter(aux))
            else:
                list_args_2d.append(i.split(','))
        return generateAgrs2D(list_args_2d)
    elif ':' in string:
        print(string)
        aux= list(map(int,string.strip(' ()').split(':')))
        return generateArgsIter(aux)
    else:
        return string.split(',')

def getDate():
    return str(datetime.date.today())


def manage_flag(argv,bench):
    """

    This function manage all flags,
    with a flag for show a list or the information,this function call a function to show that
    with a flag include or exclude,this function change the object bench
    without flag,return 1

    :param argv:args Bench:l'object BenchTrack

    """
    for i in range(len(argv)):
        if "--target-include" == argv[i]:
            flagTargets(argv[i:],bench,"include")
        if "--target-exclude" == argv[i]:
            flagTargets(argv,bench,"exclude")
        if "--target-list" == argv[i]:
            flagTargets(argv[i:],bench,"list")
            return 0
        if "--target-info" == argv[i]:
            flagTargets(argv[i:],bench,"info")
            return 0

        if "--task-include" == argv[i]:
            flagTasks(argv[i:],bench,"include")
        if "--task-exclude" == argv[i]:
            flagTasks(argv[i:],bench,"exclude")
        if "--task-list" == argv[i]:
            flagTasks(argv[i:],bench,"list")
            return 0
        if "--task-info" == argv[i]:
            flagTasks(argv[i:],bench,"info")
            return 0
        if "--output" == argv[i]:
            bench.setPathOutputHtml(argv[i+1])
        if "--pelican" == argv[i]:
            bench.setPelican(True)

    return 1

def checkInfrastructure():
    pass

def help():
    print("Commande format:benchTrack [Option] path_infrastructure\n\
    Option flag:\n\
	––target-list :Show the list of targets\n\
	––task-list :Show the list of tasks\n\
	––target-info TOTO :Show the information from readme.rst of target\n\
	––task-info A :Show the information from readme.rst of task\n\
	––targets-include TOTO,TITI :Execut only the selected target\n\
	––tasks-include A,B,C :Execut only the selected task\n\
	––targets-exclude TOTO,TITI :Execut all the task except for the selected target\n\
	––tasks-exclude A,B,C :Execut all the task except for the selected task\n\
	––check :Check le format de l’infrastructure\n\
    \t--output path : Generate the output file site in the folder\n\
    \t--pelican:Save the ficher pelican\n\
          ")
def checkInfrastructure(path_infras):
    retval=os.getcwd()
    infras=retval+"/"+path_infras
    os.chdir(infras)
    if not os.path.exists("readme.rst"):
        print("no readme at your infrastrature file")
        return False

    target_path=infras+"/targets"
    task_path=infras+"/tasks"
    os.chdir(target_path)
    for files_sous in os.listdir(target_path):
        if files_sous!=".DS_Store":
            files_sous_path=target_path+"/"+files_sous
            os.chdir(files_sous_path)
            if not os.path.exists("readme.rst"):
                print("it lack at least one readme file at your targets files,please check it ")
                return False
            if not os.path.exists("config.ini"):
                print("it lack at least one configuration file at your targets files,please check it")
                return False
                
        os.chdir(target_path)
    os.chdir(infras)
    os.chdir(task_path)
    for files_sous in os.listdir(task_path):
        if files_sous!=".DS_Store":
            files_sous_path=task_path+"/"+files_sous
            os.chdir(files_sous_path)
            for files_subs in os.listdir(files_sous_path):
                if files_subs!=".DS_Store":
                    files_subs_path=files_sous_path+"/"+files_subs
                    os.chdir(files_subs_path)
                    if not os.path.exists("readme.rst"):
                        print("it lack at least one readme file at your tasks files,please check it")
                        return False
                    if not os.path.exists("config.ini") :
                        print("it lack at least one configuration file at your tasks files,please check it ")
                        return False                    
                    if not os.path.exists("config.ini") or not os.path.exists("data") or not os.path.exists("readme.rst"):
                        print("it lack at least one data file at your tasks files,please check it")
                        return False                        
                os.chdir(files_sous_path)
        os.chdir(task_path)
    os.chdir(retval)
    return True






