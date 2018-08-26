
import argparse 
import hashlib  
import json     
import os       
import pwd      
import sys      
import textwrap     
from datetime import datetime   
from grp import getgrgid        
from pprint import pprint       
parser = argparse.ArgumentParser(
    description=textwrap.dedent('''Initialization --> siv.py -i -D 'dir' -V 'ver_file' -R 'rep_file' -H 'hash'
                                ******************************************************************************
                                Verification  --> siv.py -v -D 'dir' -V 'ver_file' -R 'rep_file' ''')) 
arg_group = parser.add_mutually_exclusive_group()
arg_group.add_argument("-i", "--initialize", action="store_true", help="Initialization mode")
arg_group.add_argument("-v", "--verify", action="store_true", help="Verification mode")
parser.add_argument("-D", "--monitored_directory", type=str, help="Give a Directory that needs to be monitored")
parser.add_argument("-V", "--verification_file", type=str,
                        help="Give a Verification File that can store records of each file in the monitored directory")
parser.add_argument("-R", "--report_file", type=str, help="Give a Report File to store final report")
parser.add_argument("-H", "--hash_function", type=str, help="Hash Algorithm supported are 'SHA-1' and 'MD-5' ")

args = parser.parse_args()      

mon = args.monitored_directory  
ver = args.verification_file    
rep = args.report_file          
alg = args.hash_function        

if args.initialize:             

    print("Initialization Mode\n")
    start = datetime.utcnow()

    
    if os.path.isdir(mon) == 1:
        print("Monitored Directory exists\n")

        
        if alg == "SHA-1" or alg == "MD-5":

            i = 0  
            j = 0  
            det = []    
            det_dir = {}
            det_file = {}
            det_hash = {}

            
            if os.path.isfile(ver) == 1 and os.path.isfile(rep) == 1:
                print("Verification and Report files exist\n")

                
                if (os.path.commonprefix([mon, ver]) == mon):

                    print("Verification and Report file must be outside from the monitored directory\n")
                    sys.exit()
                else:
                    print("Verification and Report files are outside from the monitored directory\n")

            else:
                os.open(ver, os.O_CREAT, mode=0o777)
                os.open(rep, os.O_CREAT, mode=0o0777)
                print("Verification or Report file does not exists and is created now\n")

                
                
                if (os.path.commonprefix([mon, ver]) == mon):
                    print("Verification and Report file must be outside\n")
                    sys.exit()
                else:
                    print("Verification and Report files are outside\n")

            
            choice = input("Do you want to overwrite y/n: ")

            if choice == "n":
                sys.exit()

            elif choice == "y":

                for subdir, dirs, files in os.walk(mon): 
                    for first in dirs:                        
                        
                        i = i+1      
                        path = os.path.join(subdir, first)  
                        alt = os.path.getsize(path)    
                        bol = pwd.getpwuid(os.stat(path).st_uid).pw_name  
                        cal = getgrgid(os.stat(path).st_gid).gr_name      
                        dol = datetime.fromtimestamp(os.stat(path).st_mtime).strftime('%c')  
                        eal = oct(os.stat(path).st_mode & 0o777)

                        det_dir[path] = {
                            "size": alt, "user": bol, "group": cal, "recent": dol, "access": eal
                        }   

                    for file in files:      
                        j = j+1
                        filepath = os.path.join(subdir, file)
                        filesize = os.stat(filepath).st_size
                        fileuser = pwd.getpwuid(os.stat(filepath).st_uid).pw_name
                        filegroup = getgrgid(os.stat(filepath).st_gid).gr_name
                        filerecent = datetime.fromtimestamp(os.stat(filepath).st_mtime).strftime('%c')
                        fileaccess = oct(os.stat(filepath).st_mode & 0o777)

                        
                        if alg == "MD-5":
                            htype = "md5"
                            hashe = hashlib.md5()
                            with open(filepath, 'rb') as monifile:
                                buf = monifile.read()
                                hashe.update(buf)
                                message = hashe.hexdigest()     
                        else:
                            htype = "sha1"
                            hashe = hashlib.sha1()
                            with open(filepath, 'rb') as hfile:
                                buf = hfile.read()
                                hashe.update(buf)
                                message = hashe.hexdigest()

                        det_file[filepath] = {"size": filesize, "user": fileuser, "group": filegroup, "recent": filerecent, ############
                                           "access": fileaccess, "hash": message} 

                det.append(det_dir)     
                det_hash = {"hash_type": htype} 

                det.append(det_file)
                det.append(det_hash)
                json_string = json.dumps(det, indent=2, sort_keys=True) 
                print("\nVerification File generated")

                
                with open(ver, "w") as verifyfile:
                    verifyfile.write(json_string) 

                print("\nReport File generated")

                
                with open(rep, "w") as reportf:
                    end = datetime.utcnow()
                    reportf.write(
                        "Initialization mode complete \n\nMonitored directory = " + mon + "\nVerification file =" + ver + "\nNumber of directories parsed =" + str(
                            i) + "\nNumber of files parsed = " + str(j) + "\nTime taken = " + str(end - start) + "\n")
            else:
                print("Invalid choice")
                sys.exit()
        else:
            print("Hash not supported")
            sys.exit()
    else:
        print("Monitored directory does not exist")
        sys.exit()

elif args.verify:          
    start = datetime.utcnow()

    print("Verification Mode\n")

    if os.path.isfile(ver) == 1:
        print("Verification File exists\n")

        
        if (os.path.commonprefix([mon, ver]) == mon):
            print("Verification and Report file must be outside\n")
            sys.exit()
        else:
            print("Verification and Report files are outside\n")

    else:
        print("Verification file doesn't exist")
        sys.exit()

    i = 0  
    j = 0  
    k = 0  

    with open(ver) as open_file:               
          sysinverif = json.load(open_file)

    with open(rep, "a") as rep_write:   
        rep_write.write("\nVerification Mode begin\n") 

    




    for each_file in sysinverif[2]: 
        htype = each_file[2]           
    

    with open(rep, "a") as rep_write:

        for subdir, dirs, files in os.walk(mon): 

            for fds in dirs: 
                i = i+1
                path = os.path.join(subdir, fds) 
                size = os.stat(path).st_size
                user = pwd.getpwuid(os.stat(path).st_uid).pw_name
                group = getgrgid(os.stat(path).st_gid).gr_name
                recent = datetime.fromtimestamp(os.stat(path).st_mtime).strftime('%c')
                access = oct(os.stat(path).st_mode & 0o777)
                print("Dir   " + path + "\n")

                if path in sysinverif[0]:    
                    if size != sysinverif[0][path]['size']:       
                        rep_write.write("\nWarning directory at the path  " + path + " has different size from the previous size\n")
                        k = k+1
                    if user != sysinverif[0][path]['user']:        
                        rep_write.write("\nWarning dir at the path" + path + " has different user from the previous user \n")
                        k = k+1
                    if group != sysinverif[0][path]['group']:      
                        rep_write.write("\nWarning dir at the path " + path + " has different group from the previous group\n")
                        k = k+1
                    if recent != sysinverif[0][path]['recent']:    
                        rep_write.write("\nWarning dir at the path" + path + " has different modification date from the previous date\n")
                        k =k+1
                    if access != sysinverif[0][path]['access']:    
                        rep_write.write("\nWarning dir at the path" + path + " has modified access rights\n")
                        k =k+1
                else:
                    rep_write.write("\nWarning directory " + path + " has been added\n")
                    k =k+1

        for each_prev_dir in sysinverif[0]:   

            if os.path.isdir(each_prev_dir) == 0: 
                rep_write.write("\nWarning directory " + each_prev_dir + " has been deleted\n") 
                k =k+1

        for subdir, dirs, files in os.walk(mon):

            for file in files:
                j =j+1
                filepath = os.path.join(subdir, file)
                filesize = os.stat(filepath).st_size
                fileuser = pwd.getpwuid(os.stat(filepath).st_uid).pw_name
                filegroup = getgrgid(os.stat(filepath).st_gid).gr_name
                filerecent = datetime.fromtimestamp(os.stat(filepath).st_mtime).strftime('%c')
                fileaccess = oct(os.stat(filepath).st_mode & 0o777)
                print("File   " + filepath + "\n")
                
                if htype == "md5":
                    h = hashlib.md5()
                    with open(filepath, 'rb') as mfile:
                        buf = mfile.read()
                        h.update(buf)
                        message = h.hexdigest()

                
                else:
                    h = hashlib.sha1()
                    with open(filepath, 'rb') as hfile:
                        buf = hfile.read()
                        h.update(buf)
                        message = h.hexdigest()

                if filepath in sysinverif[1]:

                    if filesize != sysinverif[1][filepath]['size']:      
                        rep_write.write("\nWarning file at the path " + filepath + " has different size from the previous size\n")
                        k =k+1
                    if fileuser != sysinverif[1][filepath]['user']:
                        rep_write.write("\nWarning file at the path " + filepath + " has different user from the previous path\n")
                        k =k+1
                    if filegroup != sysinverif[1][filepath]['group']:
                        rep_write.write("\nWarning file at the path" + filepath + " has different group from the previous group\n")
                        k =k+1
                    if filerecent != sysinverif[1][filepath]['recent']:
                        rep_write.write("\nWarning file at the path" + filepath + " has different modification date from the previous date\n")
                        k =k+1
                    if fileaccess != sysinverif[1][filepath]['access']:
                        rep_write.write("\nWarning file " + filepath + " has modified access rights\n")
                        k =k+1
                    if message != sysinverif[1][filepath]['hash']:
                        rep_write.write("\nWarning file " + filepath + " different message digest\n")
                        k =k+1
                else:
                    rep_write.write("\nWarning dir " + filepath + " has been added\n")
                    k =k+1

        for each_prev_file in sysinverif[1]:
            if os.path.isfile(each_prev_file) == 0:
                rep_write.write("\nWarning directory " + each_prev_file + " has been deleted\n")
                k =k+1

    
    with open(rep, "a") as rf:
        end = datetime.utcnow()
        rf.write(
            "\nVerification mode complete \n\nMonitored directory = " + mon + "\nVerification file =" + ver + "\nNumber of directories parsed =" + str(
                i) + "\nNumber of files parsed = " + str(j) + "\nTotal Warnings = " + str(k) + "\nTime taken = " + str(
                end - start) + "\n")

print("Report File generated")
