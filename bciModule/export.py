import subprocess
import time
p =subprocess.Popen(['python3', 'live_advance.py'], stdout=open('test3.txt', 'w'))
p.wait(5)
print('done')
#print('time start')
#time.sleep(5)
#p.terminate()
#p.wait()
#print('time stop')


