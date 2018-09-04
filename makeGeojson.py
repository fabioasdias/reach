import fiona
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
import json
import sys

if len(sys.argv)!=3:
    print('.py shp list.tsv')
    exit(-1)

shp=sys.argv[1]
tsv=sys.argv[2]


wiggle=1e-5 #about half a street - used to close gaps 

z2c={}
with open(tsv,'r') as ftsv:
    for line in ftsv:
        z,c = line.strip().split('\t')
        if (z[0]!='1') and (z[0]!='0') and (z[0]!='2'):
            continue
        # if (z[:2]=='22') or (c[:2]=='22')or (z[:2]=='20') or (c[:2]=='20'):
        z2c[z]=c


geoms={}
with fiona.open(shp, 'r') as source:
    for feat in source:
        z=feat['properties']['ZCTA5CE10']
        if (z in z2c):
            c=z2c[z]
        else:
            continue
            # c=-1

        if c not in geoms:
            geoms[c]=[]
        geoms[c].append(shape(feat['geometry']).buffer(wiggle))

for c in geoms:
    # print('merging ',c)
    geoms[c]=(unary_union(geoms[c])).buffer(-1.0625*wiggle)
    if (not geoms[c].is_valid):
        geoms[c]=geoms[c].buffer(0)


print('save')
out={}
out["type"]= "FeatureCollection"
out["features"]= []
for c in geoms:
    out['features'].append({'type': "Feature",
                            'geometry':mapping(geoms[c]), 
                            'properties':{'centre':c}})

print('saving')
with open(tsv.replace('.tsv','.json'),'w') as fout:
    json.dump(out,fout)#,indent=4, sort_keys=True)