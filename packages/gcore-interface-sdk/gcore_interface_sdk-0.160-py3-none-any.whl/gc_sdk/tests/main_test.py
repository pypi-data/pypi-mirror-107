from gc_sdk.main import MainController
from gc_sdk.tests import settings_test as s
from gc_sdk.tests import functions


mc = MainController(s.api_ip, s.api_port)
response = mc.get_api_methods()
#mc.open_internal_gate()
#mc.close_internal_gate()
#mc.open_external_gate()
#mc.close_external_gate()
#start_weigh_round_test()
#mc.capture_cm_launched()
#mc.capture_cm_terminated()
#functions.change_opened_record_test(mc)
#functions.add_comment_test(mc)
#functions.close_opened_record_test(mc)
#mc.execute_method('get_unfinished_records')
#mc.execute_method('get_health_monitor12')
mc.execute_method('get_last_event', auto_id=61)
print(mc.get_sdk_methods())
