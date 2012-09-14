"""
This is where the classes for each intrument resides
"""

__author__ = "David Perez-Suarez"
__email__ = "d.perezsuarez -?- tcd.ie"

import sunpy.map as maps
import matplotlib.pyplot as plt
from matplotlib.image import BboxImage
import numpy as np
from matplotlib.transforms import IdentityTransform
import os

import matplotlib.patches as mpatches

from matplotlib.offsetbox import AnnotationBbox,\
     AnchoredOffsetbox, AuxTransformBox

from matplotlib.cbook import get_sample_data

from matplotlib.text import TextPath


class PathClippedImagePatch(mpatches.PathPatch):
    """
    The given image is used to draw the face of the patch. Internally,
    it uses BboxImage whose clippath set to the path of the patch.

    FIXME : The result is currently dpi dependent.
    """
    def __init__(self, path, bbox_image, **kwargs):
        mpatches.PathPatch.__init__(self, path, **kwargs)
        self._init_bbox_image(bbox_image)

    def set_facecolor(self, color):
        """simply ignore facecolor"""
        mpatches.PathPatch.set_facecolor(self, "none")

    def _init_bbox_image(self, im):

        bbox_image = BboxImage(self.get_window_extent,
                               norm = None,
                               origin=None,
                               )
        bbox_image.set_transform(IdentityTransform())

        bbox_image.set_data(im)
        self.bbox_image = bbox_image

    def draw(self, renderer=None):


        # the clip path must be updated every draw. any solution? -JJ
        self.bbox_image.set_clip_path(self._path, self.get_transform())
        self.bbox_image.draw(renderer)

        mpatches.PathPatch.draw(self, renderer)



class DownloadFailed(Exception):
    pass


class Images():
    @classmethod
    def preprocess(cls,map):
        return map
    
    def make_map(self,filename):
        my_map = maps.make_map(filename)
        return self.preprocess(my_map)
        
    def sm_plot(self,sm_map,ars=None):
        """ Plot images as SM does """
        map_fig = sm_map.plot(draw_grid=False, colorbar=False)
        arr = np.ones(256).reshape(1,256)
        if ars is not None:
            for ar_number,pos in ars.items():
                text_path = TextPath((0,0),ar_number)
                text_patch = PathClippedImagePatch(text_path, arr, ec="none",
                                                   transform=IdentityTransform())
                shadow1 = mpatches.Shadow(text_patch,1,-1,props=dict(fc="none", ec="0.6", lw=3))
                offsetbox = AuxTransformBox(IdentityTransform())
                offsetbox.add_artist(shadow1)
                offsetbox.add_artist(text_patch)
                
                ab = AnnotationBbox(offsetbox,(pos[0],pos[1]),xycoords='data',frameon=False)
                map_fig.get_axes()[0].add_artist(ab)
#                plt.annotate(ar_number,xy=(pos[0],pos[1]),color='white',weight=600,stretch='condensed')
#                plt.annotate(ar_number,xy=(pos[0],pos[1]),weight=500)
            return map_fig
    def make_smfilename(self,sm_map):
        sm_filename = ("s%s_%05d_fd_%s.png" % 
                       (sm_map.instrument, 
                        sm_map.measurement, 
                        sm_map.date.strftime("%Y%m%d_%H%M%S"),
                        )
                       ).lower()
        return sm_filename

    def do_all(self,tempdir,outdir,ars):
        filename = self.download_latest(tempdir)
        sm_map = self.make_map(filename)
        figure = self.sm_plot(sm_map,ars)
        figure.savefig(os.path.join(outdir,self.make_smfilename(sm_map)))
        return
