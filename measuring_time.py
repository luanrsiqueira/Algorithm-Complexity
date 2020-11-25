import getopt
import sys
import subprocess
import os
import time
import csv

ngs =[]
mar = []
par = []
fast = []
bioseq = []

# Automatic execution of each tool
try:
    opts,args=getopt.getopt(sys.argv[1:],"he:i:p:f:")
    for opt,arg in opts:
        if opt == "-h":
            print ('measuring_time.py -i PATH <single-end>')
            print ('measuring_time.py -i PATH <Parired tag 1> -p PATH <Paired tag 2> -f PATH <Input list.txt for FastUniq>')
            sys.exit()
        elif opt == "-i":
            input1 = arg
            #print(input1)
            print("Running...")
        elif opt == "-p":
            input2 = arg
            #print(input2)
        elif opt == "-f":
            input_txt = arg
            #print(input_txt)
                
except getopt.GetoptError:
    print ('measuring_time.py -i PATH <single-end>')
    print ('measuring_time.py -i PATH <Parired tag 1> -p PATH <Paired tag 2> -f PATH <Input list.txt for FastUniq>')
    sys.exit(2)

class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def marDre():
    os.environ['HADOOP_HOME'] = '/usr/local/hadoop'
    os.environ['MARDRE_HOME'] = 'PATH where the tool is installed'
    with cd("MarDRe-v1.4/bin/"):
        if opt == "-i":
            outMardre = "./mardrerun -i " + input1
        elif opt == "-p":
            outMardre = "./mardrerun -i " + input1 + " " + "-p " + input2
        elif opt == "-f":
            outMardre = "./mardrerun -i " + input1 + " " + "-p " + input2
        #print(outMardre)
        subprocess.call(outMardre, shell=True)

def NgsReadsTreatment():
    if opt == "-i":
        ngsreads = "java -jar NgsReadsTreatment_v1.3.jar " + input1 + " 8"
    elif opt == "-p":
        ngsreads = "java -jar NgsReadsTreatment_v1.3.jar " + input1 + " " + input2 + " 8"
    elif opt == "-f":
        ngsreads = "java -jar NgsReadsTreatment_v1.3.jar " + input1 + " " + input2 + " 8"
    #print(ngsreads)
    subprocess.call(ngsreads, shell=True)

def parDre():
    with cd("ParDRe-rel2.2.5"):
        if opt == "-i":
            outPardre = "mpirun ./ParDRe -i " + input1
        elif opt == "-p":
            outPardre = "mpirun ./ParDRe -i " + input1 + " -p " + input2
        elif opt == "-f":
            outPardre = "mpirun ./ParDRe -i " + input1 + " -p " + input2
        #print(outPardre)
        subprocess.call(outPardre, shell=True)

def fastUniq():
        with cd("FastUniq/source"):
            if opt == "-i":
                print("...")
            elif opt == "-f":
                input_txt = arg
                outFast = "./fastuniq -i " + input_txt + " -t q -o output_1.fastq -p output_2.fastq -c 1"
            #print(outFast)
            subprocess.call(outFast, shell=True)

def bioSeqZip():
    with cd("bioseqzip/build"):
        if opt == "-i":
            outBio = "bioseqzip_collapse -i " + input1 + " -f fastq -v 4 --csv-report"
        elif opt == "-p":
            outBio = "bioseqzip_collapse -i " + input1 + " -p " + input2 + " -f fastq -v 4 --csv-report"
        elif opt == "-f":
            outBio = "bioseqzip_collapse -i " + input1 + " -p " + input2 + " -f fastq -v 4 --csv-report"
        #print(outBio)
        subprocess.call(outBio, shell=True)

# Measuring Time
for i in range(1,2):
    start = time.time()
    marDre()
    end = time.time()
    mar.append(end - start)

for i in range(1,2):
    start = time.time()
    NgsReadsTreatment()
    end = time.time()
    ngs.append(end - start)

for i in range(1,2):
    start = time.time()
    parDre()
    end = time.time()
    par.append(end - start)

for i in range(1,2):
    start = time.time()
    fastUniq()
    end = time.time()
    fast.append(end - start)

for i in range(1,2):
    start = time.time()
    bioSeqZip()
    end = time.time()
    bioseq.append(end - start)


# Counting the number of readings within each Dataset
reads ="awk '{s++}END{print s/4}' " + input1
output_reads = (subprocess.Popen(reads, stdout=subprocess.PIPE, shell=True, universal_newlines=True).communicate()[0])
output_reads = output_reads.rstrip('\n')
#print(output_reads)

# Storing the data
with open("dados.csv", 'a') as output:
    write = csv.writer(output)
    write.writerow([output_reads, mar, ngs, par, fast, bioseq])

