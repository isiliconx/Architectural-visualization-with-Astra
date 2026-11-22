"""Landform and distant grove, loaded after garden_extension.py."""
active=collections['06 Planting']
for _north_wall in ('North enclosure | low garden back wall','North enclosure | honed stone coping'):
    bpy.data.objects[_north_wall].location.y+=2.01

_hillmat=textured('Landscape | Silvery olive foothills',(.103,.118,.080),(.174,.184,.123),8,.98,.08,.045)
_hillmuted=textured('Landscape | Distant hazed ridge',(.119,.145,.133),(.194,.215,.187),5,.97,.05,.03)

def _hillgauss(x,y,xc,yc,sx,sy):
    return math.exp(-((x-xc)/sx)**2-((y-yc)/sy)**2)

def _hillz(x,y):
    # Site is graded flat up to the house and western walk. Beyond that,
    # broad ridges and saddles rise without a hard seam at the garden boundary.
    n=max(0,min(1,(y-11.2)/13))
    w=max(0,min(1,(-x-17)/17))
    mask=1-(1-n*n*(3-2*n))*(1-w*w*(3-2*w))
    profile=(.46+5.5*_hillgauss(x,y,-40,34,25,29)+4.6*_hillgauss(x,y,32,50,32,24)+
             7.0*_hillgauss(x,y,-31,82,58,27)+8.2*_hillgauss(x,y,46,96,54,30)+
             2.7*_hillgauss(x,y,-65,-6,28,29)+.72*sin(x*.107+y*.129)+.46*cos(x*.18-y*.14))
    return -.20+max(0,profile)*mask

_hxs=list(range(-115,112,3))
_hys=list(range(-67,121,3))
_hv=[(x,y,_hillz(x,y)) for y in _hys for x in _hxs]
_hf=[];_hi=[]
for j,y in enumerate(_hys[:-1]):
    for i,x in enumerate(_hxs[:-1]):
        if max(_hillz(x,y),_hillz(x+3,y),_hillz(x,y+3),_hillz(x+3,y+3))<-.169:
            continue
        k=j*len(_hxs)+i
        _hf.append((k,k+1,k+1+len(_hxs),k+len(_hxs)))
        _hi.append(1 if y>51 or x < -59 else 0)
_terrain_backdrop=mesh_obj('Foothills | rolling contours beyond Stillwater',_hv,_hf,[_hillmat,_hillmuted],_hi)
for _face in _terrain_backdrop.data.polygons:
    _face.use_smooth=True

for i,(x,y,h,r) in enumerate([(-19.2,11.6,4.9,1.7),(-29.4,8.7,5.3,1.8),(-17.5,19.1,5.1,1.9),(9.8,21.6,4.7,1.8),(23.5,16.7,4.75,1.9)]):
    olive('Hillside olive %02d'%(i+1),(x,y,_hillz(x,y)),h,r)

# Three narrow cypress silhouettes along the western ridge. Their bases are lifted to the local grade.
for i,(x,y,h,r) in enumerate([(-26.5,14.1,5.5,.65),(-31.2,17.3,6.0,.66),(-29.8,21.3,5.15,.48),(-16.5,13.5,5.7,.62)]):
    prior=set(bpy.data.objects)
    _cypress(x,y,h,r,'Foothill cypress %02d'%(i+1))
    for o in set(bpy.data.objects)-prior:
        o.location.z+=_hillz(x,y)+.14
