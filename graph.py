import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint


domain = [4e7,8e7,16e7,32e7,64e7,128e7,256e7,512e7,1024e7]
blockwidth=list(map(lambda x: str(x),[2,4,8,16,32,64,128,256,512,1024]))
rows = len(domain)
columns = len(blockwidth)
with open("outfile") as fp:
    lines = fp.readlines()
    lines = np.reshape(lines, (columns, rows))
    lines=np.array([list(map(lambda x: float(x.split("\n")[0]), line)) for line in lines])
    fp.close()

crop=0
for i,line in enumerate(lines):
    plt.plot(domain[crop:], line[crop:], label=str(blockwidth[i]))
    plt.scatter(domain[crop:], line[crop:])       

plt.xscale('log', base=2)
plt.title("Gassian Kernel on 8-1024 threads/block (NVIDIA RTX-2070-Super) \n Problem size vs compute time")
plt.xlabel("log size of X (ints)")
plt.ylabel("time (s)")
plt.grid(True,linestyle=":")
plt.legend(title="blockwidth")
plt.savefig("experiment.jpg")


plt.show()
data = np.vstack([domain, lines]).T


np.savetxt('outfile.csv', data, delimiter=',',header="n/blockwidth,"+','.join(blockwidth),fmt='%.6e')