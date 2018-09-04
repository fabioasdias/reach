from glob import glob
import sys
from os.path import join
from subprocess import call

if len(sys.argv)!=2:
    folder='res'
else:
    folder=sys.argv[1]

for tsv in glob(join(folder,'*.tsv')):
    print(tsv)
    call('python3 makeGeojson.py data/cb_2016_us_zcta510_500k.shp {0}'.format(tsv),shell=True)
