# Utility to process production logs.
# Counts number of passes and failures and also
# the total test time for each unit and for the batch based on the date
# that is passed to the command line in format YYYY/MM/DD
# The code is a demonstrator in that it can be modified to process any type of production log that
# consists of text files that need to be read and parsed

import sys
import os


testdate = ""
unitcount = 0
alltesttime = 0
alltestcount = 0
allfailcount = 0
allpasscount = 0
passtesttime = 0
failtesttime = 0
allpasstesttime = 0
allfailtesttime = 0
#print(sys.argv)

#get the date parameter
for l in sys.argv:
    if '-d' in l:
        testdate = l[2:]

if testdate == "":
    print("Please specify a date parameter eg >parse -d2019/10/15")
    exit(0)


print("Test Date:",testdate)
# Column names
print("SERIAL,FAIL,PASS,TOTALTESTS,TOTALTIME")


# for each file in the current directory ....
for filename in os.listdir(os.getcwd()):
    # only CY...txt files
    if "txt" in filename and filename[:2] == "CY":
        file = open(filename,'r')
        #print(filename[:-4], end=' ')

        lines = file.readlines()
        failcount = 0;
        passcount = 0;
        passtesttime = 0
        failtesttime = 0
        ldate = ""
        ltime = ""
        TotalTestTime = 0
        unitcount = unitcount + 1
        for i in range(0, len(lines)):
            l = lines[i]
            if "FAIL FAIL FAIL" in l:
                ltime = lines[i+2]
                ldate = lines[i+5]
                i = i+5
                if "Terminal Debug Version" in ldate:
                    s = ldate.split(' ')
                    if s[6] == testdate:
                        #print(s[6])
                        if "Test Time" in ltime:
                            s = ltime.split(' ')
                            #print("FAIL:",s[4])
                            TotalTestTime = TotalTestTime + int(s[4])
                            failcount = failcount + 1;
                            failtesttime = failtesttime + int(s[4])


            if "PASS PASS PASS" in l:
                ltime = lines[i+2]
                ldate = lines[i+5]
                i = i+5
                if "Terminal Debug Version" in ldate:
                    s = ldate.split(' ')
                    if s[6] == testdate:
                        #print(s[6])
                        if "Test Time" in ltime:
                            s = ltime.split(' ')
                            #print("PASS:",s[4])
                            TotalTestTime = TotalTestTime + int(s[4])
                            passcount = passcount + 1;
                            passtesttime = passtesttime +  int(s[4])
        alltesttime = alltesttime + TotalTestTime
        alltestcount = alltestcount + passcount+failcount
        allpasscount = allpasscount + passcount
        allfailcount = allfailcount + failcount
        allpasstesttime = allpasstesttime + passtesttime
        allfailtesttime = allfailtesttime + failtesttime
        #print(",",failcount,",",passcount,",",passcount+failcount,",",TotalTestTime)
        print("{:s},{:d},{:d},{:d},{:d}".format(filename[:-4],failcount,passcount,passcount+failcount,TotalTestTime))
print("Total Units Tested ",unitcount)
print("Total Tests performed ",alltestcount)
print("Total Passes ",allpasscount)
print("Total Fails  ",unitcount - allpasscount)
print("Total Test Time ",alltesttime)
print("Average test time {:0.2f}s ".format(alltesttime/(alltestcount)))
print("Average test time passed units {:0.2f}s ".format(allpasstesttime/(allpasscount)))
print("Average test time failed units {:0.2f}s ".format(allfailtesttime/(allfailcount)))
print("Percent passed units {:2.1f}% ".format(100*allpasscount/(unitcount) ))
print("Testing Efficiency {:2.1f}%".format(100*allpasstesttime/(alltesttime)))
print("Real average test time per unit {:0.2f}".format(alltesttime/unitcount)  )
