import gearman
import json
import sys
from codeprison.exec_code import exec_code

gm_worker = gearman.GearmanWorker(['localhost:4730'])

def run(gearman_worker, gearman_job):

	data = json.loads(gearman_job.data)

	code = data['code']
	language = data['language'].lower()

	result = exec_code(language, code);

	return json.dumps(result)

gm_worker.set_client_id('cloud-compiler')
gm_worker.register_task('run', run)

gm_worker.work()
