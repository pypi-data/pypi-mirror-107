import os
import sys
from src.BenchTrack.structureBench import *
from src.BenchTrack.tools import *
from src.BenchTrack.bench2site import bench2site



def exe(argv):
    """
    execution of the tool BenchTrack

    :param str argv: input in the terminal.

    """

    if len(argv) < 2:
        print("Missing parameter,use --help to read the guide")
        return -1
    path_benchTrack = os.path.dirname(os.path.dirname(os.path.abspath( __file__ )))
    path_inf = argv[-1]
    if path_inf[-1] == "/":
         path_inf = path_inf[:-1]
    if "--help" in argv:
        help()
        return 0
    if "--check" in argv:
        if checkInfrastructure(path_inf):
            benchcheck = BenchTrack(path_inf, path_benchTrack)
            print("Your infratructure is completed and it's structure shows as follow:")
            print(benchcheck.get_structure_tasks())
            exit(0)

    bench = BenchTrack(path_inf, path_benchTrack)

    if manage_flag(argv,bench):
        cwd = os.getcwd()
        save_pelican = bench.isPelican()

        # Generate results csv: 
        bench.exe_bench()
        bench.ToCsv()

        # Generate site: 
        path_csvFile = bench.getPathOutputFile()
        if len(bench.getPathOutputHtml()) == 0:
            output = cwd
        else:
            output = bench.getPathOutputHtml()

        path_absolute_inf = cwd + "/"+ path_inf
        path_absolute_benchTrack = os.path.dirname(path_benchTrack)+"/site-packages/src"
        # print(path_absolute_inf,"inf")
        # print(path_absolute_benchTrack,"bench")
        bench2site(path_absolute_inf, path_absolute_benchTrack, path_csvFile, output, save_pelican, bench)

def mainFonction():
    exe(sys.argv)
if __name__ == '__main__':
    exe(sys.argv)
