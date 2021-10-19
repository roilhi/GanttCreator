import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel('ForGantt_Creator.xlsx')

#Project Start Date
proj_start = df.start.min()
#Number of days from project start to task start
df['start_num'] = (df.start-proj_start).dt.days
# Number of days from project start to end of tasks
df['end_num'] = (df.end-proj_start).dt.days
# Days between start and end of each task
df['days_start_to_end'] = df.end_num - df.start_num

def color(row):
    c_dict = {'General':'#E64646', 'Brackets':'#E69946','Obstruction':'#34D05C','Solid State':'#34D0C3'}
    return c_dict[row['Family product']]

df['color'] = df.apply(color, axis=1)

from matplotlib.patches import Patch
fig, ax = plt.subplots(1, figsize=(16,6))

# Set background 
ax.patch.set_facecolor('#36454F')
fig.patch.set_facecolor('#36454F')

# Days between start and current progression of each task
df['current_num'] = (df.days_start_to_end*df.completion)
# bars
ax.barh(df.Task, df.current_num, left=df.start_num, color=df.color)
ax.barh(df.Task, df.days_start_to_end, left=df.start_num, color=df.color, alpha=0.5)

# Texts 
for idx, row in df.iterrows():
    ax.text(row.end_num+0.1, idx, f"{int(row.completion*100)}%", va='center', alpha=0.8, color='w')

# grid lines
ax.set_axisbelow(True)
ax.xaxis.grid(color='w', linestyle='dashed', alpha=0.2, which='both')

# # Legends 
c_dict = {'General':'#E64646', 'Brackets':'#E69946','Obstruction':'#34D05C','Solid State':'#34D0C3'}
legend_elements = [Patch(facecolor=c_dict[i], label=i) for i in c_dict]

leg = plt.legend(loc= "upper right", handles=legend_elements, ncol = len(c_dict), facecolor='#36454F')
for text in leg.get_texts():
    text.set_color("white")


## Thicks
xticks = np.arange(0, df.end_num.max()+1,3)
xticks_labels = pd.date_range(proj_start,end=df.end.max()).strftime("%m/%d")
xticks_minor = np.arange(0, df.end_num.max()+1,1)

ax.set_xticks(xticks)
ax.set_xticks(xticks_minor, minor=True)
ax.set_xticklabels(xticks_labels[::3], rotation=90, color='w')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(colors='white', which='both')



plt.setp([ax.get_xticklines()], color='w')
ax.set_xlim(0, df.end_num.max())
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_position(('outward',10))
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_color('w')
#ax.set_xticks([])
#ax.set_yticks([])


plt.suptitle('MY gantt kpi PROJECTS', color='w')


plt.savefig('gantt.png', facecolor='#36454F', bbox_inches='tight')

plt.show()

