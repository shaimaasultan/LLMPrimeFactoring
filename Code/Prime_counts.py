import logging
import time
from datetime import datetime
from logging.handlers import MemoryHandler ,RotatingFileHandler
N = 1000000
batch = 0
HowManyBatchs = 0
lg = logging.getLogger("Stats")
lg.setLevel(logging.INFO)
hnd=logging.FileHandler("Prime_Counts\PStats_{}_batch{}.lg".format(str(N*6),str(batch)),"w")
memory_handler = MemoryHandler(100, flushLevel=logging.INFO, target=hnd, flushOnClose=True)
hnd.setLevel(logging.INFO)
lg.addHandler(hnd)

lgn = logging.getLogger("Number")
lgn.setLevel(logging.INFO)
hndn=logging.FileHandler("Prime_Counts\Plist_{}_batch{}.lg".format(str(N*6),str(batch)),"w")
nmemory_handler = MemoryHandler(100, flushLevel=logging.INFO, target=hndn, flushOnClose=True)
hndn.setLevel(logging.INFO)
lgn.addHandler(hndn)


l7 = [] 
lg.info('==============================================')
start_T = time.time()
lg.info('Start Time {} {}'.format(start_T,datetime.now()))
lg.info('==============================================')
lg.info("1- First create List of Primes and their composites....")
for i in range(1,N):
    p = (i*6 + 1)
    if str(p).endswith('5'): continue
    l7.append(p)
    if str(p+4).endswith('5'): continue
    l7.append(p+4)


lg.info("2- List created and currently removing composites from the List....")

l=[7]
for i in l7:
    if i not in l : continue
    l = list(filter(lambda x : x%(i) != 0 , l7))
    if len(l) > 0 :
        l7 = l
    l7.insert(0,i)
    lgn.info(i)
lg.info('==============================================')
lg.info(" [{}] Primes in Numbers from 1 up untill [{}]. ".format(len(l7),(N * 6)))
l7.reverse()
#lg.info("Prime list ={}".format(l7))
lg.info('==============================================')
End_T = time.time()
lg.info('End Time {} {} '.format(End_T,datetime.now() ))
lg.info(" Duration in sec {} ; Duration in minutes {}".format( End_T - start_T , (End_T - start_T)/60.0 ))
lg.info("N = {} and MAX_number = {} and Prime_Counts = {} and L = {} and L7 = {}"
        .format(str(N*6) , str(N*6) , str(len(l7)) ,str(len(l)), str(len(l7)) ) )
lg.info("Prime % = {} ".format(100 * (len(l7)/ (N*6))))
lg.info('==============================================')

last_inital_list = max(l7)



for j in range(1,HowManyBatchs):

    ''' next batch '''
    lg.info("<== Number of Primes before batch # {} = {}".format(j , str(len(l7))))
    lg.info("<== In Previous Batch : minimum_Prime = {} , maxmum_prime = {} ".format( l7[0] , l7[-1]))
    
    lg.info('==============================================')
    lg.info("")
    start_T = time.time()
    lg.info('### Batch = {} # Start Time {} {}'.format(j ,start_T,datetime.now()))
    lg.info("")
    lg.info('==============================================')
    ind = int(((l[-1] +4) - 5) / 6)
    length_before = len(l7)
    #lg.info("ind ={} , l[0] = {} , l[-1] = {} , l7[0] ={} , l7[-1] = {} ".format(ind , l[0] , l[-1] , l7[0] , l7[-1]))
    lg.info("1- First create List of Primes and their composites....")
    for i in range(ind,ind+batch):
        p = (i*6 + 1)
        if str(p).endswith('5'): continue
        l7.append(p)
        if str(p+4).endswith('5'): continue
        l7.append(p+4)
    lg.info("2- List created and currently removing composites from the List....")
    lg.info("number of Primes and their composites after batch {} = {}".format(j , str(len(l7))))
    length_after = len(l7)
    lg.info(" In This Batch new {} numbers added; which Includes new {} Primes and their composites"
            .format(batch * 6 ,length_after-length_before))
    
    #lg.info(l7)
    l=[7]
    for i in l7:
        
        if i not in l : continue
        l = list(filter(lambda x : x%(i) != 0 , l7))
        if len(l) > 0 :
            l7 = l
        l7.insert(0,i)
        #lgn.info(i)
    length_after_remove_composites = len(l7)
    lg.info(" In This Batch new {} numbers added; which Includes new {} Prime Number".format(batch * 6 ,length_after_remove_composites-length_before))
   
    l7.reverse()
    #lg.info("Prime list ={}".format(l7))
    
        

    lg.info('==============================================')
    #if (Factors == False) : PrimesBefore(N)
    End_T = time.time()
    lg.info('End Time {} {} '.format(End_T,datetime.now() ))
    lg.info("    Duration in sec {} ; Duration in minutes {}".format( End_T - start_T , (End_T - start_T)/60.0 ))
    lg.info('''    Inital prime List = {}  and This Batch added = {} numbers
    Total Scanned numbers up untill This Batch ={} and Prime_count = {} and L = {} and L7 = {}'''
            .format(str(N*6) , str(6 * batch) , str( (N*6 + (j * batch*6))) ,  len(l7)  ,str(len(l7)), str(len(l)) ) )
    lg.info(" Prime % ={}".format( 100 * len(l7)/(  ((N*6) + (j *(batch*6))))))
    lg.info('==============================================')

for i in l7:
    if i <= last_inital_list : continue
    lgn.info(i)