import os
import cherrypy
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib
import seaborn as sns
from scipy.stats import ks_2samp



sns.set(style='whitegrid', rc={"grid.linewidth": 0.9, "xtick.labelsize" : 12, 
                               "ytick.labelsize" : 12, "font.family":'Times New Roman', "boxplot.boxprops.color": "black"})


plt.rcdefaults()
sns.set(style='whitegrid', rc={"grid.linewidth": 0.9, "xtick.labelsize" : 12, 
                               "ytick.labelsize" : 12, "font.family":'Times New Roman', "boxplot.boxprops.color": "black"})


font1 = {'family': 'Calibri',
         'weight': 'bold',
         'size': 20}

font2 = {'family': 'Calibri',
         'weight': 'bold',
         'size': 16}

font3 = {'family': 'Calibri',
         'weight': 'bold',
         'size': 12}

matplotlib.use('agg')

class WebApp(object):
    @cherrypy.expose
    def index(self):
        # Generate HTML for file upload form
        html = '''
        <html>
        <head>
        <title>Analytics Service</title>
        </head>
        <body>
        <center>
        <h1>Energy Insights (Half-hourly data) - Experimental</h1>
        <form method="post" enctype="multipart/form-data" action="/upload">
        <input type="file" name="myFile" />
        <br><br>
        <input type="submit" />
        </form>
        </center>
        </body>
        </html>
        '''

        # Set the content type to "text/html"
        cherrypy.response.headers['Content-Type'] = 'text/html'

        # Return the file upload form
        return html

    @cherrypy.expose
    def upload(self, myFile):
        # Read the contents of the uploaded file
        xls_data = myFile.file.read()

        # Load the XLS data into a pandas DataFrame
        xls = pd.ExcelFile(BytesIO(xls_data))
        df = pd.read_excel(xls,'Data')
#        df = pd.read_excel(BytesIO(xls_data))
        heads=list(df)

        #plot Daily Consumption
        plt.figure()
        df[heads[3]].plot.bar(alpha=0.7,facecolor='r',edgecolor='k', title=heads[3],
                            xlabel='Days', ylabel='Energy (Wh)')
        plt.savefig('results/im1.png',dpi=200,bbox_inches = 'tight')

        # df[heads[3]].plot.hist(alpha=0.7,facecolor='r',edgecolor='k', title=heads[3],
        #                       xlabel='Days', ylabel='Energy (Wh)', bins=30)



        #plot Maximun demand
        plt.figure()
        df[heads[2]].plot.bar(alpha=0.7,facecolor='b',edgecolor='k', title=heads[2],
                            xlabel='Days', ylabel='Energy (kWh)')
        plt.savefig('results/im2.png',dpi=200,bbox_inches = 'tight')


        # df[heads[2]].plot.hist(alpha=0.7,facecolor='b',edgecolor='k', title=heads[2],
        #                       xlabel='Days', ylabel='Energy (kWh)', bins=30)


        #select on the time-energy data values
        df_new=df.iloc[:,4:52].copy()
        vmin=df[heads[2]].min()
        vmax=df[heads[2]].max()

        plt.figure()
        ax=sns.heatmap(df_new,cmap='RdYlGn_r', linewidths=0.5, annot=False,
                    robust=True, vmin=vmin ,vmax=vmax)
        ax.set(xlabel="Time", ylabel="Days", title="Monthly usage profile")
        plt.savefig('results/im3.png',dpi=200,bbox_inches = 'tight')



        # daily demand profile
        plt.figure()
        for i in range(0,len(df_new)):
            df_new.iloc[i,:].plot(rot='vertical', xlabel='Time', ylabel='Demand (kWh)',
                                title='Daily demand profile')
        plt.savefig('results/im4.png',dpi=200,bbox_inches = 'tight')



        plt.figure(figsize=([32,12]))
        ax=sns.boxenplot(data=df_new)
        ax.set_ylabel('Energy consumption (kWh)', **font2)
        ax.set_xlabel('Time', **font2)
        ax.set_title("Monthly half-hourly consumption profile", **font1)
        ax.tick_params(axis='x', rotation=70)
        plt.savefig('results/im5.png',dpi=200,bbox_inches = 'tight')



        # Read the dataframe from a CSV file
        # df = pd.read_csv('dataframe.csv', header=None)
        dist_df = pd.DataFrame(columns=df_new.columns)
        dist=[]
        pval=[]
        # Calculate the distance between distributions of each column
        for col in df_new.columns:
            d, p = ks_2samp(df_new[col], df_new.mean())
            # print(f"Column {col}: Distance = {d:.4f}, p-value = {p:.4f}")
            dist.append(d)
            pval.append(p)


        pval=pd.DataFrame(pval)

        if pval.max()[0]<0.05:
            print("Probably Anomalous")
            s="Probably Anomalous"
        else:
            print("Most likely normal")
            s="Most likely normal"


        plt.figure()
        pval.plot.kde()
        plt.text(pval.max(),60,s,bbox=dict(facecolor='cyan', alpha=0.5))
        # plt.text(0.05,65,"Cutoff limit (anomalous if < 0.05)",bbox=dict(facecolor='red', alpha=0.5))
        # plt.stem(0.05,60,'r')
        plt.xlim([-0.02,0.08])
        plt.savefig('results/im6.png', dpi=200, bbox_inches = 'tight')
        plt.show()

        # Generate HTML for the plot and file upload form
        html = f'''
        <html>
        <body>
        <h1>Analysis</h1>
        <h3>A. Consumption Patterns</h3>
        <p>By analyzing half-hourly energy data, you can identify patterns in energy consumption 
        throughout the day, week, or month. For example, you may see that energy consumption is 
        highest during peak hours, or that energy usage varies based on weather conditions.</p>
        <img src="results/im1.png" width="480" border="0">
        <img src="results/im2.png" width="480" border="0">
        <br><br>

        <h3>B. Load Profile</h3>
        <p>Load profiling is the process of identifying the typical load or energy consumption pattern 
        of a building or group of buildings. By analyzing half-hourly energy data, you can create load 
        profiles that show how energy consumption varies over time, which can help you identify opportunities 
        for energy savings or efficiency improvements.</p>
        <img src="results/im3.png" width="480" border="0">
        <img src="results/im4.png" width="480" border="0">
        <img src="results/im5.png" width="1020" border="0">
        <br><br>
        <h3>C. Anomaly Detection</h3>
        <img src="results/im6.png" width="480" border="0">
        <h1>Upload Another XLS File</h1>
        <form method="post" enctype="multipart/form-data" action="/upload">
        <input type="file" name="myFile" />
        <br><br>
        <input type="submit" />
        </form>
        </body>
        </html>
        '''

        # Set the content type to "text/html"
        cherrypy.response.headers['Content-Type'] = 'text/html'

        # Return the HTML page with the plot and file upload form
        return html

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Set up site-wide config first so we get a log if errors occur.
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080, })

    conf = {'/results': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(current_dir, 'results')}}
    cherrypy.quickstart(WebApp(), config=conf)
