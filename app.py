import os
import cherrypy
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib

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
        <h1>Energy Insights (Half-hourly data)</h1>
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

        # Return the file upload form
        return html

    @cherrypy.expose
    def upload(self, myFile):
        # Read the contents of the uploaded file
        xls_data = myFile.file.read()

        # Load the XLS data into a pandas DataFrame
        df = pd.read_excel(BytesIO(xls_data))
        df_new=df.iloc[:,4:52].T
        # axes = df_new.iloc[1:40,1:6].plot.bar(rot=0, subplots=True)
        # axes[1].legend(loc=2) 

        # Generate a plot of the data
        # plt.plot(df_new.iloc[:,:12])
        # plt.plot(df['x'], df['y'])
        # plt.xlabel('x')
        # plt.ylabel('y')
        plt.figure(figsize=(18,200))
        axes = df_new.iloc[:,:50].plot.kde(subplots=True)
        axes[1].legend(loc=2)
        y_axis=axes[1].axes.get_yaxis()
        y_axis.set_visible(False)
        plt.savefig("results/in1.png",dpi=200)

        plt.figure(figsize=(18,200))
        axes = df_new.iloc[:,:50].plot.bar(rot=0, subplots=True)
        axes[1].legend(loc=2) 
        plt.savefig("results/in2.png",dpi=200)
        # plt.show()

        # Write the plot to a PNG image buffer
        # img_buffer = BytesIO()
        # plt.savefig(img_buffer, format='png')
        # img_buffer.seek(0)

        # Generate HTML for the plot and file upload form
        html = f'''
        <html>
        <body>
        <h1>Result Plot</h1>
        <img src="results/in2.png" width="720" border="0">
        <img src="results/in1.png" width="720" border="0">
        <br><br>
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
