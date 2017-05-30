# -*- coding: utf-8 -*-
from collections import namedtuple
import functools as ft

#%%
class Scheduler:
    Job = namedtuple("Job", ("weight, length"))
    
    def __init__(self, filename=None):
        self.jobs = [] # list to hold all the jobs to be scheduled
        if(filename):
            self.read_from(filename)
    
    def read_from(self, filename):
        with open(filename, "r") as FILE:
            l = FILE.readline().split()
            assert(len(l) == 1)
            num_jobs = int(l[0])
           
            for line in FILE:
                l = map(int, line.split())
                if len(l) == 0: continue
                assert len(l) == 2
                self.jobs.append(Scheduler.Job(*l))
         
        assert len(self.jobs) == num_jobs
        return

    def get_schedule(self, mode=2):
        """ 
        Schedule the jobs by decreasing value of (Weight - Length).
        Return a list of indices into the master-list "jobs".
        """
        if mode == 1:
            def sort_key(idx):
                job = self.jobs[idx]
                return ((job.weight-job.length), job.weight)
        elif mode == 2:
            def sort_key(idx):
                job = self.jobs[idx]
                return float(job.weight)/float(job.length)
        else:
            raise ValueError("'mode' should be 1 or 2")
            
        return sorted( range(len(self.jobs)), \
                       key=sort_key, \
                       reverse=True )
        
    def compute_schedule_cost(self, sched):
        """
        Return the cost of the job-schedule "sched", computed as the
        weighted sum of completion times.
        sched should be an ordered iterable of job-indices into the 
        master-list "Scheduler.jobs"
        """
        def add_job_cost((total_cost,total_time), job_idx):
            job = self.jobs[job_idx]
            total_time += job.length
            total_cost += (job.weight * total_time)
            return (total_cost, total_time)
        
        return ft.reduce(add_job_cost, sched, (0,0))
