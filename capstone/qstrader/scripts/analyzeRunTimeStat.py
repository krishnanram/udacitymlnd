import json
import sys
from collections import OrderedDict

if __name__ == '__main__':

    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    experiment = sys.argv[1]

    runtimeStatFile = "logs/" + experiment + "/runTimeStat.json"

    runtimeStat = None
    with open(runtimeStatFile) as f:
        runtimeStat = json.load(f)


    i=1
    for key in sorted(runtimeStat):
        value = runtimeStat[key]
        print  i,"\t:",key,  "==> ", value
        i=i+1
    print " --------------------------------------------------------------------------------------------------------------"

    rewardsDict = OrderedDict()
    highCompletionParms = OrderedDict()

    for key in sorted(runtimeStat):

        value = runtimeStat[key]
        words = key.split(",")
        trials = words[4].split(" ")
        if int(trials[2]) == 0 :
            print "***********************************************************************************************************************************************************"
        print  key, "  ==> ", value
        if value['reached_dest'] == "yes" :
            rewardsDict[value['rewards']] = key
            if words[0]+words[1]+words[2]+words[3] not in highCompletionParms :
                highCompletionParms[words[0]+words[1]+words[2]+words[3]] = 1
            else :
                highCompletionParms[words[0]+words[1]+words[2]+words[3]] = highCompletionParms[words[0]+words[1]+words[2]+words[3]]+1


    print " \n\n****************************  Sorted by Higest Reward **************************\n"
    for key in reversed(sorted(rewardsDict)) :
        value = rewardsDict[key]
        print  value, "  ==> Total Reward:", key

    print " \n\n****************************  Sorted by Maximum Success Experiment  **************************\n"

    #for key in reversed(sorted(highCompletionParms.values())):

    for key in OrderedDict(reversed(sorted(highCompletionParms.items(), key=lambda t: t[1]))) :
        value = highCompletionParms[key]
        print  "Experimental Param", key, " Success rate:", value
