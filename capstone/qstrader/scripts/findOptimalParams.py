import time
import os.path
import  sys
from ast import literal_eval as make_tuple


if __name__ == '__main__':

    import subprocess

    alpha_params = [0.2, 0.5, 0.9]
    gamma_params = [0.2,0.5,0.9]
    epsilon_params = [0.2,0.9]

    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    experiment = sys.argv[1]
    agentType = sys.argv[2]
    alpha_params = sys.argv[3].split(',')
    gamma_params = sys.argv[4].split(',')
    epsilon_params = sys.argv[5].split(',')
    trials = sys.argv[6]

    print "Experiment:", experiment
    print "Learning agent:", agentType
    print "Alpha:", alpha_params
    print "Gamma:", gamma_params
    print "Epsilon:",epsilon_params
    print "Trials:", trials

    if not os.path.isdir("logs/"+experiment+"/"):
        os.mkdir("logs/"+experiment+"/")

    #iterate_list = [0.9]
    allDone=True

    for alpha in alpha_params:
        for gamma in gamma_params:
            for epsilon in epsilon_params:

                    file = "logs/"+experiment+"/findOptimalParam_"+str(alpha)+"_"+str(gamma)+"_"+str(epsilon)+".log"

                    if not os.path.isfile(file) :

                        allDone=False
                        print "BEFORE"

                        p = subprocess.Popen("python agent.py --debug=0 --trials="+str(trials)+" --alpha="+ str(alpha) +" --gamma=" +str(gamma) +" --epsilon="+str(epsilon)+ " --agentType="+agentType+ " --start=random --destination=random  > "+ file,
                                     shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                        #for line in p.stdout.readlines():
                        #    print line,
                        prevSize = 0
                        #os.path.getsize(file)
                        terminated = False
                        i =1

                        while (1) :

                            if terminated == True :
                               break

                            time.sleep(2)

                            if not os.path.isfile(file):
                                break

                            b = os.path.getsize(file)

                            print "Loop id:",i
                            print " FILE ", file, "SIZE:", b
                            #print " PID;" + str(p.pid)

                            p = subprocess.Popen("grep GREAT " + file + " | wc -l", shell=True, stdout=subprocess.PIPE,
                                                 stderr=subprocess.STDOUT)
                            done = 0
                            for line in p.stdout.readlines():
                                done = int(line)

                            print "Done:", done
                            if done == 1 :
                                terminated = True

                            if prevSize == b :
                                if ( i >= 5 ):
                                    p.terminate()
                                    subprocess.Popen("pkill -9 -f python agent.py ", shell=True, stdout=subprocess.PIPE,
                                                         stderr=subprocess.STDOUT)
                                    p = subprocess.Popen("rmtrash "+ file, shell=True, stdout=subprocess.PIPE,
                                                         stderr=subprocess.STDOUT)
                                    terminated = True
                                else :
                                    i = i + 1
                            else :
                                i = 0

                            prevSize = b


    if allDone :
        print "findOptimalParams completed processing for all specified params for alpha, gamma and epsilon. Please check the resuls in logs"
        exit(0)
    else :
        print "findOptimalParams needs reprocesssing for some params."
        exit(1)