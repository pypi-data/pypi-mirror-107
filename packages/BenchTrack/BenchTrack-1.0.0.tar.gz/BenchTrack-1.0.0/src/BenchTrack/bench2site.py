"""
-----------------------------------------------bench2site---------------------------------------------------
This module generates the site,
It can be used by calling directly the functions,
You can also call in a shell as follows: python bench2site.py path_infrastructure path_csv path_output

"""

import os
import csv
import shutil
import sys
from os import getcwd, chdir, mkdir
import pathlib as pl
import datetime
from src.BenchTrack.structureBench import BenchTrack
from src.BenchTrack.generateRst import *
import tempfile
from distutils.dir_util import copy_tree



def getDate():
    return str(datetime.datetime.today()).replace(" ","-")

def load_csv_results(path_infra_csv, structure_run_time):
    """
    Loads the csv file of the run results

    Parameters
    ----------
        path_infra_csv : String, path of the csv file
        structure_run_time: Dictionary 3D [task][target][arg] which has been initialized
    Returns
    -------
        structure_run_time: The completed dictionary [task][target][arg]

    """
    
    with open(path_infra_csv) as csv_file:
        csv_reader = list(csv.reader(csv_file, delimiter=','))
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            
            structure_run_time[row[1]][row[2]][row[3]] = row[4]

    return structure_run_time



def csv2content(path_infra, path_benchTrack, file_csv, my_bench):
    """
    This function generates a content directory for the static site

    Parameters
    ----------
        path_infra : String, absolute path of the infrastructure
        path_benchTrack: String, absolute path of the framework Benchtrack
        file_csv: String, name of the csv file used
        my_bench: Benchtrack object, object of the infrastructure
    Returns
    -------
        path_site_infra: String, absolute path of temporary repository for generate site
        name_infra: String, infrastructure name
    """

    name_infra = os.path.basename(path_infra)

    # Get from the Benchtrack object some attributes
    display_tasks = my_bench.getDisplay()

    list_targets = my_bench._BenchTrack__allTarget
    list_tasks = my_bench._BenchTrack__allTask

    # structure_task tells us how the tasks and targets are distributed
    structure_tasks = my_bench.get_structure_tasks()
    list_themes = list(structure_tasks.keys())

    # Initialization of structure_run_time
    structure_run_time = {}
    for task in list_tasks:
        structure_run_time[task] = {}
        for target in list_targets:
            structure_run_time[task][target] = {}

    # Instanciation of structure_run_time from file_csv 
    structure_run_time = load_csv_results(file_csv, structure_run_time)

    #-----------Initialize site_infra repository -----------
    

    # Temporary pelican directory
    path_site_infra = tempfile.mkdtemp()

    path_site = path_benchTrack + "/site"
    # print(path_benchTrack,"bench2site")
    copy_tree(path_site, path_site_infra)

    path_content = path_site_infra + "/content"
    os.mkdir(path_content)
    path_pages = path_content+"/pages"
    os.mkdir(path_pages)

    # Get images for content
    path_images = path_content + "/images"
    shutil.copytree(path_site+"/images_content", path_images)
    os.system("rm -r "+path_site_infra + "/images_content")

    #------------ Summary page ----------------

    create_infra_rst(name_infra,path_pages,path_infra+"/README.rst",structure_run_time,list_targets)

    #------------ Page by target  ------------

    # We create a subdirectory targets
    path_targets = path_content+"/targets"
    os.mkdir(path_targets)

    for tg in list_targets:
        path_tg_rd= path_infra+"/targets/"+tg+"/README.rst" 
        create_target_rst(tg, path_tg_rd, path_targets, structure_run_time, list_tasks)


    #------------ Page by task/ Page by target x task ------------

    path_tasks = path_content+"/tasks"
    os.mkdir(path_tasks)
    path_targetsXtasks = path_content+"/targetsXtasks"
    os.mkdir(path_targetsXtasks)

    for theme in list_themes:
        list_tasks_in_theme = list(structure_tasks[theme].keys())

        for task in list_tasks_in_theme:
            path_readme_task = path_infra+"/tasks/"+theme+"/"+task+"/README.rst"
            display_mode = display_tasks[task]
            # Generation of page by task 
            create_task_rst(task, path_readme_task, path_tasks, structure_run_time, list_targets, path_images,display_mode)
            list_target_in_task = structure_tasks[theme][task]

            for target in list_target_in_task:
                # Generation of page by target x task 
                path_code = path_infra+"/tasks/"+theme+"/"+task+"/"+target
                name_target = os.path.splitext(os.path.basename(target))[0]
                name_target = name_target.replace("_run","")
                create_targetXtask_rst(name_target, task, path_code, path_targetsXtasks, structure_run_time,path_images,display_mode)


    return path_site_infra, name_infra

    
def content2html(path_site_infra, path_infra, name_infra, path_output):
    """
    This function generates the static site with pelican

    Parameters
    ----------
        path_site_infra : String, absolute path of the infrastructure site
        path_infra : String, absolute path of the infrastructure
        name_infra: String, name of the current infrastructure
        path_output: String, absolute path of the output
    Returns
    -------
        Nothing
    """

    # Img for site
    img = False
    os.chdir(path_infra)
    if os.path.exists("img"):
        img = True
        shutil.copytree(path_infra+"/img", path_site_infra + "/theme/static/img")
        
    # Modification of  pelicanconf.py:
    path_conf_py = path_site_infra + "/pelicanconf.py"
    new_file = ""
    line_name_site = "SITENAME = '"+ name_infra+"'\n"

    with open(path_conf_py) as f:
        cpt_line = 0
        for line in f:
            cpt_line +=1
            if cpt_line == 5:
                new_file += "\n"
                new_file += line_name_site
                if img:
                    new_file += "FAVICON = True \n"
                    new_file += "SITELOGO = True \n"
                new_file += "\n"
            else:
                new_file +=line

    with open(path_conf_py,'w') as f:
        f.write(new_file)

    # Call pelican
    os.chdir(path_site_infra)
    os.system(sys.executable + " -m pelican content")

    # Export output
    shutil.copytree(path_site_infra + "/output", path_output)



def bench2site(path_infra, path_benchTrack, file_csv, path_output, save_pelican, benchObject):
    """
    Main functions to generate the site which call the functions: csv2content, content2html, 
    by default the site will be in the benchtrack directory

    Parameters
    ----------
        path_infra: String, absolute path of the infrastructure
        path_benchTrack: String, absolute path of the package benchTrack
        file_csv: String, absolute path of the framework Benchtrack
        path_output: String, absolute path of the output site
        save_pelican: Boolean, indicate if we have to save pelican archive
        benchObject: Benchtrack object, object of the infrastructure

    Returns
    -------
        Nothing
    """
    # print("HELLO BEAUTIFULL WORLD, THIS PACKAGE IS UPDATED")
    path_site_infra, name_infra = csv2content(path_infra, path_benchTrack, file_csv, benchObject)
    output_site = path_output + "/" + name_infra + "_site" + getDate()
    content2html(path_site_infra, path_infra, name_infra,  output_site)

    if save_pelican:
        output_pelican = path_output + "/" + name_infra + "_pelican" + getDate()
        shutil.copytree(path_site_infra, output_pelican)
    # Delete temp directory
    shutil.rmtree(path_site_infra)








    

