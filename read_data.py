#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 10:03:17 2023

@author: anandarupmukherjee
"""



import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template



# Read the .xls file using xlrd engine
df = pd.read_excel("Dec12a.xls", engine="xlrd")

# Show the contents of the DataFrame
print(df)

df.iloc[:,4:15].plot.hist(alpha=0.5,edgecolor='k') #all days for select hours of operation


df_new=df.iloc[:,4:52].T
axes = df_new.iloc[1:40,1:6].plot.bar(rot=0, subplots=True)
axes[1].legend(loc=2) 


plt.figure(figsize=(12,12))
axes = df_new.iloc[:,:12].plot.kde(subplots=True)
axes[1].legend(loc=2)
plt.axis('off')
plt.savefig("results/in1.png",dpi=200)
plt.show()

# Generate report as HTML page using jinja2
template = Template('''
<html>
<head><title>Data Report</title></head>
<body>
<h1>Energy Insights</h1>
<table>
{% for row in data %}
<tr>
    <td>{{ row[0] }}</td>
    <td>{{ row[1] }}</td>
</tr>
{% endfor %}
</table>
</body>
</html>
''')
html = template.render(data=df_new.iloc[:,:12])

# Save report to file
with open('results/report.html', 'w') as f:
    f.write(html)
# import sweetviz as sv
# my_report = sv.analyze(df)
# my_report.show_html() # Default arguments will generate to "SWEETVIZ_REPORT.html"


