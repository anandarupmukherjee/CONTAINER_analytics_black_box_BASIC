import os.path
import cherrypy

class Root:
    @cherrypy.expose
    def index(self):
        return """ <html>
                <head>
                <title>Energy</title>
                </head>
                <html>
                <body>
                <h1>Energy Insights (Half-hourly data)</h1>
                <img src="results/in1.png" width="640" border="0">
                </body>
                </html>"""

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Set up site-wide config first so we get a log if errors occur.
    cherrypy.config.update({'server.socket_host': 'localhost',
                            'server.socket_port': 8080, })

    conf = {'/results': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(current_dir, 'results')}}

    cherrypy.quickstart(Root(), '/', config=conf)