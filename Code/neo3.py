import logging
import time
from datetime import datetime
from logging.handlers import MemoryHandler ,RotatingFileHandler

def InitiateLogger(loggerName , FilePath):
    lg = logging.getLogger(loggerName)
    lg.setLevel(logging.INFO)
    hnd=logging.FileHandler(FilePath,"w")
    memory_handler = MemoryHandler(100, flushLevel=logging.INFO, target=hnd, flushOnClose=True)
    hnd.setLevel(logging.INFO)
    lg.addHandler(hnd)
    return lg , hnd

def CreateBatchFactorFiles( batches , batchSize , generate_file_List):
    for i in batches:
        print(i, batchSize * (i)  ,batchSize * i+batchSize)
        Filefrom = int(batchSize) * (i)
        Fileto = int(batchSize) * i+batchSize
        for p in generate_file_List:
            lg , hnd = InitiateLogger("Stats_{}".format(str(p)) , "Prime_Counts\Factor_{}_{}.lg".format(str(p),str(i)))
            for j in range(Filefrom,Fileto):
                n1 = 7 + j * 6
                n2 = 7 + 4 + j * 6
                if str(n1).endswith('5') == False : 
                    lg.info("{};{};{}".format(str(p) , int(n1), int(n1)*int(p)) )
                if str(n2).endswith('5') == False :
                    lg.info("{};{};{}".format(str(p) , int(n2), int(n2)*int(p)) )
            lg.removeHandler(hnd)
            hnd.close()



def InitiatePrimeList(Filefrom ,Fileto ):
        lg , hnd = InitiateLogger("Initial_Stats" ,"Prime_Counts\Prime.lg")
        for i in range(Filefrom,Fileto):
            n1 = 7 + i * 6
            n2 = 7 + 4 + i * 6
            if n1 % 5 != 0 : 
                lg.info("{};{};{}".format(str(7) , int(n1), int(n1)*int(7)) )
            if n2 % 5 != 0 :
                lg.info("{};{};{}".format(str(7) , int(n2), int(n2)*int(7)) )
        lg.removeHandler(hnd)
        hnd.close()

def FeedbackFactors(batches,FactorsList , power_depth , lg):
    for batchA in batches:
        for batchB in batches[0:batchA]: 
            for N in  FactorsList: 
                lg.info("working : BatchA ={} ; BatchB = {} ; Factors For = {} .....".format(batchA,batchB , N))
                print("working : BatchA ={} ; BatchB = {} ; Factors For = {} .....".format(batchA,batchB , N))
                f = open( "Prime_Counts\Factor_{}_{}.lg".format(7,batchA), '+r')
                str7 = f.read()
                fm = open("Prime_Counts\Factor_{}_{}.lg".format(N,batchB) , 'r')
                for i in fm.readlines():
                    mc = i.split(';')
                    c = ";" +mc.pop()[:-1]+";"
                    factors=  ";"+ ";".join(mc)+ ";"   
                    s = str7.replace(c , factors)
                    if len(s)> 0:
                        str7 = s
                #roots replace        
                roots = [str(N)]
                c=N
                for j in range(2,power_depth):
                    c = int(N) * int(c)
                    roots.append(str(N))
                    factors=  ";"+ ";".join(roots)+ ";"
                    rep = ";" + str(c) + ";"  
                    s = str7.replace( rep, factors)
                    if len(s)> 0:
                        str7 = s

                f.seek(0)
                f.write(str7)
            

def ForwardFactors(batches,FactorsList , power_depth , lg):
    for batchA in batches:
        for batchB in batches: 
            for N in  FactorsList: 
                lg.info("working : BatchA ={} ; BatchB = {} ; Factors For = {} .....".format(batchA,batchB , N))
                print("working : BatchA ={} ; BatchB = {} ; Factors For = {} .....".format(batchA,batchB , N))
                fn = open("Prime_Counts\Factor_{}_{}.lg".format(N,batchB) , '+r')
                strfn = fn.read()
                f = open( "Prime_Counts\Factor_{}_{}.lg".format(7,batchA), 'r')
                
                for i in f.readlines():
                    mc = i.split(';')
                    c = ";" +mc.pop()[:-1]+";"
                    factors=  ";"+ ";".join(mc)+ ";"   
                    s = strfn.replace(c , factors)
                    #if len(s)> 0:
                    strfn = s
                #roots replace
                roots = [N]
                c=N
                for j in range(2,power_depth):
                    c = int(N) * int(c)
                    roots.append(N)
                    factors=  ";"+ ";".join(roots)+ ";"
                    rep = ";" + str(c) + ";"  
                    s = strfn.replace( rep, factors)
                    if len(s)> 0:
                        strfn = s

                fn.seek(0)
                fn.write(strfn)


batchSize = 1000       # batch size for each file 
batches = range(0,10)  # divide the files into N batch files

lg , hnd = InitiateLogger("RunStats" , "Prime_Counts\RunStats.lg")

lg , hnd = InitiateLogger("RunStats" , "Prime_Counts\RunStats.lg")
lg.info('==============================================')
start_T = time.time()
lg.info('Start Time {} {}'.format(start_T,datetime.now()))
lg.info('==============================================')
l =[]
for i in range(0,40):
        n1 = 7 + i * 6
        n2 = 7 + 4 + i * 6
        if n1 % 5 != 0  or n1 % 5 != 0 : 
            l.append(n1)
            l.append(n2)


#l = [7,11,13,17,19,23,31,37,39,41,43,47,51,53,57,59,61,67,71,73,79,81,83]
CreateBatchFactorFiles( batches , batchSize , l)
FeedbackFactors(batches,l, 10 , lg)



lg.info('==============================================')
End_T = time.time()
lg.info('End Time {} {} '.format(End_T,datetime.now() ))
lg.info(" Duration in sec {} ; Duration in minutes {}".format( End_T - start_T , (End_T - start_T)/60.0 ))
lg.info('==============================================')
'''




batchSize = 1000       # batch size for each file 
batches = range(0,5)  # divide the files into N batch files
Scanned_Factors = []    # Temp list to save the working scanned factor
from_factor_line = 0    #   from factor line until factor line  in the main intial list. Prime.lg
to_factor_line = 300      # difference between from and to is How many factors will be used to get final prime numbers list and factors.
notFacotred_yet=[ ]     # Prime lines after each iteration shorten after removing the factors form the previous factor iteration 
power_depth = 10        # factor perfect powers to max limit N**10 ( N*N*N*N*N*N*N*N*N*N*N*N*N*N*)

# TBD
# Slice = batch starts not from 0 from any range to and rage  
# check ranges and numbers in each dy amic start and end batch rages 
# correct stats from all files not only 7th 
# ranges starts from Factor_11_3 after 7 * 11 * 1000 because 7 * 11 * batchsize
# # check file modes for append in forward 
# 11;2401;26411 in 7**4 not factord in 11th_1.lg  #done
# first one in the range is 11*1000
# first prime list from 0

print('notFacotred_yet = {}'.format(len(notFacotred_yet))) 
P = open( "Prime_Counts\Prime.lg", 'w+')
if len(notFacotred_yet) == 0 :
    InitiatePrimeList(0, len(batches) * batchSize)
notFacotred_yet = P.readlines()


#Set Cutoff point



print(notFacotred_yet[from_factor_line:to_factor_line])

for t in notFacotred_yet[from_factor_line:to_factor_line]:
    i = str(t.split(";")[1])
    currentRun = [i]
    if str(i) in Scanned_Factors: continue    
    CreateBatchFactorFiles(batches , batchSize ,currentRun ) #create batch files for one of the factors
    FeedbackFactors(batches,currentRun,power_depth) #Feedback this files factors into main 7 batch files.
    #ForwardFactors(batches,currentRun,power_depth)
    Scanned_Factors.append(i)           # save the already saved factors 

print(notFacotred_yet[from_factor_line:to_factor_line])

print('Savinging Final Prime List')
P = open( "Prime_Counts\Prime.lg", 'w')
P.write('')

for i in batches:
    f = open( "Prime_Counts\Factor_7_{}.lg".format(i), 'r+')
    P = open( "Prime_Counts\Prime.lg", 'a')
    batchLineCounts = f.readlines()
    lf = list(filter(lambda x: len(x.split(';')) == 3 , batchLineCounts ))
    P.writelines(lf)

print(notFacotred_yet[from_factor_line:to_factor_line])

for j in notFacotred_yet[from_factor_line:to_factor_line]:
    n=0
    for i in batches:
        f = open( "Prime_Counts\Factor_7_{}.lg".format(i), 'r')
        batchLineCounts = f.readlines()
        factCount =list(filter(lambda x: x.find( ";"+str(j.split(';')[1])+";") > 0 , batchLineCounts ))
        lg.info('Batch File Factor_7_{}.lg ; File Line Count = {} ; Composites = {} ; None Composite = {} ; Factor by ={} ; count of Factor by = {}'
            .format(i , len (batchLineCounts) , len(batchLineCounts) - len(lf) , len(lf) , j.split(';')[1] , len(factCount) ))
        n=n+len(factCount)
    lg.info('Total Factor by = {};count of Factor by = {}'.format(j.split(';')[1] , n  ))


lg.info('==============================================')
End_T = time.time()
lg.info('End Time {} {} '.format(End_T,datetime.now() ))
lg.info(" Duration in sec {} ; Duration in minutes {}".format( End_T - start_T , (End_T - start_T)/60.0 ))
lg.info('==============================================')


'''

