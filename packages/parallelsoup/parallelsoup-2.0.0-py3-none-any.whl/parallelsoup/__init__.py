from multiprocessing import Process, Lock, Pipe
import requests
from bs4 import BeautifulSoup
import math
import time

class ParallelSoup:
    # Class constructor
    def __init__(self, threads = 2, urls = [], extractor = {}):
        self.threads = threads
        self.siteURLs = urls
        self.extractor = extractor
        self.processData = {}

    def threadedProgram(self, threadId, urls, comm, lock):
        
        data = []
        for url in urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, features="html.parser")
            data = data + self.extractor(soup)
            
        # After work is done,
        # Acquire lock and send data back
        lock.acquire()
        try:
            # Use communication channel and send data back
            comm.send([threadId, data])
        finally:
            # Finally release lock, for others too acquire
            lock.release()
            print("Thread", str(threadId), "done")

    def start(self):
        # Parallel controls
        pComm, comm = Pipe()
        lock = Lock()

        # Number of URLs each thread will get
        chunkSize = math.floor(len(self.siteURLs)/self.threads)

        # List to hold number of processes
        processes = []
        for i in range(0, self.threads):
            if i != self.threads - 1:
                siteUrlChunk = self.siteURLs[i*chunkSize : (i + 1)*chunkSize]
            else:
                # Done to make sure all the remaining urls are allocated to the last thread
                siteUrlChunk = self.siteURLs[i*chunkSize : ]
            
            # Create the processes
            p = Process(target = self.threadedProgram, args = (i, siteUrlChunk, comm, lock,))

            # Append the process to processes list for control
            processes.append(p)

        for p in processes:
            p.start()

        for p in processes:
            d = pComm.recv()
            self.processData[d[0]] = d[1]

        for p in processes:
            p.join()  

    # Get back the processed data
    def get(self):
        arr = []
        for k in self.processData.keys():
            arr = arr + self.processData[k]
        return arr