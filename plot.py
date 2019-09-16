with open("plot", "r") as f :
    lines = f.readlines()

mb1 = []
mb2 = []
def epoch_loss_mb1(line):
    items = line.split('-')
    return int(items[3]), float(items[5][:-5])


def epoch_loss_mb2(line):
    items = line.split('-')
    return int(items[4]), float(items[6][:-5])

for line in lines:
    if "mb1" in line:
        mb1.append(epoch_loss_mb1(line))
    else:
        mb2.append(epoch_loss_mb2(line))

print(mb1)
print(mb2)

import numpy as np
import matplotlib.pyplot as plt

mb1 = np.array(mb1)
print(mb1)
plt.plot(mb1)
plt.show()
