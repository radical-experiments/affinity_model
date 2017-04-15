import os                                                                                                                                                                                                   
import sys 
import glob
from pprint import pprint as pprint
import radical.utils as ru
import radical.pilot as rp
import radical.analytics as ra


src = sys.argv[1]
json_file = glob.glob('%s/*.json' % src)[0]

json = ru.read_json(json_file)
sid = os.path.basename(json_file)[:-5]

print 'sid: %s' % sid 

session = ra.Session(sid, 'radical.pilot', src=src)

'''
s_desc = session.describe('state_model', etype=['unit'])
#s_desc = session.describe()

pprint.pprint(s_desc)
'''
ses_unit = session.get(etype=['unit'])
#pprint(s_desc)

unit_id_l = [ses_unit[i].uid for i in range(len(ses_unit))]
#pprint(unit_id_l)
#pprint(session.filter(uid=[unit_id_l[0]], inplace=True).as_dict())
#unit_exec_time = session.filter(uid=unit_id_l[3], inplace=True).duration(state=[rp.AGENT_EXECUTING, rp.AGENT_STAGING_OUTPUT_PENDING])
#pprint(unit_exec_time)

unit_exec_time = list()

for unit_id in unit_id_l:
    try:
        unit_time = session.filter(uid=unit_id, inplace=False).duration(state=[rp.AGENT_EXECUTING, rp.AGENT_STAGING_OUTPUT_PENDING])
        print "%s %f" % (unit_id, unit_time)
        #unit_exec_time.append(unit_time)
    except:
        print "unit %s did not execute" % unit_id

#pprint(unit_exec_time)

