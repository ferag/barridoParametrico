#!/usr/bin/env python

"""barridoDatos.py: iterate a config files different parameters to run
   delft3D simulations using different values"""

__author__ = "Fernando Aguilar"
__copyright__ = "Copyright 2016"
__credits__ = ["Fernando Aguilar"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Ferando Aguilar"
__email__ = "aguilarf@ifca.unican.es"
__status__ = "On development"

import csv
import subprocess
import os
import sys
import getpass

def config(filename,inputFile,username,password,path):
    """Prepares the config file to set up N analysis.

    Params:
     - Filename: Name of the csv file with these columns:
            - Name of param
            - Value of param
            - Number of iteration (iration indicates the number of analysis tu run)
     - inputFile: .inp base file
     - username: Altamira username
     - password: altamira pass
     - path: path of the original base set of input files from hydrodinamics

    Exceptions:
    ?

    """
    reader = csv.reader(open(filename, 'rb'),delimiter=';')
    iteration = -1 #Indicates number of current iteration.
    for index,row in enumerate(reader):
        if index>0:
            if row[2] > iteration:
                if iteration > -1:
                    print "Launch Job Iteration#" + iteration
		    launchJob(inputFile,username,password,path,iteration)
		iteration = row[2]
                print "Iteration #" + iteration
                lines = open(inputFile, 'r').readlines()
                out = open(inputFile.rsplit( ".", 1 )[ 0 ] + "_" + iteration + ".inp", 'w')
                out.writelines(lines)
                out.close()

            print "Param: " + row[0] + " Value: " + row[1]
            modInputFile(inputFile.rsplit( ".", 1 )[ 0 ] + "_" + iteration + ".inp", row[0], row[1])

    #Launch Last iteration
    print "Launch Job Iteration#" + iteration
    launchJob(inputFile,username,password,path,iteration)

def modInputFile(inputFile, paramName, value):
    """Modifies the input File with the new value of a Param.

    Params:
     - inputFile: Name of the input File to be modified
     - paramName: Name of param to be changed
     - value: value of param to be changed.

    Exceptions:
    ?

    """
    lookup = "; " + paramName 
    print "Buscando: " + lookup
    with open(inputFile) as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
               print 'found at line:', num
               replaceLine(inputFile, num-1, " " + value + " ; " + paramName + "\n")

def replaceLine(inputFile, lineNum, text):
    """Replace the line with number lineNum with the text.

    Params:
     - inputFile: Name of the input File to be modified
     - lineNum: Number of line to be replaced
     - text: text to replace the line

    Exceptions:
    ?

    """
    
    lines = open(inputFile, 'r').readlines()
    lines[lineNum] = text
    out = open(inputFile, 'w')
    out.writelines(lines)
    out.close()

def launchJob(inputFile, username, password, path, iteration):
    """Upload the input file to a new environment a launch the Delft3D job.
    
    Params:
     - inputFile: .inp config file
     - username: Altamira username
     - password: Altamira password
     - path: base path with input files from hydrodinamics
     - iteration: number of iteration to name the new folder

    Exceptions:
    ?
    """
    newInputFile = inputFile.rsplit( ".", 1 )[ 0 ] + "_" + iteration + ".inp"
    command = "ssh {0}@altamira1.ifca.es 'mkdir {1}'".format(username, path + "_" + iteration)
    print command
    print "Creating base directory..."
    os.system(command)
    

    #Changes in run_waq
    #Change inp file
    command = "sed -i\"run_delwaq.sh\" \'40d\' run_delwaq.sh; sed -i\"run_delwaq.sh\" '40iinpfile={2}' 'run_delwaq.sh'".format(username,path + "_" + iteration, newInputFile, inputFile.rsplit( ".", 1 )[ 0 ], inputFile.rsplit( ".", 1 )[ 0 ] + "_" + iteration )

    #if we need to change names: mv {3}.scn {4}.scn ; mv {3}.par {4}.par ; mv {3}.res {4}.res
    print "Preparing files"
    print command
    os.system(command)
    
    #Change BASE_PATH
    command = "sed -i\"run_delwaq.sh\" \'28d\' run_delwaq.sh; sed -i\"run_delwaq.sh\" '28iexport BASE_PATH={0}' 'run_delwaq.sh'".format(path)
    print "Changing BASE_PATH"
    print command
    os.system(command)

    command = "sed -i\"run_delwaq.sh\" \'29d\' run_delwaq.sh; sed -i\"run_delwaq.sh\" '29iexport OUTPUT_PATH={0}' 'run_delwaq.sh'".format(path + "_" + iteration)
    print "Changing OUTPUT_PATH"
    print command
    os.system(command)
    
    #Send input files
    command = "scp {0} {1}@altamira1.ifca.es:/{2}".format(newInputFile,username,path + "_" + iteration)
    print "Sending input file"
    os.system(command)

    command = "scp {0} {1}@altamira1.ifca.es:/{2}".format("run_delwaq.sh",username,path + "_" + iteration)
    os.system(command)
    
    #Job Submission
    command = "ssh {0}@altamira1.ifca.es 'cd {1} ; mnsubmit run_delwaq.sh'".format(username,path + "_" + iteration)
    print "Job submission"
    print command
    os.system(command)

def main():
        print "Delft3D - Altamira: Barrido de Datos"
	print "Barrido needs some data for working:"
	username = raw_input("Please, insert your Altamira ID:\n")
        password = getpass.getpass("Please, insert your password\n")
        print "In order to work, Barrido needs the path of base set of Delft3D files (from the hydrodinamics)"
        path = raw_input("Type the path\n")
        inputFile = 'wqnew_basic2_t26.inp'
	# inputFile = raw_input("Type the name of the original .inp file\n")
        configFile = "configBarrido.csv"
        # configFile = raw_input("Type the name of the csv input file\n")
        config(configFile, inputFile, username, password, path)

if __name__ == "__main__":
    main()

