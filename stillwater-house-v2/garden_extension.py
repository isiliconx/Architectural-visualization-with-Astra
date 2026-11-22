"""Stillwater V2: garden extension, executed in the base Blender generator's globals."""
_gr = random.Random(241607)
_ground_z = -.17

def _rect(name, x0,x1,y0,y1, top, thickness, mat, bevel=.018):
    return cube(name,((x0+x1)/2,(y0+y1)/2,top-thickness/2),(x1-x0,y1-y0,thickness),mat,bevel)

def _pavers(name,x0,x1,y0,y1,z,cols,rows,mat,joint=.018):
    dx,dy=(x1-x0)/cols,(y1-y0)/rows
    for ix in range(cols):
        for iy in range(rows):
            x,y=x0+ix*dx,y0+iy*dy
            _rect(name,x+joint/2,x+dx-joint/2,y+joint/2,y+dy-joint/2,z,.12,mat,.009)

def _rim(name, x0,x1,y0,y1,w,z,d,mat):
    _rect(name,x0-w,x1+w,y0-w,y0,z,d,mat,.015)
    _rect(name,x0-w,x1+w,y1,y1+w,z,d,mat,.015)
    _rect(name,x0-w,x0,y0,y1,z,d,mat,.015)
    _rect(name,x1,x1+w,y0,y1,z,d,mat,.015)

lawnmat=textured('Garden | Fine fescue lawn',(.065,.100,.027),(.17,.205,.058),5,.89,.34,.036)
grounds=textured('Garden | Hill-country ground',(.066,.082,.032),(.16,.16,.072),2.8,.95,.23,.045)
selfdraining=textured('Garden | Sand-washed aggregate',(.25,.22,.165),(.43,.38,.30),38,.94,.44,.045)
poolplaster=textured('Pool | Mineral sea-glass plaster',(.024,.145,.13),(.070,.265,.23),5.9,.54,.12,.018)
poolwater=material('Pool | Lightly rippled clear water',(.91,.98,.98),.083)
_pw_nodes=poolwater.node_tree.nodes
_pw_links=poolwater.node_tree.links
_pw=_pw_nodes.get('Principled BSDF')
_pw.inputs['Transmission Weight'].default_value=1
_pw.inputs['IOR'].default_value=1.333
_pwcoord=_pw_nodes.new('ShaderNodeTexCoord')
_pwnoise=_pw_nodes.new('ShaderNodeTexNoise')
_pwnoise.inputs['Scale'].default_value=5.7
_pwnoise.inputs['Detail'].default_value=3
_pwnoise.inputs['Roughness'].default_value=.56
_pw_links.new(_pwcoord.outputs['Object'],_pwnoise.inputs['Vector'])
_pwb=_pw_nodes.new('ShaderNodeBump')
_pwb.inputs['Strength'].default_value=.17
_pwb.inputs['Distance'].default_value=.037
_pw_links.new(_pwnoise.outputs['Fac'],_pwb.inputs['Height'])
_pw_links.new(_pwb.outputs['Normal'],_pw.inputs['Normal'])
_pool_led=material('Pool | Warm-white recessed lamps',(.59,.88,.90),.24)
_ple=_pool_led.node_tree.nodes.get('Principled BSDF')
_ple.inputs['Emission Color'].default_value=(.56,.86,1,1)
_ple.inputs['Emission Strength'].default_value=2.4

# A meshed site plane omits the three excavations. Pool walls and fire-pit floor
# close their own openings instead of being hidden behind an unbroken ground cube.
active=collections['05 Water garden']
_cutouts=[(-4,10,-14.5,-9.5),(-11.3,-5.7,-16.0,-10.4),(12.9,16.1,-18.9,-15.9)]
_gx=sorted(set([-116,116]+[p for x0,x1,y0,y1 in _cutouts for p in (x0,x1)]))
_gy=sorted(set([-116,116]+[p for x0,x1,y0,y1 in _cutouts for p in (y0,y1)]))
_gv=[(x,y,_ground_z) for y in _gy for x in _gx]
_gf=[]
for j,(ya,yb) in enumerate(zip(_gy,_gy[1:])):
    for i,(xa,xb) in enumerate(zip(_gx,_gx[1:])):
        x,y=(xa+xb)/2,(ya+yb)/2
        if not any(x0<x<x1 and y0<y<y1 for x0,x1,y0,y1 in _cutouts):
            k=j*len(_gx)+i
            _gf.append((k,k+1,k+1+len(_gx),k+len(_gx)))
mesh_obj('Earth plane with excavated pool and lounge wells',_gv,_gf,[grounds])

active=collections['04 Terrace']
_rect('Continuous garden gallery slab',-7.05,15.8,-4.4,-.81,.295,.425,travertine,.035)
_pavers('Gallery terrace | staggered limestone field',-7.03,15.78,-4.39,-.83,.315,18,3,travertine)
for i,(edge,z) in enumerate([(-4.77,.24),(-5.13,.16),(-5.49,.08)]):
    _rect('Gallery descent | long cantilevered tread',-4.2,8.65,edge,-4.36,z,.17,travertine,.022)
    if i!=2:
        cube('Gallery descent | recessed bronze reveal',(2.225,edge-.004,z-.07),(12.8,.014,.023),bronze,.004)
_rect('Central terrace | upper landing',-4.63,10.52,-9.1,-5.39,.079,.20,selfdraining,.018)
_pavers('Central terrace | limestone slabs',-4.65,10.55,-9.15,-5.35,.107,13,3,travertine)
_rect('East gallery link',10.52,14.2,-7.8,-4.39,.105,.18,travertine,.025)
_pavers('East gallery link | joints',10.53,14.18,-7.78,-4.41,.112,3,3,travertine)
_rect('West walk | aggregate base',-8.58,-7.0,-10.5,-2.18,-.04,.16,selfdraining,.02)
_pavers('West walk | floating slabs',-8.58,-7.0,-10.42,-2.19,.038,1,8,travertine,.155)
_rect('East garden allée',18.26,19.4,-22.75,-2.86,-.045,.15,selfdraining,.03)
_pavers('East garden allée | stepping panels',18.27,19.39,-22.65,-3.1,.022,1,18,travertine,.13)

def _chaise(x,y,z,angle=0):
    local=[(-.33,-.92,.24,.053,1.98,.11,woodlight),(.33,-.92,.24,.053,1.98,.11,woodlight)]
    def _pos(a,b,c):
        return (x+a*cos(angle)-b*sin(angle),y+a*sin(angle)+b*cos(angle),z+c)
    for xx in [-.34,.34]:
        for yy in [-.75,.73]:
            rod('Pool chaise | tapered teak leg',_pos(xx,yy,.015),_pos(xx,yy,.315),.042,woodlight,.029)
        rod('Pool chaise | side rail',_pos(xx,-.92,.255),_pos(xx,.93,.255),.035,woodlight)
        rod('Pool chaise | hinged back frame',_pos(xx,.36,.34),_pos(xx,.91,.66),.028,woodlight)
    cube('Pool chaise | linen seat cushion',_pos(0,-.31,.354),(.68,1.38,.15),linen,.065,rot=(0,0,angle))
    cube('Pool chaise | raised linen back',_pos(0,.63,.493),(.68,.71,.145),linen,.06,rot=(.52,0,angle))
    cube('Pool chaise | rolled sage headrest',_pos(0,.84,.678),(.50,.18,.11),sage,.05,rot=(.52,0,angle))
for lx,ly in [(-2.85,-7.52),(-1.5,-7.63),(6.1,-7.55),(7.47,-7.6)]:
    _chaise(lx,ly,.117)
for lx in [-2.155,6.785]:
    cyl('Pool terrace | travertine side table',(lx,-7.7,.30),.272,.36,travertine,40,.055)
    lathe('Pool terrace | handmade ceramic cup',(lx,-7.7,.488),[(.036,0),(.05,.012),(.054,.11),(.049,.112),(.045,.02)],ceramic,20)
# Slim parasol tilted away from the main sightline.
for _x,_y in [(-3.5,-6.75),(8.04,-6.75)]:
    cyl('Parasol | bronze socket',( _x,_y,.159),.21,.09,bronze,36,.022)
    rod('Parasol | bronze mast',(_x,_y,.18),(_x,_y,2.64),.034,bronze)
    _rv=[(_x,_y,2.68)]
    for kr in [1,2,3]:
        for i in range(12):
            a=2*pi*i/12
            r=kr*.42
            _rv.append((_x+r*cos(a),_y+r*sin(a),2.68-.08*kr-.05*(kr==3)))
    _rf=[(0,i+1,(i+1)%12+1) for i in range(12)]
    for j in range(2):
        for i in range(12):
            a=1+j*12+i;b=1+j*12+(i+1)%12
            _rf.append((a,a+12,b+12,b))
    _r=mesh_obj('Parasol | tailored oyster fabric',_rv,_rf,[linen])
    _r.modifiers.new('Fabric thickness','SOLIDIFY').thickness=.012
    for i in range(12):
        a=2*pi*i/12
        rod('Parasol | radial rib',(_x,_y,2.62),(_x+1.23*cos(a),_y+1.23*sin(a),2.37),.009,bronze)
    sphere('Parasol | bronze finial',(_x,_y,2.693),(.052,.052,.045),bronze,12,8)

active=collections['05 Water garden']
# Steps run down through the west end of the basin; sea-glass plaster is visible through the surface.
def _basin(tag,x0,x1,y0,y1,top,water_z,bottom,w):
    _rim(tag+' | basin plaster',x0,x1,y0,y1,.115,top-.05,top-bottom,poolplaster)
    _rect(tag+' | plaster floor',x0-.11,x1+.11,y0-.11,y1+.11,bottom,.14,poolplaster,.015)
    _rim(tag+' | mitred limestone coping',x0,x1,y0,y1,w,top,.13,travertine)
    mesh_obj(tag+' | rippled clear surface',[(x0-.002,y0-.002,water_z),(x1+.002,y0-.002,water_z),(x1+.002,y1+.002,water_z),(x0-.002,y1+.002,water_z)],[(0,1,2,3)],[poolwater])
_basin('Fourteen-meter swimming pool',-4,10,-14.5,-9.5,.104,-.008,-1.22,.28)
for i in range(4):
    x=-3.99+i*.43
    _rect('Pool | broad submerged entry step',x,x+.44,-14.49,-9.51,-.13-i*.23,1.1-i*.23,poolplaster,.015)
    cube('Pool | inset entry tread marker',(x+.37,-11.99,-.127-i*.23),(.024,4.82,.012),travertine,.005)
for x in [-.75,2.65,6.05,9.04]:
    cube('Pool | recessed underwater lamp',(x,-14.489,-.36),(.205,.02,.107),_pool_led,.029)
    area('Pool wall | underwater glow',(x,-14.45,-.34),19,(.62,.86,1),.24,(x,-12.8,-1.13))
_rect('Pool | south waterfront promenade',-4.3,10.31,-15.93,-14.76,.058,.18,travertine,.027)
_pavers('Pool | promenade laid limestone',-4.29,10.29,-15.91,-14.77,.070,13,1,travertine)
_rect('Pool | west dry perimeter',-4.98,-4.25,-14.88,-9.09,.077,.213,travertine,.018)
_rect('Pool | east dry perimeter',10.27,11.51,-15.91,-9.08,.073,.23,travertine,.022)
_basin('Separate limestone spa',12.9,16.1,-18.9,-15.9,.305,.195,-.73,.29)
for y in [-18.89,-16.17]:
    _rect('Spa | submerged bench',12.91,16.09,y,y+.26,-.135,.58,poolplaster,.06)
for x in [13.2,13.76,14.34,14.92,15.5,15.82]:
    cube('Spa | circular bronze jet collar',(x,-15.896,.039),(.09,.037,.085),bronze,.029)
_rect('Spa | entry step',13.18,15.82,-15.67,-15.22,.159,.21,travertine,.025)
_rect('Spa | west connection',11.49,12.65,-19.15,-14.23,.052,.18,travertine,.018)
_pavers('Spa | pebble terrace',12.67,16.38,-15.2,-13.58,.082,3,2,travertine)
_pavers('Spa | south lounging terrace',12.5,17.47,-21.01,-19.18,.074,5,2,travertine)
# Three glazed ceramic jars provide a softer silhouette beside the geometric spa.
for x,y,h,r in [(16.8,-17.96,.82,.41),(17.44,-18.32,.55,.29),(17.62,-17.7,.34,.22)]:
    lathe('Spa garden | hand-thrown jar',(x,y,-.127),[(r*.6,0),(r*.91,.11),(r,h*.5),(r*.63,h*.86),(r*.56,h),(r*.42,h),(r*.43,h*.82)],ceramic,36)

# West-side social fire court, with open entrance on the house side.
_fire_x,_fire_y=-8.5,-13.2
_firefloor=-.56
_rect('Sunken fire court | stone floor',-11.3,-5.7,-16,-10.42,_firefloor,.21,selfdraining,.02)
_pavers('Sunken fire court | limestone paving',-11.29,-5.71,-15.99,-10.43,-.537,7,7,travertine)
for xa,xb,ya,yb in [(-11.53,-11.1,-16.2,-10.4),(-5.9,-5.49,-16.2,-10.4),(-11.1,-5.9,-16.19,-15.82),(-11.1,-9.48,-10.64,-10.24),(-7.51,-5.9,-10.64,-10.24)]:
    _rect('Fire court | honed limestone retaining wall',xa,xb,ya,yb,.116,.69,stone,.025)
for i in range(4):
    _rect('Fire court | entry stair',-9.47,-7.52,-10.64-i*.27,-10.36-i*.27,-.054-i*.12,.18,travertine,.012)
# Built-in oak bench lingers along two quieter edges, leaving the top stair open.
for x in [-10.75,-6.28]:
    cube('Fire court | seating plinth',(x,-13.59,-.34),(.75,3.68,.37),stone,.039)
    for i in range(4):
        y=-14.93+i*.89
        cube('Fire court | upholstered seat',(x,y,-.085),(.69,.85,.15),linen,.064)
        cube('Fire court | upholstered back',(x+(-.30 if x< -9 else .30),y,.13),(.15,.82,.40),sage,.043)
cube('Fire court | rear bench plinth',(_fire_x,-15.46,-.34),(4.06,.71,.37),stone,.038)
for x in [-10.04,-9.02,-8,-6.98]:
    cube('Fire court | rear upholstered seat',(x,-15.45,-.085),(.97,.66,.15),linen,.064)
    cube('Fire court | rear upholstered back',(x,-15.72,.13),(.96,.16,.39),sage,.045)
    if x in [-10.04,-8]:
        cube('Fire court | woven lumbar pillow',(x+.19,-15.57,.147),(.42,.2,.27),rust,.057,rot=(.21,0,.11))
lathe('Fire court | bronze lined fire bowl',(_fire_x,_fire_y,-.53),[(.30,0),(.46,.13),(.73,.36),(.82,.43),(.79,.46),(.70,.45),(.49,.26),(.26,.22)],blackstone,64)
cyl('Fire court | recessed bronze burner',(_fire_x,_fire_y,-.208),.38,.06,bronze,48,.018)
embers=material('Fire court | warm embers',(.8,.15,.028),.7)
_ep=embers.node_tree.nodes.get('Principled BSDF')
_ep.inputs['Emission Color'].default_value=(1,.21,.028,1)
_ep.inputs['Emission Strength'].default_value=1.5
for i in range(13):
    a=_gr.uniform(0,2*pi); r=_gr.uniform(.05,.29)
    sphere('Fire court | ember',(_fire_x+r*cos(a),_fire_y+r*sin(a),-.173),(.052,.032,.034),embers,9,6)
for i in range(5):
    a=_gr.uniform(0,2*pi);r=_gr.uniform(.043,.23)
    x,y=_fire_x+r*cos(a),_fire_y+r*sin(a)
    rod('Fire court | natural split-wood fuel',(x-.17,y-.05,-.18),(x+.17,y+.09,-.102),.076,bark,.058)
area('Fire court | ember bounce',(_fire_x,_fire_y,.155),70,(1,.23,.055),.65,(_fire_x-1.75,_fire_y,.07))

active=collection('09 Outdoor dining pavilion')
# Detached pavilion, detailed as a shaded garden room rather than a second house.
_pavers('Pavilion | terrace paving',11.42,17.86,-13.51,-7.81,.143,6,5,travertine)
_rect('Pavilion | grounded terrace plinth',11.37,17.92,-13.58,-7.75,.128,.34,travertine,.043)
_rect('Pavilion | entrance tread',11.66,17.59,-13.92,-13.55,.055,.22,travertine,.018)
for x in [11.82,17.59]:
    for y in [-13.19,-8.1]:
        cube('Pavilion | blackened bronze post',(x,y,1.64),(.16,.16,3.00),charcoal,.015)
        cube('Pavilion | bronze footing plate',(x,y,.155),(.265,.265,.03),bronze,.012)
for y in [-13.22,-8.07]:
    cube('Pavilion | continuous fascia',(14.705,y,3.105),(6.3,.225,.24),charcoal,.023)
for x in [11.51,17.90]:
    cube('Pavilion | returning bronze fascia',(x,-10.645,3.105),(.23,5.39,.24),charcoal,.021)
for i in range(26):
    x=11.74+i*.238
    cube('Pavilion | deep oak solar louver',(x,-10.645,3.14),(.117,5.18,.145),woodlight,.009)
for y in [-12.3,-11.03,-9.36]:
    cube('Pavilion | louver support',(14.71,y,3.03),(6.26,.085,.10),charcoal,.008)

cube('Pavilion kitchen | limestone wind screen',(17.66,-10.63,.85),(.22,4.94,1.47),stone,.021)
for i in range(19):
    cube('Pavilion kitchen | slatted oak privacy screen',(17.68,-12.71+i*.228,2.25),(.09,.10,1.37),wood,.008)
cube('Pavilion kitchen | basalt worktop',(17.17,-10.67,1.13),(.81,4.38,.105),blackstone,.025)
cube('Pavilion kitchen | oak carcass',(17.19,-10.67,.63),(.72,4.24,.89),wood,.021)
for i in range(7):
    y=-12.47+i*.60
    cube('Pavilion kitchen | solid oak cabinet door',(16.80,y,.65),(.05,.575,.80),woodlight,.009)
    cube('Pavilion kitchen | bronze pull',(16.763,y,.93),(.017,.235,.024),bronze,.007)
cube('Pavilion kitchen | black grill hob',(17.17,-11.92,1.189),(.612,.77,.019),charcoal,.03)
for k in range(10):
    cube('Pavilion kitchen | recessed grill bar',(17.17,-12.241+k*.072,1.208),(.534,.021,.026),bronze,.006)
cube('Pavilion kitchen | undermount sink',(17.17,-9.42,1.185),(.49,.59,.012),charcoal,.029)
curve('Pavilion kitchen | bronze faucet',[(17.46,-9.42,1.2),(17.44,-9.42,1.51),(17.24,-9.42,1.58),(17.15,-9.42,1.45)],.017,bronze)
lathe('Pavilion kitchen | terra-cotta oil bottle',(17.12,-10.31,1.19),[(.055,0),(.084,.028),(.086,.23),(.047,.29),(.04,.37),(.035,.36)],terracotta,32)
cube('Pavilion | outdoor dining table top',(14.08,-10.83,.977),(1.06,2.79,.108),woodlight,.075)
for y in [-11.88,-9.78]:
    cube('Pavilion | dining table stone trestle',(14.08,y,.539),(.63,.22,.78),travertine,.028)
for x,angle in [(13.16,pi/2),(14.99,-pi/2)]:
    for y in [-11.82,-10.84,-9.86]:
        before=set(bpy.data.objects)
        dining_chair(x,y,angle)
        for o in set(bpy.data.objects)-before:
            if o.type=='EMPTY':
                o.location.z=-.191
for y in [-11.57,-10.07]:
    rod('Pavilion | bronze pendant cable',(14.08,y,3.015),(14.08,y,2.23),.007,charcoal)
    lathe('Pavilion | spun bronze pendant',(14.08,y,2.115),[(.23,0),(.213,.046),(.093,.129),(.054,.172)],bronze,40)
    cyl('Pavilion | opal pendant diffuser',(14.08,y,2.112),.19,.012,led,40,.002)
    area('Pavilion | warm pendant light',(14.08,y,2.09),70,(1,.69,.40),.34,(14.08,y,.985))
lathe('Pavilion | vase on table',(14.08,-10.87,1.033),[(.09,0),(.129,.041),(.144,.16),(.07,.23),(.056,.36),(.046,.37),(.043,.23)],ceramic,32)
for dx,dy in [(.117,.097),(-.08,-.082),(.083,-.117)]:
    curve('Pavilion | vase stems',[(14.08,-10.87,1.35),(14.08+dx,-10.87+dy,1.53),(14.08+dx*1.7,-10.87+dy*1.7,1.64)],.005,bark)
for y in [-11.78,-10.85,-9.89]:
    for x in [13.79,14.38]:
        cyl('Pavilion | stoneware place setting',(x,y,1.043),.16,.016,ceramic,32,.007)
        cube('Pavilion | folded sage napkin',(x,y+.013,1.054),(.11,.172,.022),sage,.013,rot=(0,0,.08))

active=collections['06 Planting']
def _bed(name, xa,xb,y0,y1,wa,wb,seed,mat=soil):
    rr=random.Random(seed);pts=[];mids=[]
    for i in range(21):
        t=i/20;x=xa+(xb-xa)*t+.19*sin(t*3*pi);y=y0+(y1-y0)*t
        taper=.39+.61*sin(pi*t)**.55
        w=(wa+(wb-wa)*t)*taper
        pts.extend([(x-w*.5,y,-.125),(x+w*.5,y,-.125)])
        if 0<i<20:
            mids.append((x,y,w))
    mesh_obj(name,pts,[(i,i+1,i+3,i+2) for i in range(0,len(pts)-2,2)],[mat])
    return mids

# Quiet open fescue is balanced by layered borders. The outer site remains more natural.
_lawnpoly=[(-6.8,-16.53),(-4.96,-16.24),(7.3,-16.24),(9.65,-16.83),(10.48,-18.49),(10.31,-21.11),(9.05,-22.85),(6.87,-23.47),(-3.98,-23.47),(-6.73,-22.48),(-7.65,-20.83),(-7.72,-18.09)]
mesh_obj('Lower lawn | clipped fescue clearing',[(x,y,-.137) for x,y in reversed(_lawnpoly)],[tuple(range(len(_lawnpoly)))],[lawnmat])
_rect('Lawn walk | drifted gravel landing',-5.06,11.48,-16.29,-15.94,-.085,.12,selfdraining,.02)
for k in range(12):
    x=-7.45+k*1.61;y=-24+.35*sin(k*.37)
    _rect('Lawn walk | individual floating limestone slab',x-.65,x+.65,y-.36,y+.36,.005,.15,travertine,.038)

# Elliptical shrub trunks and each leaflet occupy the same editable mesh for low overhead.
hedgemats=[material('Garden | Myrtle foliage '+str(i),c,.81) for i,c in enumerate([
    (.031,.066,.019),(.064,.12,.035),(.12,.19,.063),(.17,.235,.089),(.10,.137,.061)])]
cipm=[material('Garden | Cypress scale '+str(i),c,.86) for i,c in enumerate([
    (.023,.045,.026),(.04,.071,.035),(.062,.103,.053),(.082,.12,.060)])]
flowerbright=[material('Garden | Salvia florets '+str(i),c,.83) for i,c in enumerate([
    (.17,.09,.24),(.25,.13,.36),(.31,.20,.45),(.45,.30,.47),(.58,.48,.40),(.78,.64,.48)])]
garden_grass=[material('Garden | Meadow grass blade '+str(i),c,.88) for i,c in enumerate([
    (.10,.143,.044),(.20,.26,.087),(.28,.31,.13),(.36,.33,.16),(.47,.38,.197),(.13,.20,.07)])]

def _gmesh(name,quads,mats):
    vs=[];fs=[];ids=[]
    for verts,mid in quads:
        k=len(vs)
        vs.extend(verts)
        fs.append(tuple(range(k,k+len(verts))))
        ids.append(mid)
    return mesh_obj(name,vs,fs,mats,ids)

def _shrub_cloud(name,patches,mats=hedgemats):
    qs=[]
    for x,y,z,rx,ry,h,num in patches:
        # Vary angle, height and radial density; dense inner leaves hide artificial hollows.
        for i in range(num):
            a=_gr.random()*2*pi; t=_gr.random()*pi*.52
            q=_gr.uniform(.54,1.02)
            rip=1+.12*sin(5*a+1.1)+.10*sin(9*a-1.4)
            x0=x+cos(a)*rx*cos(t)*q*rip
            y0=y+sin(a)*ry*cos(t)*q*rip
            zz=z+h*(.09+.91*sin(t))*_gr.uniform(.82,1.07)
            le=_gr.uniform(.036,.09);wi=le*_gr.uniform(.35,.64)
            dr=Vector((cos(a),sin(a),_gr.uniform(.35,1.3))).normalized()*le
            sx=Vector((-sin(a)*wi,cos(a)*wi,0))
            p=Vector((x0,y0,zz))
            qs.append(((p-dr,p+sx,p+dr,p-sx),_gr.randrange(len(mats))))
    return _gmesh(name,qs,mats)

def _cypress(x,y,h,r,name):
    rod(name+' | trunk',(x,y,-.14),(x+.025,y+.02,h*.69),r*.23,bark,r*.07)
    gs=[]
    profile=[(.02,.43),(.11,.69),(.27,.95),(.43,1),(.59,.91),(.73,.68),(.86,.48),(.96,.19),(1.02,.032)]
    mvs=[]
    for i,(t,wid) in enumerate(profile):
        for j in range(16):
            a=j*2*pi/16
            radius=r*wid*(.9+.21*sin(j*2.7+i*.49))
            mvs.append((x+cos(a)*radius,y+sin(a)*radius,-.12+h*t))
    mfs=[(i*16+j,i*16+(j+1)%16,(i+1)*16+(j+1)%16,(i+1)*16+j) for i in range(len(profile)-1) for j in range(16)]
    mesh_obj(name+' | tapered foliage core',mvs,mfs,cipm,[(_gr.randrange(2) if j%3 else 2) for j in range(len(mfs))])
    for i in range(2500):
        a=_gr.random()*2*pi; t=_gr.random()**.91
        for (lo,r0),(hi,r1) in zip(profile,profile[1:]):
            if t<hi:
                rw=r0+(r1-r0)*max(0,t-lo)/(hi-lo)
                break
        rr=r*rw*_gr.uniform(.84,1.16)*(1+.15*sin(16*a+3*t))
        p=Vector((x+cos(a)*rr,y+sin(a)*rr,-.13+h*t))
        le=_gr.uniform(.055,.14);wi=le*.41
        dr=Vector((cos(a)*le*.37,sin(a)*le*.37,le))
        s=Vector((-sin(a)*wi,cos(a)*wi,0))
        gs.append(((p-dr,p+s,p+dr,p-s),_gr.randrange(4)))
    _gmesh(name+' | close-knit spray foliage',gs,cipm)

for i,(x,y,h,r) in enumerate([(-14.1,-9.45,6.3,.63),(-15.36,-8.13,7.1,.69),(-13.25,-7.6,5.55,.57),(-15.15,3.75,6.90,.66),(20.4,-7.6,5.95,.61),(19.09,3.52,7.2,.71),(20.99,5.41,7.5,.74),(16.1,8.6,6.0,.61)]):
    _cypress(x,y,h,r,'Italian cypress %02d'%(i+1))

# Sculptural olive trunks frame views from the house but do not block the elevation.
for i,(x,y,h,r) in enumerate([(-10.8,-4.1,4.45,1.63),(-12.7,-17.5,4.65,1.75),(-10.55,-23.0,3.75,1.48),(12.45,-22.0,4.25,1.59),(20.15,-15.71,3.85,1.44),(18.0,-2.4,4.2,1.6),(-10.5,6.65,5.35,1.76),(4.7,8.2,4.4,1.59),(11.56,8.6,4.4,1.59)]):
    olive('Garden olive %02d'%(i+1),(x,y,-.12),h,r)
# Subdivide foliage by planting border so each drift can be independently moved.
_west=_bed('West border | meandering dark soil',-14.5,-10.88,-23.14,-2.60,5.5,4.8,11)
_east=_bed('East border | fragrant strata',19.32,19.48,-24.75,3.10,3.9,3.8,12)
_south=[(-9.1+i*1.09,-24.63,.68) for i in range(19)]
_galleft=[(-9.3,-3.1+i*.54,1.0) for i in range(10)]
_poolsouth=[(-3.75+i*1.1,-16.40,.54) for i in range(13)]
_lawnwest=[(-7.93,-28+i*.84,1.15) for i in range(5,14)]
for idx,(name,beds) in enumerate([
    ('West border',_west),('East border',_east),('South lawn border',_south),('Gallery west raised border',_galleft),('Poolside perennial drift',_poolsouth),('Lower court transition',_lawnwest)]):
    q=[];blooms=[];shrubs=[]
    for i,(cx,cy,ww) in enumerate(beds):
        jor=idx in [2,4]
        if i%3==0 and not jor:
            sx=cx+_gr.uniform(-.18,.18)*ww;sy=cy+_gr.uniform(-.23,.23)
            shrubs.append((sx,sy,-.125,_gr.uniform(.39,.79),_gr.uniform(.53,.89),_gr.uniform(.48,.99),720))
        for k in range(4 if jor else 9):
            x=cx+_gr.uniform(-.43,.43)*ww;y=cy+_gr.uniform(-.45,.47)
            tuft=_gr.uniform(.65,1.1)*(.56 if idx==4 else 1)
            for blade in range(_gr.randint(18,39)):
                an=_gr.random()*2*pi
                rr=_gr.uniform(0,.14)*tuft;w=_gr.uniform(.006,.018)*tuft;h=_gr.uniform(.18,.58)*tuft;a=_gr.uniform(.055,.25)*tuft
                pos=Vector((x+rr*cos(an),y+rr*sin(an),-.127))
                side=Vector((-sin(an)*w,cos(an)*w,0))
                mid=pos+Vector((cos(an)*a*.33,sin(an)*a*.33,h*.55))
                end=pos+Vector((cos(an)*a,sin(an)*a,h))
                mi=_gr.randrange(len(garden_grass))
                q.extend([((pos-side,pos+side,mid+side*.64,mid-side*.64),mi),((mid-side*.64,mid+side*.64,end),mi)])
            if (i+idx)%3==1:
                for flower in range(5):
                    dx,dy=_gr.uniform(-.16,.16),_gr.uniform(-.16,.16)
                    th=_gr.uniform(.23,.52)*tuft
                    pos=Vector((x+dx,y+dy,-.125))
                    h0=pos+Vector((dx*.28,dy*.38,th))
                    q.append(((pos-Vector((.006,0,0)),pos+Vector((.006,0,0)),h0+Vector((.003,0,0)),h0-Vector((.003,0,0))),0))
                    mid=idx%3 if idx in [0,1,4] else 4+_gr.randrange(2)
                    for m in range(4):
                        z=m*.023*tuft
                        a=_gr.random()*2*pi
                        cx0,cy0=h0.x+.012*cos(a),h0.y+.012*sin(a)
                        d=.018*tuft
                        verts=[(cx0-d,cy0,h0.z+z),(cx0,cy0-d,h0.z+z),(cx0+d,cy0,h0.z+z),(cx0,cy0+d,h0.z+z),(cx0,cy0,h0.z+z+.034*tuft)]
                        for f in range(4):
                            blooms.append(((verts[f],verts[(f+1)%4],verts[4]),mid))
    _gmesh(name+' | tufted grasses',q,garden_grass)
    _gmesh(name+' | flowering perennial heads',blooms,flowerbright)
    if shrubs:
        _shrub_cloud(name+' | clipped myrtle understory',shrubs)
# A repeated but non-uniform grove hedge softens the eastern perimeter wall.
_shrub_cloud('East perimeter | mature loose hedge',[(20.55,-21.76+i*1.14,-.135,_gr.uniform(.53,.76),_gr.uniform(.57,.84),_gr.uniform(.71,1.23),770) for i in range(21)])
_shrub_cloud('Fire court border | fragrant bushes',[(-11.63,-15.89+i*.78,-.12,.59,.58,_gr.uniform(.58,1.1),750) for i in range(7)])
_shrub_cloud('Spa | ground-hugging myrtle',[(16.87,-16.14-i*.49,-.135,.31,.34,_gr.uniform(.26,.55),410) for i in range(6)])

active=collections['05 Water garden']
_rect('North enclosure | low garden back wall',-15.9,20.4,8.75,9.11,1.26,1.47,stone,.038)
_rect('North enclosure | honed stone coping',-15.94,20.44,8.71,9.15,1.37,.14,travertine,.02)
_rect('East enclosure | planting background',21.28,21.6,-23.12,9.10,1.01,1.31,stone,.035)
_rect('East enclosure | subtle coping',21.23,21.65,-23.17,9.14,1.13,.14,travertine,.022)
for i in range(25):
    y=-22.65+i*1.29
    cube('Perimeter | stone expansion joint',(21.273,y,.47),(.005,.012,1.05),selfdraining,0)
# Low lamps extend the architecture's bronze and warm light into the garden.
active=collections['07 Lighting']
for x,y,z in [(-8.5,-7.6,.055),(-9.86,-10.1,-.08),(-5.75,-16.55,-.07),(-7.9,-20.14,-.09),(10.95,-16.09,.04),(11.52,-19.62,-.05),(18.25,-20.8,-.09),(18.2,-13.76,-.05),(11.15,-7.98,.04),(8.79,-5.12,.06),(-4.46,-5.19,.06)]:
    cube('Garden wayfinder | bronze bollard',(x,y,z+.225),(.092,.092,.45),bronze,.014)
    cube('Garden wayfinder | warm diffuser',(x,y-.048,z+.357),(.06,.019,.081),led,.006)
    cube('Garden wayfinder | deep bronze hood',(x,y-.018,z+.405),(.11,.135,.037),bronze,.013)
    area('Garden wayfinder | discreet ground wash',(x,y-.069,z+.347),10,(1,.64,.34),.109,(x,y-.66,z-.01))
for x,y,tx,ty,tz,power in [(-11.1,-3.87,-10.8,-4.1,1.6,65),(18.44,-2.79,18,-2.4,2.2,65),(-13.65,-10.18,-14.1,-9.45,2.6,50),(12.16,-22.45,12.45,-22,2.2,60)]:
    cyl('Garden uplight | flush bronze ring',(x,y,-.111),.112,.047,bronze,24,.007)
    area('Garden uplight | sculptural tree graze',(x,y,-.078),power,(1,.69,.39),.15,(tx,ty,tz))
