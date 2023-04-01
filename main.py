import time
import secure
import mainsail as m
import mainsail_gate as mg
from env_setup import gat_rul_val

# Validate rules
gat_rul_val.run()
#
# # MAIN:
mg.line_chassis()
mg.mod_container_size_type('20DH')

secure.login('Mainsail', "Admin")
time.sleep(10)
m.home('Tools', 'Gate')
mg.select_transaction('Full In')
mg.line_popup('DEV')
mg.fill_trucker_data()
time.sleep(10)
mg.fill_data(mg.request_data(mg.read_transaction_form()))
time.sleep(15)
