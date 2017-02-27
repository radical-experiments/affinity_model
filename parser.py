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

            if (req_type != 'compute') and (req_type != 'memory') and (req_type != 'storage') and (req_type != 'network'):
                #The type of the requirement is not allowed
                return False

            ## Checking the amount of consumables required is represented correctly
            if 'amount' in req_type_list:
                # Network looks at data sent AND received. Thus, there are two separate 'amount' values must be specified 
                if req_type == 'network':
                    if (type(req_type_list['amount']) == list) and \\
                        (len(req_type_list['amount']) == 2):
                        if (type(req_type_list['amount'][0]) == int) and \\
                            (req_type_list['amount'][0] > 0) and \\
                            (type(req_type_list['amount'][1]) == int) and \\
                            (req_type_list['amount'][1] > 0):
                            pass
                        else:
                            #In Task task_id, requirement type network, the amount of consumables are not both positive integers
                            return False
                    else:
                        #In Task task_id, requirement type network, the amount of consumables is not a list of length 2
                        return False
                else:
                    if (req_type_list['amount'] > 0) and \\
                        (type(req_type_list['amount'] == int):
                        pass
                    else:
                        #In Task task_id, requirement type `not network`, the amount of consumables is not a positive integer
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
                    if 'co-located threads' in req_type_list['form']:
                        if (req_type_list['form']['co-located threads'] > 0) and \\
                            (type(req_type_list['form']['co-located threads']) == int):
                            pass
                        else:
                            #In Task task_id, requirement type compute, number of co-located threads is not a positive integer
                    else:
                        #In Task task_id, requirement type compute, number of co-located threads is not specified
                        return False
                    # Checking machine ISA
                    if 'machine ISA' in req_type_list['form']:
                        pass
                        ## TODO: This part checks the possible machine ISA available
                    else:
                        #In Task task_id, requirement type compute, no machine ISA specified
                        return False

                elif req_type == "memory":
                    pass
                    if 'max memory usage' in req_type_list['form']:
                        ## TODO: Let user specify unit of memory (B, KB, MB, GB, etc...)
                        if (req_type_list['form']['max memory usage'] > 0) and \\
                            (type(req_type_list['form']['max memory usage']) == int):
                            pass
                        else:
                            #In Task task_id, requirement type memory, max amount of memory used is not a positive integer
                            return False
                    else:
                        #In Task task_id, requirement type memory, max amount of memory used during execution not specified
                        return False

                elif req_type == "storage":
                    pass
                    if 'max storage usage' in req_type_list['form']:
                        if (req_type_list['form']['max storage usage'] > 0) and \\
                            (type(req_type_list['form']['max storage usage']) == int):
                            pass
                        else:
                            #In Task task_id, requirement type storage, max amount of storage used is not a positive integer
                            return False
                    else:
                        #In Task task_id, requirement type storage, max amount of storage used during execution not specified
                        return False

                elif req_type == "network":
                    pass
                    if 'downlink protocol' in req_type_list['form']:
                        pass
                        # TODO: This part checks the possible L2 protocol for downlink
                    else:
                        #In Task task_id, requirement type network, L2 protocol for downlink is not specified
                        return False

                    if 'uplink protocol' in req_type_list['form']:
                        pass
                        # TODO: This part checks the possible L2 protocol for uplink
                    else:   
                        #In Task task_id, requirement type network, L2 protocol for uplink is not specified
                        return False

                else:
                    #In Task task_id, there is an entry for an unknown consumable type
                    return False

            else:
                #In Task task_id, requirement type req_type, the form of the consumables is not specified
                pass

        #Workload structure passes all current checks
        return True


def is_chunk_list(chunk_list):

    pass

    for chunk_id, chunk in chunk_list.iteritems():
        if not chunk:
            # Chunk has no rates
            pass        
        for rate_type, rate_type_list in chunk.iteritems():

            if (rate_type != 'compute') and (rate_type != 'memory') and (rate_type != 'storage') and (rate_type != 'network'):
                #In Chunk chunk_id, there is a rate of a type which we don't recognize
                return False

            if 'rate' in rate_type_list:
                if rate_type == 'network':
                    pass
                    if (type(rate_type_list['rate']) == list) and \\
                        (len(rate_type_list['rate']) == 2):
                        if (type(rate_type_list['rate'][0]) == int) and \\
                            (rate_type_list['rate'][0] > 0) and \\
                            (type(rate_type_list['rate'][1] == int) and \\
                            (rate_type_list['rate'][1] > 0):
                            pass
                        else:
                            #In Chunk chunk_id, rate type network, the downlink [0] and uplink [0] rates are not positive integers
                            return False
                    else:
                        #In Chunk chunk_id, rate type network, the rate is not a list of length 2
                        return False
                else:
                    if (rate_type_list['rate'] > 0) and \\
                        (type(rate_type_list['rate'] == int):
                        pass
                    else:
                        #In Chunk chunk_id, rate type, rate_type, rate is not a positive integer
                        return False
            else:
                #In Chunk chunk_id, rate type rate_type, no rate is specified
                return False

            if 'form' in rate_type_list:
                if rate_type == 'compute':
                    pass
                    if 'co-located threads' in rate_type_list['form']:
                        if (type(rate_type_list['form']['co-located threads']) == int) and \\
                            (rate_type_list['form']['co-located threads'] > 0):
                            pass
                        else:
                            #In Chunk chunk_id, rate type compute, number of co-located threads is not a positive integer
                            return False
                    else:
                        #In Chunk chunk_id, rate type compute, number of co-located threads is not specified
                        return False

                    if 'machine ISA' in rate_type_list['form']:
                        pass
                        # TODO: This part checks the machine ISA
                    else:
                        #In Chunk chunk_id, rate type compute, no machine ISA is specified
                        return False

                elif rate_type == 'memory':
                    pass
                    if 'maximum memory offered' in rate_type_list['form']:
                        if (type(rate_type_list['form']['maximum memory offered']) == int) and \\
                            (rate_type_list['form']['maximum memory offered'] > 0):
                            pass
                        else:
                            #In Chunk chunk_id, rate type memory, amount of maximum memory offered is not a positive integer
                            return False
                    else:
                        #In Chunk chunk_id, rate type memory, amount of maximum memory offered is not specified
                        return False

                elif rate_type == 'storage':
                    pass
                    if 'maximum storage offered' in rate_type_list['form']:
                        if (type(rate_type_list['form']['maximum storage offered']) == int) and \\
                            (rate_type_list['form']['maximum storage offered'] > 0):
                            pass
                        else:
                            #In Chunk chunk_id, rate type storage, amount of maximum storage offered is not a positive integer
                            return False
                    else:
                        #In Chunk chunk_id, rate type storage, amount of maximum storage offered is not specified
                        return False


                elif rate_type == 'network':
                    pass
                    if 'downlink protocol' in rate_type_list['form']:
                        pass
                        # TODO: This part checks the L2 protocols for downlink
                    else:
                        #In Chunk chunk_id, rate type network, the L2 protocol for downlink is not specified
                        return False

                    if 'uplink protocol' in rate_type_list['form']:
                        pass
                        # TODO: This part checks the L2 protocols for uplink
                    else:
                        #In Chunk chunk_id, rate type network, the L2 protocol for uplink is not specified
                        return False
                else:
                    #In Chunk chunk_id, there is an entry for an unknown rate type
                    return False
            else:
                #In Chunk chunk_id, rate type, rate_type, no form is specified
                return False

        # Chunk list passes all current checks
        return True
                

def read_workload(filename):

    with open(filename, 'r') as j:
        workload = json.load(j)

    if is_workload(workload):
        return workload
    else:
        return None

def read_chunk_list(filename):

    with open(filename, 'r') as j:
        chunk_list = json.load(j)

    if is_chunk_list(chunk_list):
        return chunk_list
    else:
        return None



if __name__ == "__main__":

    fname = sys.argv[1]
    read_workload(fname)
