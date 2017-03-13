import json
import sys


def is_workload(workload)
    pass

    if not workload:
        # Workload is empty
        return True

    for task_id, task_reqs in workload.iteritems():
        if not task_reqs:
            # The tasks has no requirements
            continue
        for req_type, req_type_list in task_reqs.iteritems():

            if (req_type != 'compute') and (req_type != 'memory') and (req_type != 'network'):
                #The type of the requirement is not allowed
                return False

            ## Checking the amount of consumables required is represented correctly
            if 'amount' in req_type_list:
                if (req_type_list['amount'] > 0) and \\
                    (type(req_type_list['amount'] == int):
                    pass
                else:
                    #In Task task_id, the amount of consumables is not a positive integer
                    return False
            else:
                #In Task task_id, requirement type req_type, no amount of consumables is specified
                return False

            ## Checking the form of each input
            if 'form' in req_type_list:
                ## For Compute, check if number of co-located threads, and machine ISA is specified 
                if req_type == "compute":
                    pass
                    # Checking co-located threads
                    if 'num_threads' in req_type_list['form']:
                        if (req_type_list['form']['num_threads'] > 0) and \\
                            (type(req_type_list['form']['num_threads']) == int):
                            pass
                        else:
                            #In Task task_id, requirement type compute, number of co-located threads is not a positive integer
                    else:
                        #In Task task_id, requirement type compute, number of co-located threads is not specified
                        return False
                    # Checking machine ISA
                    if 'ISA' in req_type_list['form']:
                        if (type(req_type_list['form']['ISA']) == str):
                            pass
                        else:
                            #In Task task_id, requirement type compute, ISA specified is not a string
                            return False
                    else:
                        #In Task task_id, requirement type compute, no machine ISA specified
                        return False

                elif req_type == "memory":
                    pass
                    if 'max_mem' in req_type_list['form']:
                        ## TODO: Let user specify unit of memory (B, KB, MB, GB, etc...)
                        if (req_type_list['form']['max_mem'] > 0) and \\
                            (type(req_type_list['form']['max_mem']) == int):
                            pass
                        else:
                            #In Task task_id, requirement type memory, max amount of memory used is not a positive integer
                            return False
                    else:
                        #In Task task_id, requirement type memory, max amount of memory used during execution not specified
                        return False

                    if 'device' in req_type_list['form']:
                        if (type(req_type_list['form']['device']) == str):
                            pass
                        else:
                            #In Task task_id, requirement type memory, device is not a string
                            return False
                    else:
                        #In Task task_id, requirement type memory, device is not specified 
                        return False

                elif req_type == "network":
                    pass
                    if 'L2_protocol' in req_type_list['form']:
                        if (type(req_type_list['form']['L2_protocol']) == str):
                            pass
                        else:
                            # In Task task_id, requirement type network, L2 protocol is not a string
                            return False
                    else:
                        #In Task task_id, requirement type network, L2 protocol for downlink is not specified
                        return False

                    if 'direction' in req_type_list['form']:
                        if ((req_type_list['form']['direction']).lower() == 'ul') or //
                            ((req_type_list['form']['direction']).lower() == 'dl'):
                            pass
                        else:
                            #In Task task_id, requirement type network, direction specified is not correct
                            return False
                    else:   
                        #In Task task_id, requirement type network, direction is not specified 
                        return False

                else:
                    #In Task task_id, there is an entry for an unknown consumable type
                    return False

            else:
                #In Task task_id, requirement type req_type, the form of the consumables is not specified
                pass

        #Workload structure passes all current checks
        return True


def is_res_list(res_list):

    pass

    for res_id, res in res_list.iteritems():
        if not res:
            # Resource has no rates
            pass        
        for rate_type, rate_type_list in res.iteritems():

            if (rate_type != 'compute') and (rate_type != 'memory') and (rate_type != 'network'):
                #In Resource res_id, there is a rate of a type which we don't recognize
                return False

            if 'rate' in rate_type_list:
                if (rate_type_list['rate'] > 0) and \\
                    (type(rate_type_list['rate'] == int):
                    pass
                else:
                    #In Resource res_id, rate type, rate_type, rate is not a positive integer
                    return False
            else:
                #In Resource res_id, rate type rate_type, no rate is specified
                return False

            if 'form' in rate_type_list:
                if rate_type == 'compute':
                    pass
                    if 'num_threads' in rate_type_list['form']:
                        if (type(rate_type_list['form']['num_threads']) == int) and \\
                            (rate_type_list['form']['num_threads'] > 0):
                            pass
                        else:
                            #In Resource res_id, rate type compute, number of co-located threads is not a positive integer
                            return False
                    else:
                        #In Resource res_id, rate type compute, number of co-located threads is not specified
                        return False

                    if 'ISA' in rate_type_list['form']:
                        if (type(rate_type_list['form']) == str):
                            pass
                        else:
                            #In Resource res_id, rate type compute, ISA specified is not a string
                            return False
                    else:
                        #In Resource res_id, rate type compute, no machine ISA is specified
                        return False

                elif rate_type == 'memory':
                    if 'max_mem' in rate_type_list['form']:
                        ## TODO: Let user specify unit of memory (B, KB, MB, GB, etc...)
                        if (type(rate_type_list['form']['max_mem']) == int) and \\
                            (rate_type_list['form']['max_mem'] > 0):
                            pass
                        else:
                            #In Resource res_id, rate type memory, amount of maximum memory offered is not a positive integer
                            return False
                    else:
                        #In Resource res_id, rate type memory, amount of maximum memory offered is not specified
                        return False

                    if 'device' in rate_type_list['form']:
                        if (type(rate_type_list['form']['device']) == str):
                            pass
                        else:
                            #In Resource res_id, rate type memory, device specified is not a string
                            return False
                    else:
                        #In Resource res_id, rate type memory, no device specified
                        return False

                elif rate_type == 'network':
                    pass
                    if 'L2_protocol' in rate_type_list['form']:
                        if (type(rate_type_list['form']['L2_protocol']) == str):
                            pass
                        else:
                            #In Resource res_id, rate type network, the L2 protocol is not a string
                            return False
                    else:
                        #In Resource res_id, rate type network, the L2 protocol is not specified
                        return False

                    if 'direction' in rate_type_list['form']:
                        if (rate_type_list['form']['direction'].lower() == 'ul') or \\
                            (rate_type_list['form']['direction'].lower() == 'dl'):
                            pass
                        else:
                            #In Resource res_id, rate type network, the direction specified is not correct
                            return False
                    else:
                        #In Resource res_id, rate type network, no direction specified 
                        return False
                else:
                    #In Resource res_id, there is an entry for an unknown rate type
                    return False
            else:
                #In Resource res_id, rate type, rate_type, no form is specified
                return False

        # Resource list passes all current checks
        return True
                

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



if __name__ == "__main__":

    fname = sys.argv[1]
    read_workload(fname)
