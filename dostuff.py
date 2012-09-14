# coding: utf-8
import os
from tempfile import mkdtemp
from datetime import date
from smpy.instruments.aia import AIA

temp_dir = mkdtemp()
date_dir = os.path.join(*["%02d" % getattr(date.today(), x) for x in ["year", "month", "day"]])
dated_dir = os.path.join('/tmp/sm',date_dir)
if not os.path.isdir(dated_dir):
    os.makedirs(dated_dir)

ars = {'10920':[100,100],'10921':[-100,-100]}

aias = map(AIA, [94, 131, 171, 193, 211]) 
#gongs = map(Gong, ['int','mag'])
instruments = aias #+ gongs
for inst in instruments:
    inst.do_all(temp_dir,dated_dir,ars)
                

