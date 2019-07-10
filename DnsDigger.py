import os
import argparse
import sys
import time
start = time.time()
time_out = 2 # you can modify the timeout here
i = 1
vulnerable = False


print("""                                        
                             *,        
                           *#(((,      
                         /#/.   ,(*    
    DnsDigger 1.0         .((,     ,(,  
                           ./(,    .((,
    @Cyber_Purge           ,((//(, *(*  
                        .((/   .///    
                      ,((,             
                    ,((/               
         *%%#.   .&(,/                 
       #@&&&&%(/&&%%(                  
     .@@&&&&&.#&%%%                    
    ,@@&&&&%.&%%,.#/                   
   ,@@&&&&&#  .#####/                  
   &@&&&&&&&%%%#####/                  
 .,@&&&&&&&%%%#####.                   
  .&&&&&&%%%####(                      
    #%%#####(,        \n""")
os.system("mkdir /home/DnsDigger/ >/dev/null 2>&1")
staticPath="/home/DnsDigger/"
OriginalExceptHook = sys.excepthook
def NewExceptHook(type, value, traceback): #exit by pressing CTRL-C
    global Terminator
    Terminator = True
    if type == KeyboardInterrupt:
        print("\n\nExiting by CTRL+C.\n\n")
    else:
        OriginalExceptHook(type, value, traceback)
sys.excepthook = NewExceptHook

global Terminator
Terminator = False

def DnsDigger_list(file_path,domain): # list mode
    t = 1
    vuln = ""
    vulnerable = False
    target_list_file = open(file_path,"r") #opening the list file
    line = target_list_file.readline().rstrip("\n\r") # striping any empty lines
    while line: # looping through the list line by line
        output = os.popen(f" dig +tries=1 +time={time_out} axfr {domain} @{line}").read()
        if "failed" in str(output): # error handling
            print(f"[{t}]:{line}   :\033[31mnot vulnerable to zone-tranfer \033[0m \n")
            line = target_list_file.readline().rstrip("\n\r")# striping any empty lines
            t += 1
        else:
            print(f"[{t}]:{line}   :\033[92m~~IS VULNERABLE~~ \033[0m \n")
            raw_path=(f"{staticPath}{line}" + ".txt") #creating a string to contain the path of the txt file
            path = text = os.linesep.join([s for s in raw_path.splitlines() if s]) # cleaning up the string
            outputWrite = open(path,'w')
            outputWrite.write(output)# writing the output to the txt file
            outputWrite.close()
            vulnerable = True
            vuln += line
            line = target_list_file.readline().rstrip("\n\r")
            t+= 1

    end = time.time() # ending time capture
    elapsed = time.time() - start
    final_time = time.strftime("%H:%M:%S", time.gmtime(elapsed)) # formating the time variable
    print(f"\033[92mscan complete {i-1}/{i-1} | time elapsed : {final_time}\033[0m ") # number of targets | time taken
    print(f"command : dif axfr (domain) @(ip)")
    if vulnerable:
        print(f"DNS Zone transfer data is saved at : \033[36m {path}  \033[0m")
    else:
        print("No vulnerable targets.") #


def DnsDigger_Single(ip,domain):
    global vulnerable
    output = os.popen(f" dig +tries=1 +time={time_out} axfr {domain} @{str(ip)}").read() #command for zone-starnsfer
    if "failed" in str(output):
        print(f"[{i}]:{str(ip)}   :\033[31mnot vulnerable to zone-tranfer \033[0m \n")
    else:
        print(f"[{i}]:{str(ip)}   :\033[92m~~IS VULNERABLE~~ \033[0m \n")
        raw_path = (f"{staticPath}{str(ip)}" + ".txt")
        path = text = os.linesep.join([s for s in raw_path.splitlines() if s])
        outputWrite = open(path, 'w')
        vulnerable = True
        outputWrite.write(output)
        outputWrite.close()
    end = time.time()
    elapsed = time.time() - start
    final_time = time.strftime("%H:%M:%S", time.gmtime(elapsed))
    print(f"\033[92mscan complete {i-1}/{i-1} | time elapsed : {final_time}\033[0m ")
    print(f"command : dif axfr (domain) @(ip)")
    if vulnerable:
        print(f"DNS Zone transfer data is saved at : \033[36m {path}  \033[0m")
    else:
        print("No vulnerable targets.")

# parsing the parameters #
HELP = argparse.ArgumentParser(
    description="example:  invisible-digger.py -l (target.txt) \n"
                " -d (example.com) \n"
)
HELP.add_argument('--list', help='enter the target list file, example:" /root/target.txt')
HELP.add_argument('--domain',help='enter the domain name, example:" example.com "')
HELP.add_argument('--ip',help='enter the ip address of the target example: "127.0.0.1"')
args = HELP.parse_args()
file_path = args.list
domain = args.domain
ip = args.ip
#                       #
# display help if no argument is passer #
if len(sys.argv) < 2:
    HELP.print_usage()
    sys.exit(1)
#                                       #

# EXECUTE THE FUNCTIONS #

if not ip:
    DnsDigger_list(file_path,domain)
    if Terminator:
        print
        "I'll be back!"
        sys.exit()
else:
    DnsDigger_Single(ip,domain)
    if Terminator:
        print
        "I'll be back!"
        sys.exit()
