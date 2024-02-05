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
        Filefrom = batchSize * (i)
        Fileto = batchSize * i+batchSize
        for p in generate_file_List:
            lg , hnd = InitiateLogger("Stats_{}".format(str(p)) , "Prime_Counts\Factor_{}{}.lg".format(str(p),str(i)))
            for i in range(Filefrom,Fileto):
                n1 = 7 + i * 6
                n2 = 7 + 4 + i * 6
                if str(n1).endswith('5') == False : 
                    lg.info("{};{};{}".format(str(p) , int(n1), int(n1)*int(p)) )
                if str(n2).endswith('5') == False :
                    lg.info("{};{};{}".format(str(p) , int(n2), int(n2)*int(p)) )
            lg.removeHandler(hnd)
            hnd.close()

def InitiatePrimeList(Filefrom ,Fileto ):
        lg , hnd = InitiateLogger("Initial_Stats" , "Prime_Counts\Prime.lg")
        for i in range(Filefrom,Fileto):
            n1 = 7 + i * 6
            n2 = 7 + 4 + i * 6
            if n1 % 5 != 0 : 
                lg.info("{};{};{}".format(str(7) , int(n1), int(n1)*int(7)) )
            if n2 % 5 != 0 :
                lg.info("{};{};{}".format(str(7) , int(n2), int(n2)*int(7)) )
        lg.removeHandler(hnd)
        hnd.close()

def FeedbackFactors(batches,FactorsList):
    for batchA in batches:
        for batchB in batches: 
            for N in  FactorsList: 
                lg.info("working : BatchA ={} ; BatchB = {} ; Factors For = {} .....".format(batchA,batchB , N))
                print("working : BatchA ={} ; BatchB = {} ; Factors For = {} .....".format(batchA,batchB , N))
                f = open( "Prime_Counts\Factor_{}{}.lg".format(7,batchA), '+r')
                str7 = f.read()
                fm = open("Prime_Counts\Factor_{}{}.lg".format(N,batchB) , 'r')
                for i in fm.readlines():
                    mc = i.split(';')
                    c = ";" +mc.pop()[:-1]+";"
                    factors=  ";"+ ";".join(mc)+ ";"   
                    s = str7.replace(c , factors)
                    if len(s)> 0:
                        str7 = s
            

                f.seek(0)
                f.write(str7)
            



lg , hnd = InitiateLogger("RunStats" , "Prime_Counts\RunStats.lg")
lg.info('==============================================')
start_T = time.time()
lg.info('Start Time {} {}'.format(start_T,datetime.now()))
lg.info('==============================================')


batchSize = 10000
batches = range(0,3)
Scanned_Factors = []


try:
    notFacotred_yet=[]
    P = open( "Prime_Counts\Prime.lg", 'r')
    notFacotred_yet = P.readlines()
    if len(notFacotred_yet) == 0 :
        InitiatePrimeList(0, len(batches) * batchSize)
except :
    InitiatePrimeList(0, len(batches) * batchSize)

'''Set Cutoff point'''
from_factor_line = 0
to_factor_line = 270 
print(notFacotred_yet[from_factor_line:to_factor_line])
for t in notFacotred_yet[from_factor_line:to_factor_line]:
    i = str(t.split(";")[1])
    currentRun = [i]
    if str(i) in Scanned_Factors: continue    
    #CreateBatchFactorFiles(batches , batchSize ,currentRun )
    #FeedbackFactors(batches,currentRun)
    Scanned_Factors.append(i)


print('Savinging Final Prime List')
P = open( "Prime_Counts\Prime.lg", 'w')
P.write('')

for i in batches:
    f = open( "Prime_Counts\Factor_7{}.lg".format(i), 'r')
    P = open( "Prime_Counts\Prime.lg", 'a')
    batchLineCounts = f.readlines()
    lf = list(filter(lambda x: len(x.split(';')) == 3 , batchLineCounts ))
    P.writelines(lf)

for j in Scanned_Factors:
    #n=0
    for i in batches:
        f = open( "Prime_Counts\Factor_7{}.lg".format(i), 'r')
        batchLineCounts = f.readlines()
        factCount =list(filter(lambda x: x.find( ";"+str(j)+";") > 0 , batchLineCounts ))
        lg.info('Batch = {}; Batch Line Count = {} ; Composites = {} ; None Composite = {} ; Factor by ={} ; count of Factor by = {}'
            .format(i , len (batchLineCounts) , len(batchLineCounts) - len(lf) , len(lf) , j , len(factCount) ))
        #n=n+len(factCount)
    #lg.info('{};{}'.format(j , n  ))


lg.info('==============================================')
End_T = time.time()
lg.info('End Time {} {} '.format(End_T,datetime.now() ))
lg.info(" Duration in sec {} ; Duration in minutes {}".format( End_T - start_T , (End_T - start_T)/60.0 ))
lg.info('==============================================')




'''
def LLMFactor(batchmain,batchfactor ,factor , main):
    f = open( "Prime_Counts\Factor_{}{}.lg".format(main,batchmain), '+r')
    str7 = f.read()
    fm = open("Prime_Counts\Factor_{}{}.lg".format(factor,batchfactor) , 'r')
    for i in fm.readlines():
            mc = i.split(';')
            c = ";" +mc.pop()[:-1]+";"
            factors=  ";"+ ";".join(mc)+ ";"   
            s = str7.replace(c , factors)
            if len(s)> 0:
                str7 = s
            

    f.seek(0)
    f.write(str7)
'''