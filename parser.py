from pprint import pprint
import json
import sys



############################################################################################

def check_task_format(task_reqs):

    for req in task_reqs:
        if (req['type'] != 'compute') and (req['type'] != 'memory') and (req['type'] != 'network'):
            print "The type of the requirement is not allowed"
            return False

        ## Checking the amount of consumables required is represented correctly
        if 'amount' in req:
            if (req['amount'] > 0) and \
                (type(req['amount']) == int):
                pass
            else:
                print "In Task task_id, the amount of consumables is not a positive integer"
                return False
        else:
            print "In Task task_id, requirement type req_type, no amount of consumables is specified"
            return False

        ## Checking the form of each input
        if 'form' in req:
            ## For Compute, check if number of co-located threads, and machine ISA is specified 
            if req['type'] == "compute":
                pass
                # Checking co-located threads
                if 'num_threads' in req['form']:
                    if (req['form']['num_threads'] > 0) and \
                        (type(req['form']['num_threads']) == int):
                        pass
                    else:
                        print "In Task task_id, requirement type compute, number of co-located threads is not a positive integer"
                        return False
                else:
                    print "In Task task_id, requirement type compute, number of co-located threads is not specified"
                    return False
                # Checking machine ISA
                if 'ISA' in req['form']:
                    if isinstance(req['form']['ISA'], str) or isinstance(req['form']['ISA'], unicode):
                        pass
                    else:
                        print "In Task task_id, requirement type compute, ISA specified is not a string"
                        return False
                else:
                    print "In Task task_id, requirement type compute, no machine ISA specified"
                    return False

            elif req['type'] == "memory":
                pass
                if 'max_mem' in req['form']:
                    ## TODO: Let user specify unit of memory (B, KB, MB, GB, etc...)
                    if (req['form']['max_mem'] > 0) and \
                        (type(req['form']['max_mem']) == int):
                        pass
                    else:
                        print "In Task task_id, requirement type memory, max amount of memory used is not a positive integer"
                        return False
                else:
                    print "In Task task_id, requirement type memory, max amount of memory used during execution not specified"
                    return False

                if 'device' in req['form']:
                    if isinstance(req['form']['device'], str) or isinstance(req['form']['device'], unicode):
                        pass
                    else:
                        print "In Task task_id, requirement type memory, device is not a string"
                        return False
                else:
                    print "In Task task_id, requirement type memory, device is not specified"
                    return False

            elif req['type'] == "network":
                pass
                if 'L2_protocol' in req['form']:
                    if isinstance(req['form']['L2_protocol'], str) or isinstance(req['form']['L2_protocol'], unicode):
                        pass
                    else:
                        print "In Task task_id, requirement type network, L2 protocol is not a string"
                        return False
                else:
                    print "In Task task_id, requirement type network, L2 protocol for downlink is not specified"
                    return False

                if 'direction' in req['form']:
                    if ((req['form']['direction']).lower() == 'ul') or \
                        ((req['form']['direction']).lower() == 'dl'):
                        pass
                    else:
                        print "In Task task_id, requirement type network, direction specified is not correct"
                        return False
                else:   
                    print "In Task task_id, requirement type network, direction is not specified"
                    return False

            else:
                print "In Task task_id, there is an entry for an unknown consumable type"
                return False
    # Is a task
    return True    


def check_res_format(res):

    for cap in res:

        if (cap['type'] != 'compute') and (cap['type'] != 'memory') and (cap['type'] != 'network'):
            print "In Resource res_id, there is a rate of a type which we don't recognize"
            return False

        if 'rate' in cap:
            if (cap['rate'] > 0) and \
                (type(cap['rate']) == int):
                pass
            else:
                print "In Resource res_id, rate type, rate_type, rate is not a positive integer"
                return False
        else:
            print "In Resource res_id, rate type rate_type, no rate is specified"
            return False

        if 'form' in cap:
            if cap['type'] == 'compute':
                pass
                if 'num_threads' in cap['form']:
                    if (type(cap['form']['num_threads']) == int) and \
                        (cap['form']['num_threads'] > 0):
                        pass
                    else:
                        print "In Resource res_id, rate type compute, number of co-located threads is not a positive integer"
                        return False
                else:
                    print "In Resource res_id, rate type compute, number of co-located threads is not specified"
                    return False

                if 'ISA' in cap['form']:
                    if isinstance(cap['form']['ISA'], str) or isinstance(cap['form']['ISA'], unicode):
                        pass
                    else:
                        #In Resource res_id, rate type compute, ISA specified is not a string
                        return False
                else:
                    print "In Resource res_id, rate type compute, no machine ISA is specified"
                    return False

            elif cap['type'] == 'memory':
                if 'max_mem' in cap['form']:
                    ## TODO: Let user specify unit of memory (B, KB, MB, GB, etc...)
                    if (type(cap['form']['max_mem']) == int) and \
                        (cap['form']['max_mem'] > 0):
                        pass
                    else:
                        print "In Resource res_id, rate type memory, amount of maximum memory offered is not a positive integer"
                        return False
                else:
                    print "In Resource res_id, rate type memory, amount of maximum memory offered is not specified"
                    return False

                if 'device' in cap['form']:
                    if isinstance(cap['form']['device'], str) or isinstance(cap['form']['device'], unicode):
                        pass
                    else:
                        print "In Resource res_id, rate type memory, device specified is not a string"
                        return False
                else:
                    print "In Resource res_id, rate type memory, no device specified"
                    return False

            elif cap['type'] == 'network':
                pass
                if 'L2_protocol' in cap['form']:
                    if isinstance(cap['form']['L2_protocol'], str) or isinstance(cap['form']['L2_protocol'], unicode):
                        pass
                    else:
                        print "In Resource res_id, rate type network, the L2 protocol is not a string"
                        return False
                else:
                    print "In Resource res_id, rate type network, the L2 protocol is not specified"
                    return False

                if 'direction' in cap['form']:
                    if (cap['form']['direction'].lower() == 'ul') or \
                        (cap['form']['direction'].lower() == 'dl'):
                        pass
                    else:
                        print "In Resource res_id, rate type network, the direction specified is not correct"
                        return False
                else:
                    print "In Resource res_id, rate type network, no direction specified "
                    return False
            else:
                print "In Resource res_id, there is an entry for an unknown rate type"
                return False
        else:
            print "In Resource res_id, rate type, rate_type, no form is specified"
            return False
    # Is a resource
    return True


def is_workload(workload):
    pass

    if not workload:
        # Workload is empty
        return True

    for task_id, task_reqs in workload.iteritems():
        is_task = False
        if not task_reqs:
            # The tasks has no requirements
            continue
        is_task = check_task_format(task_reqs)
        if is_task == False:
            return False

    #Workload structure passes all current checks
    return True


def is_res_list(res_list):

    for res_id, res in res_list.iteritems():
        is_res = False
        if not res:
            # Resource has no rates
            continue     
        else:
            is_res = check_res_format(res)

        if is_res == False:
            return False

    # Resource list passes all current checks
    return True
                
############################################################################################

def read_workload(filename):

    with open(filename, 'r') as j:
        workload = json.load(j)

    if is_workload(workload):
        return workload
    else:
        return None

def read_res_list(filename):

    with open(filename, 'r') as j:
        res_list = json.load(j)

    if is_res_list(res_list):
        return res_list
    else:
        return None


############################################################################################

def satisfy_form(req, cap):

    for attr in req['form'].keys():
        if (isinstance(req['form'][attr], str) and isinstance(cap['form'][attr], str)) \
            (isinstance(req['form'][attr], unicode) and isinstance(cap['form'][attr], unicode):
            if req[attr] != cap[attr]:
                return False
            else:
                pass
        elif isinstance(req['form'][attr], int) and isinstance(cap['form'][attr], int):
            if req[attr] > cap[attr]:
                return False
            else:
                pass
        else:
            return False
    # Capability can accommodate resource
    return True



def satisfy_task(res, task):

    for req in task:
        match = 0
        for cap in res:
            if req['type'] == cap['type']:
                if satisfy_form(req, cap) == True:
                    match = 1
            if match = 0:
                return False
    # Resource capabilities can satisfy all task requirements
    return True


def satisfy_wkd(wkd, res_list):

    for task_id, task in wkd.iteritems():
        match = 0
        for res_id, res in res_list.iteritems():
            if satisfy_task(res, task) == True:
                match = 1
        if match = 0:
            return False
    # There is at least one resource in res_list which can run each task in wkd        
    return True


############################################################################################


def max_execution_time(res, task):

    exec_time = 0

    for req in task:
        for cap in res:
            if req['type'] == cap['type']:
                for attr in req['form'].keys():
                    if satisfy_form(req, cap) == True:
                        exec_time += req['amount'] / cap['rate']

    return exec_time


def min_execution_time(res, task)

    exec_time = 0

    for req in task:
        tmp_exec_time = 0
        for cap in res:
            if req['type'] == cap['type']:
                for attr in req['form'].keys():
                    if satisfy_form(req, cap) == True:
                        tmp_exec_time = req['amount'] / cap['rate']
                    if tmp_exec_time > exec_time:
                        exec_time = tmp_exec_time

    return exec_time


def affinity(task, res, exec_time_metric):
    
    return exec_time_metric(res, task)



def res_select(task, viable_res_list,  exec_time_metric):

    best_res = ""
    best_res_aff = -1000000000      #Suppose to represent minus infinity

    for res_id, res in viable_res_list.iteritems():
        res_aff = affinity(res, task, exec_time_metric)
        if res_aff > best_res_aff:
            best_res_aff = res_aff
            best_res = res_id
    
    return best_res


############################################################################################

if __name__ == "__main__":

    fname = sys.argv[1]
    #wkd = read_workload(fname)
    #pprint(wkd)
    #res_list = read_res_list(fname)
    #pprint(res_list)


