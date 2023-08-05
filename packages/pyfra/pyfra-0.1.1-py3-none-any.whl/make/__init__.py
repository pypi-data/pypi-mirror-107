from pyfra.utils import *
from pyfra.remote import *
from functools import wraps


class Orchestrator:
    def __init__(self, experiment_name):
        ...
    
    def fetch_result(self, task):
        ...
    
    def plan_dag(self, task):
        ...


class Task:
    def dependencies(self, params):
        ...
    
    def run(self, env, params, inputs):
        ...