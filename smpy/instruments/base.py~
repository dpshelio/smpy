"""
This is where the classes for each intrument resides
"""

__author__ = "David Perez-Suarez"
__email__ = "d.perezsuarez -?- tcd.ie"

import sunpy.map as maps

class Base():

    def sm_plot(cls,file,ars=None):
        """ Plot images as SM does """
        my_map = maps.make_map(file)
        map_fig = my_map.plot()
        plt.annotate('test',xy=(100,100))
        map_fig.savfig('test.png')
