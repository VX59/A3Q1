import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
table = pd.read_csv("outfile.csv").to_numpy()
ns = [row[0] for row in table]
table = [row[1:] for row in table]
table = np.array(table)

# Sp = T1/Tp
# rows are runtime for each core count
# divide each row by row[0]
n = [4e7,8e7,16e7,32e7,64e7,128e7,256e7,512e7,1024e7]
p=[2,4,8,16,32,64,128,256,512,1024]
sp_table = []
i=0
for row in table:
    t1 = row[0]
    sp_row = list(map(lambda x: t1/x, row))
    plt.scatter(p,sp_row)
    plt.plot(p, sp_row,label="n "+str(n[i]/1e6)+"e7")
    sp_table.append(sp_row)
    i+=1
sp_table = np.array(sp_table)
plt.xscale('log', base=2)

plt.legend()
plt.ylabel("Speedup")
plt.xlabel("Blockwidth")
plt.title("Gaussian Kernel Speedup vs Threads/Block")
plt.savefig("speedup.jpg")
plt.show()

import pandas as pd
sp_df = pd.DataFrame(sp_table)
np.savetxt('sp_outfile.csv', sp_df, delimiter=',',fmt='%.6e')

# Ep = Sp/p
# rows are divided into speedup for each core count
# divide each row by p
ep_table = []

i=0
sp_table_t = list(np.transpose(sp_table))
for i in range(len(table)):
    ep_row = sp_table_t[i] / p[i]
    ep_table.append(ep_row)
    i+=1

ep_table = list(np.transpose(ep_table))
i=0
for row in ep_table:
    plt.plot(p[1:], row, label="n "+str(n[i]/1e7)+"e7")
    plt.scatter(p[1:],row)
    i+=1

ep_df = pd.DataFrame(ep_table)
np.savetxt('ep_outfile.csv', ep_df, delimiter=',',fmt='%.6e')

plt.xscale('log', base=2)

plt.legend()
plt.ylabel("Efficiency")
plt.xlabel("Blockwidth")
plt.title("Gaussian Kernel Efficiency vs Threads/Block")
plt.savefig("efficiency.jpg")
plt.show()

print(ep_table)