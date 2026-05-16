import seaborn as sns
import matplotlib.pyplot as plt
from pprint import pprint


fmri = sns.load_dataset("fmri")
sns.lineplot(x="timepoint", y="signal", hue="region", data=fmri)
pprint(type(fmri))
plt.show()

tips = sns.load_dataset("tips")
sns.scatterplot(x="total_bill", y="tip", hue="day", data=tips)
# plt.show()

tips = sns.load_dataset("tips")
sns.barplot(x="day", y="total_bill", data=tips)
# plt.show()


tips = sns.load_dataset("tips")
sns.boxplot(x="day", y="total_bill", data=tips)
# plt.show()


plt.plot([0, 1], [10, 11], label='Line 1')
plt.plot([0, 1], [11, 10], label='Line 2')
plt.scatter([0, 1], [10.5, 10.5], color='blue', marker='o', label='Dots')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Simple Line and Dot Plot')
plt.legend()
# plt.show()



