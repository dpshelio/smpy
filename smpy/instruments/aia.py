"""
This is where the class for SDO/AIA is defined
"""

__author__ = "David Perez-Suarez"
__email__ = "d.perezsuarez -?- tcd.ie"

from sunpy.map import sdo
from sunpy.net.util import download_file
import matplotlib.pyplot as plt
from smpy.images import Images, DownloadFailed
import numpy as np

class AIA(Images):
    """ AIA magic

    """
    def __init__(self, wavelength):
        self.wavelength = wavelength
    
    def download_latest(self, directory):
        aia_latest_url = 'http://jsoc.stanford.edu/data/aia/synoptic/mostrecent/'
        aia_file =  'AIAsynoptic%4.4i.fits' % self.wavelength
        aia_latest_url += aia_file
        try:
            return download_file(aia_latest_url,directory)
        except Exception:
            raise
            raise DownloadFailed
                
    @classmethod
    def download_by_date(cls, date):
        """ Downloading (image clossest to noon?) using vso? """
        return

    @classmethod
    def preprocess(cls,map):
        mp = map.max() - map
        return mp
#    def sm_plot(cls,file,ars=None):
#        """ Plot images as SM does """
