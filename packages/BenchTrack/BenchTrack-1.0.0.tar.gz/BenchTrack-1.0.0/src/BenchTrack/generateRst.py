"""
-----------------------------------------------generateRst---------------------------------------------------
This module contains all functions to generate rst files for the content directory

"""

import matplotlib.pyplot as plt


def meta_data():
    """
    This function writes the string that contains all the metadata

    Parameters
    ----------
        Nothing
    Returns
    -------
        Nothing
    """
    md = "\n"
    md = "\n"
    md += ":authors: Benchtrack\n"
    md += ":date: 2010-10-03 10:20\n"
    md += "\n"
    return md

def create_rst_base(readme, title_rst):
    """
    This function generates the beginning of the rst files, it manages the titles

    Parameters
    ----------
        readme : String, the content of a readme file
        title_rst: String, title of the rst file
    Returns
    -------
        base_rst: String, the beginning of the rst file 
    """
    base_rst = ""
    # For file text without \n: 
    one_line = True

    for i in range(len(readme)):
        if readme[i] == '\n':
            one_line = False
            if readme[i+1] == '#' or readme[i+1] == '=':
                base_rst = readme
                j = i + 1
                while readme[j] =='#' or readme[j] == '=':
                    j += 1
                base_rst = base_rst[:j] + meta_data() + base_rst[j:]
                break
            else:
                title = title_rst + " [Automatic]\n"
                base_rst += title
                nb_carac = len(title)
                for i in range(nb_carac-1):
                    base_rst += "="
                base_rst += "\n"
                base_rst += meta_data()
                base_rst += readme
                break

    if one_line:
        title = title_rst + " [Automatic]\n"
        base_rst += title
        nb_carac = len(title)
        for i in range(nb_carac-1):
            base_rst += "="
        base_rst += "\n"
        base_rst += meta_data()
        base_rst += readme

    return base_rst

def create_graph (name_task, structure_run_time, list_target, path_images, display, name_target="targets"):
    """   
    Create graph of run time for task page, either barchart or curve depends of display

    Parameters
    ----------
        name_task : String, name of the task
        structure_run_time: Dictionary 3D [task][target][arg]
        list_targets: String, list of the targets
        path_images: String, absolute path of images
        display: String, the type of display
        name_target: 

    Returns
    -------
        path_relative_file: String, relative path to content of graph file
    """

    fig, ax = plt.subplots()

    for target in list_target:
        list_args = list(structure_run_time[name_task][target].keys())
        list_number = True
        for i in range (len(list_args)):
            list_args[i] = list_args[i].replace(" ","-")
            if not list_args[i].isdigit():
                list_number = False

        if list_number:
           list_args = list(map(int, list_args))

        list_runTime = list(structure_run_time[name_task][target].values())
        list_runTime = list(map(float, list_runTime))
        if display == "line":
            ax.plot(list_args,list_runTime, label = "Target: "+target)
        if display == "bar":
            ax.bar(list_args,list_runTime, label = "Target: "+target)
        

    ax.set_ylabel('run_time(s)')
    ax.set_title('Time execution of ' + name_task + ' by '+ name_target+' by args')
    ax.legend()

    if name_target == "targets":
        name_file = name_task
    else:
        name_file = name_task +"X" + name_target
    path_file = path_images + "/" + name_file + "_graph.jpg"
    plt.savefig(path_file, dpi=90)
    path_relative_file = "images/" +  name_file + "_graph.jpg"

    return path_relative_file

def create_infra_rst(name_infra, path_content, path_readme, structure_run_time, list_targets):
    """
    Write the rst file of the infrastructure presentation and the summary of results    
    
    Parameters
    ----------
        name_infra : String, name of the infrastructure
        path_content: String, absolute path of the content directory
        path_readme: String, absolute path of the corresponding readme file
        structure_run_time: Dictionary 3D [task][target][arg]
        list_targets: String, list of the targets
    Returns
    -------
        Nothing
    """
    readme = ''
    with open(path_readme,'r') as f:
        readme = f.read()

    path_file = path_content+ "/" +name_infra+ ".rst"

    with open(path_file,'w') as f:

        f.write(create_rst_base(readme, name_infra))

        f.write("\n")
        f.write("\n")

        f.write(".. list-table:: \n")
        f.write("   :widths: auto\n")
        f.write("   :header-rows: 1\n")
        f.write("   :stub-columns: 1\n")
        f.write("\n")
        f.write("   * - Tasks/Targets\n")
        for target in list_targets:
            f.write("     - `"+target+" <{filename}/targets/"+target + ".rst>`__ \n")

        problem_exec = False

        for task in list(structure_run_time.keys()):
            f.write("   * - `"+task+" <{filename}/tasks/"+task + ".rst>`__ \n")
            for target in list(structure_run_time[task].keys()):
                if len(list(structure_run_time[task][target].keys())) == 0:
                    f.write("     - .. image:: {static}/images/rect_orange.png \n")
                    f.write("          :target: {filename}/targetsXtasks/"+target+"X"+task+".rst \n")
                    f.write("          :alt: image orange rectangle \n")
                else:
                    for arg in list(structure_run_time[task][target].keys()):
                        if structure_run_time[task][target][arg] == -2:
                            problem_exec = True
                            f.write("     - .. image:: {static}/images/rect_red.png \n")
                            f.write("          :target: {filename}/targetsXtasks/"+target+"X"+task+".rst \n")
                            f.write("          :alt: image red rectangle \n")
                            break
                    if not problem_exec:
                        f.write("     - .. image:: {static}/images/rect_green.png \n")
                        f.write("          :target: {filename}/targetsXtasks/"+target+"X"+task+".rst \n")
                        f.write("          :alt: image green rectangle \n")
                    

        
def create_target_rst(name_target, path_readme, path_targets, structure_run_time, list_tasks):
    """
    Write the rst file for a target (presentation and result)    
    
    Parameters
    ----------
        name_target : String, name of the target
        path_readme: String, absolute path of the corresponding readme file
        path_targets: String, absolute path of the targets directory
        structure_run_time: Dictionary 3D [task][target][arg]
        list_tasks: String, list of the tasks
    Returns
    -------
        Nothing
    """
    readme = ''
    with open(path_readme,'r') as f:
        readme = f.read()

    path_file = path_targets+ "/" +name_target+ ".rst"

    with open(path_file,'w') as f:
        f.write(create_rst_base(readme, name_target))

        f.write("\n")
        f.write("\n")
        f.write(".. list-table:: \n")
        f.write("   :widths: auto\n")
        f.write("\n")

        list_tasks2 = []
        one_argument = True
        for task in list_tasks:
            if len(list(structure_run_time[task][name_target].keys())) > 0:
                list_tasks2.append(task)
            if len(list(structure_run_time[task][name_target].keys())) > 1:
                one_argument = False
                break


        if one_argument:

            f.write("   * - Tasks\n")
            for task in list_tasks2:
                f.write("     - `"+task+ " <{filename}/targetsXtasks/"+name_target+"X"+task +".rst>`__ \n")
            f.write("   * - Run_time\n")
            for task in list_tasks2:
                for arg in list(structure_run_time[task][name_target].keys()):
                    f.write("     - "+structure_run_time[task][name_target][arg]+"\n")

        else:
            f.write("   * - Arg/Tasks\n")
            list_allArgs = []
            for task in list_tasks:
                f.write("     - `"+task+ " <{filename}/targetsXtasks/"+name_target+"X"+task +".rst>`__ \n")
                for arg in list(structure_run_time[task][name_target].keys()):
                    if arg not in list_allArgs:
                        list_allArgs.append(arg)

            for arg in list_allArgs:
                f.write("   * - "+arg+"\n")
                for task in list_tasks:
                    if arg in list(structure_run_time[task][name_target].keys()):
                        f.write("     - "+structure_run_time[task][name_target][arg]+"\n")
                    else:
                        f.write("     -  \n")
 

def create_task_rst(name_task, path_readme, path_tasks, structure_run_time, list_targets, path_images, display):
    """
    Write the rst file for a task (presentation and result)     
    
    Parameters
    ----------
        name_task : String, name of the task
        path_readme: String, absolute path of the corresponding readme file
        path_tasks: String, absolute path of the tasks directory
        structure_run_time: Dictionary 3D [task][target][arg]
        list_targets: String, list of the targets
        path_images: String, absolute path of images
        display: String, the type of display

    Returns
    -------
        Nothing
    """
    readme = ''
    with open(path_readme,'r') as f:
        readme = f.read()

    path_file = path_tasks+ "/" +name_task+ ".rst"

    with open(path_file,'w') as f:
        f.write(create_rst_base(readme, name_task))

        f.write("\n")
        f.write("\n")

        # For get only target which have at least one arg
        list_ownTargets = []
        one_argument = True
        for target in list_targets:
            if len(list(structure_run_time[name_task][target].keys())) > 0:
                list_ownTargets.append(target)
            if len(list(structure_run_time[name_task][target].keys())) > 1:
                one_argument = False
                break

        if display == "line" or display == "bar":
            path_graph = create_graph(name_task, structure_run_time, list_ownTargets, path_images, display)
            f.write(".. image:: {static}/"+path_graph +" \n")
            f.write("   :alt: Image of run time graph \n")
 
        elif display == "tabular":

            f.write(".. list-table:: \n")
            f.write("   :widths: auto\n")
            f.write("\n")
            
            if one_argument:
                f.write("   * - Targets\n")
                for target in list_ownTargets:
                    f.write("     - `"+target+ " <{filename}/targetsXtasks/"+target+"X"+name_task +".rst>`__ \n")
                f.write("   * - Run_time\n")
                for target in list_ownTargets:
                    for arg in list(structure_run_time[name_task][target].keys()):
                        f.write("     - "+structure_run_time[name_task][target][arg]+"\n")

            else:
                f.write("   * - Arg/Targets\n")
                list_allArgs = []

                for target in list_targets:
                    f.write("     - `"+target+ " <{filename}/targetsXtasks/"+target+"X"+name_task +".rst>`__ \n")
                    for arg in list(structure_run_time[name_task][target].keys()):
                        if arg not in list_allArgs:
                            list_allArgs.append(arg)

                for arg in list_allArgs:
                    f.write("   * - "+arg+"\n")
                    for target in list_targets:
                        if arg in list(structure_run_time[name_task][target].keys()):
                            f.write("     - "+structure_run_time[name_task][target][arg]+"\n")
                        else:
                            f.write("     -  \n")
            

def create_targetXtask_rst(name_target, name_task,path_code, path_targetsXtasks, structure_run_time, path_images,display):
    """
    Write the rst file for a target of a task (result and source code)  
    
    Parameters
    ----------
        name_target: String, name of the target
        name_tasks: String, name of the task
        path_code: String, absolute path of the code file
        path_targetsXtasks: String, absolute path of the targetsXtasks directory
        structure_run_time: Dictionary 3D [task][target][arg]
    Returns
    -------
        Nothing
    """
    path_file = path_targetsXtasks + "/" + name_target + "X" + name_task + ".rst"

    with open(path_code,'r') as f:
        code = f.read()
    
    with open(path_file,'w') as f:
        f.write(name_task+"/"+name_target+"\n")
        for i in range(len(name_task+name_target)+1):
            f.write("#")
        f.write("\n")

        f.write(meta_data())

        f.write ("The target ")
        f.write("`"+name_target+" <{filename}/targets/"+name_target+".rst>`_")
        f.write(" of the task ")
        f.write("`"+name_task+" <{filename}/tasks/"+name_task+".rst>`_ \n")
        f.write("\n")
        f.write("\n")

        if display == "line" or display == "bar":
            list_target = []
            list_target.append(name_target)
            path_graph = create_graph(name_task, structure_run_time, list_target, path_images, display, name_target)
            f.write(".. image:: {static}/"+path_graph +" \n")
            f.write("   :alt: Image of run time graph \n")
 
        elif display == "tabular":
            f.write(".. list-table:: \n")
            f.write("   :widths: auto\n")
            f.write("\n")
            list_args = list(structure_run_time[name_task][name_target].keys())
            if len(list_args) > 1:
                f.write("   * - Arg \n")
                for arg in list_args:
                    f.write("     - "+arg+"\n")
                f.write("   * - Run_time\n")
                for arg in list_args:
                    f.write("     - "+structure_run_time[name_task][name_target][arg]+"\n")    
            else:
                f.write("   * - Run_time\n")
                if len(list_args) == 0:
                    f.write("     -  X\n")
                else:
                    f.write("     - "+structure_run_time[name_task][name_target][list_args[0]]+"\n")

        f.write("\n")
        f.write("\n")
        f.write("Source code: \n")
        f.write("\n")
        f.write(".. code-block:: python \n")
        f.write("   :linenos: table\n")
        f.write("   :linenostart: 1\n")
        f.write("\n")
        f.write("   ")
        for i in range (len(code)-1):
            if code[i] == '\n':
                f.write('\n')
                f.write("   ")
            else:
                f.write(code[i])
   
