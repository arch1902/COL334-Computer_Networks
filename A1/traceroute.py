import subprocess
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys

domain = input()

ip_addresses = []
hop_num = []
rtt = []
i = 1
max_hops = 100

while(True):
    if i>max_hops:
        break
    print("Hop Number",i)
    process = subprocess.Popen(['ping', '-m', str(i),'-c','10', domain], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
    hop_num.append(i)
    i += 1
    output = process.stdout.readlines()
    process.terminate()
    s = output[1].strip()
    temp = s.split(' ')
    #print(temp)
    if temp[-1]=='0':
        print("Request Timeout")
        ip_addresses.append('0')
        continue
    if temp[3][0].isdigit():
        ip_addresses.append(temp[3][:-1])
    else:
        ip_addresses.append(temp[4][1:-2])

    print("IP:",ip_addresses[-1])

    if temp[-1]=='ms':
        break
   
######################################################################################
for i in range(len(ip_addresses)):
    print("Processing plot ",str(i+1)+"/"+str(len(ip_addresses)))
    if ip_addresses[i]=='0':
        rtt.append(0)
        continue
    process = subprocess.Popen(['ping','-c','10', ip_addresses[i]], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
    output = process.stdout.readlines()
    process.terminate()
    s = output[1].strip()
    temp = s.split(' ')
    #print(temp)
    if temp[-1]=='0':
        rtt.append(0)
    else:
        t = temp[6]
        rtt.append(float(t[5:]))
        print(rtt[-1])

    #print(temp)
    #print(output[1].strip().split(' ')[3])


#Plotting the Graph
plt.plot(hop_num, rtt)
 
plt.xlabel('Hop Number')
plt.ylabel('RTT(ms)')

plt.title('RTT vs Hop Number')

plt.show()
