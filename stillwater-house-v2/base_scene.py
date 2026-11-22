"""STILLWATER HOUSE | fully procedural architectural visualization.
Run: blender -b --python build_scene.py -- --output ./output --mode preview
Blender 4.5 LTS. No downloaded assets, textures, add-ons or fonts required.
"""
import bpy, math, random, json, os, sys, argparse, time
from pathlib import Path
from mathutils import Vector
from math import sin, cos, pi

parser = argparse.ArgumentParser()
parser.add_argument('--output', default=str(Path(__file__).parent))
parser.add_argument('--mode', choices=['preview','final','build'], default='final')
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
OUT = Path(args.output).resolve(); (OUT/'renders').mkdir(parents=True,exist_ok=True)
random.seed(20261121)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for mat in list(bpy.data.materials): bpy.data.materials.remove(mat)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'; scene.unit_settings.length_unit='METERS'
scene.render.engine='CYCLES'
scene.cycles.samples=96 if args.mode=='preview' else 256
scene.cycles.use_denoising=True
scene.cycles.max_bounces=10; scene.cycles.diffuse_bounces=4; scene.cycles.glossy_bounces=5; scene.cycles.transmission_bounces=8
scene.cycles.transparent_max_bounces=8
scene.render.threads_mode='FIXED'; scene.render.threads=6
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGB'; scene.render.image_settings.color_depth='8'
scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'
scene.view_settings.look='AgX - Medium High Contrast'
scene.view_settings.exposure=-0.45
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type='OPTIX'; prefs.get_devices()
    for d in prefs.devices: d.use=d.type=='OPTIX'
    scene.cycles.device='GPU'
except Exception as e: print('GPU fallback',repr(e))

collections={}
def collection(name):
    c=bpy.data.collections.new(name);scene.collection.children.link(c);collections[name]=c;return c
for n in ['01 Architecture','02 Living atelier','03 Dining and kitchen','04 Terrace','05 Water garden','06 Planting','07 Lighting','08 Cameras']: collection(n)
active=collections['01 Architecture']
def put(obj):
    for c in list(obj.users_collection):c.objects.unlink(obj)
    active.objects.link(obj)
    return obj

def material(name,color,rough=.6,metal=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    return m

def textured(name,c1,c2,scale=4,rough=.7,bump=.035,dist=.07,stretch=None):
    m=material(name,c1,rough);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    tc=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale;noise.inputs['Detail'].default_value=3;noise.inputs['Roughness'].default_value=.7
    if stretch:
        v=n.new('ShaderNodeVectorMath');v.operation='MULTIPLY';v.inputs[1].default_value=stretch;l.new(tc.outputs['Generated'],v.inputs[0]);l.new(v.outputs['Vector'],noise.inputs['Vector'])
    else:l.new(tc.outputs['Generated'],noise.inputs['Vector'])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.2;ramp.color_ramp.elements[0].color=(*c1,1);ramp.color_ramp.elements[1].position=.8;ramp.color_ramp.elements[1].color=(*c2,1)
    l.new(noise.outputs['Fac'],ramp.inputs['Fac']);l.new(ramp.outputs['Color'],p.inputs['Base Color'])
    micro=n.new('ShaderNodeTexNoise');micro.inputs['Scale'].default_value=220;micro.inputs['Detail'].default_value=2;l.new(tc.outputs['Generated'],micro.inputs['Vector'])
    b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=bump;b.inputs['Distance'].default_value=dist;l.new(micro.outputs['Fac'],b.inputs['Height']);l.new(b.outputs['Normal'],p.inputs['Normal'])
    return m
stone=textured('01 | Honed ivory limestone',(.49,.43,.33),(.72,.66,.54),5,.78,.19,.045)
travertine=textured('02 | Vein-cut travertine',(.40,.34,.25),(.70,.61,.46),5,.61,.14,.03,(1,1,16))
plaster=textured('03 | Warm lime plaster',(.67,.63,.53),(.77,.73,.64),3,.82,.09,.018)
wood=textured('04 | Smoked European oak',(.105,.063,.032),(.28,.17,.083),3,.43,.14,.024,(2,38,3))
woodlight=textured('05 | Oiled ash joinery',(.31,.20,.105),(.53,.37,.21),4,.41,.08,.015,(1,40,2))
linen=textured('06 | Oatmeal boucle',(.57,.53,.44),(.79,.75,.64),8,.95,.34,.012)
sage=textured('07 | Sage linen',(.20,.25,.18),(.35,.39,.27),10,.95,.27,.01)
rust=textured('08 | Tobacco cushion wool',(.26,.105,.045),(.47,.23,.11),6,.91,.22,.01)
charcoal=material('09 | Charcoal anodized aluminium',(.023,.028,.028),.31,.7)
bronze=material('10 | Brushed bronze',(.30,.19,.075),.28,.82)
blackstone=textured('11 | Basalt kitchen stone',(.025,.027,.025),(.067,.069,.06),3,.39,.06,.02)
ceramic=material('12 | Chalk-glazed stoneware',(.71,.68,.57),.3)
terracotta=textured('13 | Handmade terracotta',(.25,.10,.047),(.43,.22,.11),5,.83,.21,.035)
pages=material('14 | Uncoated book paper',(.79,.75,.64),.85)
soil=textured('15 | Dark garden soil',(.04,.035,.021),(.09,.075,.039),8,.98,.4,.08)
gravel=textured('16 | Fine warm gravel',(.12,.12,.095),(.25,.24,.19),48,.93,.6,.08)
water=material('17 | Still-water jade',(.045,.105,.09),.09)
p=water.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=.95;p.inputs['IOR'].default_value=1.333
wNoise=water.node_tree.nodes.new('ShaderNodeTexNoise');wNoise.inputs['Scale'].default_value=7;wNoise.inputs['Roughness'].default_value=.4
wB=water.node_tree.nodes.new('ShaderNodeBump');wB.inputs['Strength'].default_value=.1;wB.inputs['Distance'].default_value=.022
water.node_tree.links.new(wNoise.outputs['Fac'],wB.inputs['Height']);water.node_tree.links.new(wB.outputs['Normal'],p.inputs['Normal'])
glass=material('18 | Low-iron architectural glass',(.86,.94,.92),.035)
p=glass.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.45
bark=textured('19 | Olive bark',(.085,.074,.045),(.21,.18,.11),7,.92,.5,.08)
leaves=[material('20 | Olive leaf '+str(i),c,.73) for i,c in enumerate([(.12,.18,.075),(.21,.28,.13),(.31,.36,.20),(.17,.23,.10)])]
grasses=[material('21 | Grass '+str(i),c,.92) for i,c in enumerate([(.17,.22,.065),(.28,.31,.12),(.37,.36,.18),(.15,.20,.07)])]
lavenders=[material('22 | Lavender '+str(i),c,.8) for i,c in enumerate([(.26,.21,.34),(.35,.28,.44),(.44,.37,.52)])]
led=material('23 | Warm 2700 K emitter',(1,.66,.31),.4)
p=led.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.52,.19,1);p.inputs['Emission Strength'].default_value=4
rug=textured('24 | Woven sand rug',(.43,.37,.27),(.67,.60,.46),12,.98,.27,.015)
bookm=[material('Book cover '+str(i),c,.8) for i,c in enumerate([(.21,.26,.24),(.54,.39,.26),(.10,.12,.13),(.52,.50,.43),(.25,.16,.11)])]


def cube(name,loc,scale,mat,bevel=0,rot=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=put(bpy.context.object);o.name=name;o.dimensions=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if rot:o.rotation_euler=rot
    if mat:o.data.materials.append(mat)
    if bevel:
        mod=o.modifiers.new('Soft crafted edges','BEVEL');mod.width=bevel;mod.segments=3
        mod=o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    return o

def sphere(name,loc,scale,mat,seg=24,rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,radius=1,location=loc);o=put(bpy.context.object);o.name=name;o.scale=scale;o.data.materials.append(mat)
    for f in o.data.polygons:f.use_smooth=True
    return o

def cyl(name,loc,radius,depth,mat,verts=32,bevel=.015):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=radius,depth=depth,location=loc);o=put(bpy.context.object);o.name=name;o.data.materials.append(mat)
    if bevel:
        mod=o.modifiers.new('Edge glint','BEVEL');mod.width=bevel;mod.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    for f in o.data.polygons:f.use_smooth=True
    return o

def rod(name,a,b,r,mat,r2=None):
    mid=(Vector(a)+Vector(b))*.5;d=Vector(b)-Vector(a)
    if r2 is None:o=cyl(name,mid,r,d.length,mat,12,.004)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=12,radius1=r,radius2=r2,depth=d.length,location=mid);o=put(bpy.context.object);o.name=name;o.data.materials.append(mat)
        for p in o.data.polygons:p.use_smooth=True
    o.rotation_euler=d.to_track_quat('Z','Y').to_euler();return o

def curve(name,pts,r,mat,cyclic=False):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=16;cu.bevel_depth=r;cu.bevel_resolution=3
    sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
    for p,co in zip(sp.bezier_points,pts):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
    sp.use_cyclic_u=cyclic;o=bpy.data.objects.new(name,cu);active.objects.link(o);o.data.materials.append(mat);return o

def lathe(name,loc,profile,mat,segments=48):
    verts=[];faces=[]
    for radius,z in profile:
        verts.extend([(loc[0]+radius*cos(2*pi*i/segments),loc[1]+radius*sin(2*pi*i/segments),loc[2]+z) for i in range(segments)])
    for j in range(len(profile)-1):
        for i in range(segments):faces.append((j*segments+i,j*segments+(i+1)%segments,(j+1)*segments+(i+1)%segments,(j+1)*segments+i))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);active.objects.link(o);o.data.materials.append(mat)
    for p in mesh.polygons:p.use_smooth=True
    return o

def area(name,loc,power,color,size,target):
    d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);collections['07 Lighting'].objects.link(o);o.location=loc;d.energy=power;d.color=color;d.shape='DISK';d.size=size;o.visible_glossy=False;o.visible_camera=False;o.visible_transmission=False;d.transmission_factor=0;d.specular_factor=0;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o

def seam(name,center,size,z,mat):
    x,y=center;w,d=size;rr=.10
    pts=[(x-w/2+rr,y-d/2,z),(x+w/2-rr,y-d/2,z),(x+w/2,y-d/2+rr,z),(x+w/2,y+d/2-rr,z),(x+w/2-rr,y+d/2,z),(x-w/2+rr,y+d/2,z),(x-w/2,y+d/2-rr,z),(x-w/2,y-d/2+rr,z)]
    return curve(name,pts,.006,mat,True)

# Earth, plinth, and low horizontal volumes.
cube('Ground to horizon',(0,0,-.42),(200,200,.5),gravel)
cube('Floating limestone foundation',(0,2.5,.02),(14.4,7.6,.38),stone,.06)
cube('Continuous living floor',(-1.1,2.6,.25),(11.8,6.9,.14),travertine,.015)
cube('Bedroom garden wing',(6.9,2.6,1.86),(3.4,7.6,3.4),stone,.035)
cube('Rear lime plaster wall',(-1,6.15,1.83),(12.2,.3,3.2),plaster,.015)
cube('Left limestone return',(-7,3.4,1.83),(.32,5.8,3.2),stone,.03)
cube('Left cantilever roof',(-.75,2.45,3.62),(13.25,8.1,.32),stone,.045)
cube('Fine bronze roof fascia',(-.75,-1.61,3.58),(13.2,.045,.16),bronze,.01)
cube('Timber ceiling plane',(-.75,2.4,3.435),(12.45,7.55,.075),wood,.01)
# Ceiling battens signal scale and craftsmanship.
for i in range(51):
    x=-6.85+i*.245
    cube('Oak ceiling rib %02d'%i,(x,2.43,3.38),(.052,7.45,.068),woodlight,.008)
# Thick stone wing softened by recesses and panels.
for x in [5.4,6.2,7,7.8,8.6]:cube('Limestone vertical joint',(x,-1.208,1.9),(.009,.008,3.17),gravel)
for z in [.84,1.66,2.48]:cube('Limestone horizontal bed',(6.9,-1.211,z),(3.38,.008,.009),gravel)
cube('Bedroom recessed dark reveal',(6.88,-1.224,1.83),(2.4,.04,2.62),charcoal,.015)
cube('Bedroom oak shutter',(6.88,-1.258,1.83),(2.22,.055,2.45),wood,.008)
for i in range(24):cube('Bedroom vertical fluting',(5.83+i*.092,-1.3,1.83),(.028,.08,2.44),woodlight,.008)
cube('Stone wing cap',(6.9,2.6,3.67),(3.54,7.8,.22),stone,.04)
# Full-height front glazing with open central bay. Thin divisions, no chunky frames.
for x in [-6.75,-4.4,-1.6,1.1,4.5]:
    cube('Bronze facade mullion',(x,-.83,1.83),(.055,.095,3.09),charcoal,.009)
for z in [.32,3.36]:cube('Glazing perimeter rail',(-1.1,-.83,z),(11.6,.10,.05),charcoal,.006)
for left,right in [(-6.73,-4.44),(-4.36,-1.65),(1.15,4.47)]:cube('Low iron fixed glazing',((left+right)/2,-.84,1.83),(right-left,.018,2.98),glass)
# Slim left side corner glass facing garden.
for y in [-.7,1.0]:cube('Side light mullion',(-6.9,y,1.83),(.07,.055,3.04),charcoal,.006)
cube('Side corner glazing',(-6.91,.15,1.83),(.018,1.64,3.0),glass)
# Deep charcoal interior door and shadow gaps.
cube('Hall opening',(4.9,5.96,1.7),(1.0,.035,2.75),charcoal,.01)
cube('Oak pivot door',(4.77,5.91,1.7),(.75,.06,2.65),wood,.012)
rod('Long bronze door pull',(5.02,5.85,1.35),(5.02,5.85,2.0),.016,bronze)
# Timber wall articulation at rear living room.
for i in range(34):cube('Living wall oak slat',(-6.68+i*.093,5.965,1.83),(.045,.11,3.08),wood,.008)
cube('Back wall cove',(-.8,5.97,3.19),(8,.035,.035),led,.009)

# Interior lounge: sculpted upholstered modules with piping, real feet and joinery.
active=collections['02 Living atelier']
cube('Woven lounge rug',(-3.25,1.85,.34),(5.25,3.75,.033),rug,.035)
# Fine parallel rug binding.
for y in [.01,3.69]:cube('Rug hand-bound edge',(-3.25,y,.361),(5.1,.018,.007),linen,.004)
for x in [-5.83,-.67]:cube('Rug hand-bound edge',(x,1.85,.361),(.018,3.66,.007),linen,.004)
sofa_y=3.35
cube('Low sofa ash plinth',(-3.7,sofa_y,.52),(3.52,1.08,.16),wood,.055)
for x in [-5.15,-2.25]:
    for y in [2.96,3.76]:cyl('Sofa recessed turned leg',(x,y,.40),.055,.18,wood,20)
for i in range(3):
    x=-4.81+i*1.12
    cube('Individual deep seat cushion '+str(i),(x,3.20,.72),(1.08,.94,.28),linen,.135)
    seam('Hand-sewn cushion piping',(x,3.20),(1.0,.86),.745,linen)
    o=cube('Tailored back cushion '+str(i),(x,3.78,1.07),(1.09,.27,.74),linen,.12);o.rotation_euler.x=math.radians(9)
cube('Sofa left padded arm',(-5.48,3.38,.87),(.26,1.13,.58),linen,.13)
cube('Sofa right padded arm',(-1.92,3.38,.87),(.26,1.13,.58),linen,.13)
for name,x,y,z,m,ang in [('Sage throw cushion',-4.96,3.47,1.05,sage,-.15),('Tobacco lumbar cushion',-2.49,3.46,.99,rust,.18)]:
    o=cube(name,(x,y,z),(.57,.24,.52),m,.115);o.rotation_euler=(.17,ang,ang)
# Chaise perpendicular to sofa.
cube('Chaise timber plinth',(-5.12,2.35,.51),(1.25,1.37,.16),wood,.05)
cube('Chaise long cushion',(-5.12,2.30,.72),(1.2,1.45,.28),linen,.14)
seam('Chaise double stitched seam',(-5.12,2.30),(1.1,1.34),.75,linen)
# Twin low monolithic coffee tables.
for x,y,r,z in [(-3.25,1.56,.76,.64),(-2.15,1.70,.46,.53)]:
    cyl('Travertine drum table base',(x,y,.47),r*.65,.25,travertine,64,.035)
    cyl('Honed rounded coffee table top',(x,y,z),r,.12,travertine,96,.04)
# Books: offset stacked covers, paper block, spine.
def book(name,loc,size,idx,ang=0):
    x,y,z=loc;w,d,h=size
    root=bpy.data.objects.new(name,None);active.objects.link(root);root.location=loc;root.rotation_euler.z=ang
    for part,zz,hh,mat in [('paper',h*.5,h-.012,pages),('lower cover',.005,.01,bookm[idx%5]),('upper cover',h-.005,.01,bookm[idx%5])]:
        o=cube(name+' '+part,(0,0,zz),(w,d,hh),mat,.003);o.parent=root
    return root
book('Architecture monograph',(-3.42,1.62,.706),(.48,.34,.045),0,.12)
book('Garden notebook',(-3.40,1.61,.751),(.38,.28,.032),3,-.06)
lathe('Small porcelain tea cup',(-2.97,1.31,.70),[(.04,0),(.052,.01),(.055,.08),(.052,.085),(.046,.08),(.045,.018),(.04,.015)],ceramic)
cyl('Cup espresso',(-2.97,1.31,.77),.043,.002,blackstone,32,0)
curve('Tea cup handle',[(-2.915,1.31,.72),(-2.87,1.31,.74),(-2.88,1.31,.77),(-2.915,1.31,.765)],.008,ceramic)
lathe('Sculptural dark bowl',(-2.12,1.69,.59),[(.10,0),(.18,.03),(.23,.09),(.24,.10),(.225,.105),(.16,.055),(.08,.03)],blackstone)
# Lounge chair with bent ash frame and sling upholstery.
def lounge_chair(x,y,angle):
    made=set(bpy.data.objects)
    for sx in [-1,1]:
        xx=x+sx*.36
        rod('Lounge front tapered leg',(xx,y-.36,.35),(xx,y-.30,.82),.035,woodlight,.025)
        rod('Lounge rear tapered leg',(xx,y+.42,.35),(xx,y+.25,1.13),.038,woodlight,.025)
        curve('Sculpted ash arm',[(xx,y-.42,.85),(xx,y-.20,.94),(xx,y+.28,1.01)],.033,woodlight)
    seat=cube('Sling chair padded seat',(x,y,.66),(.68,.69,.15),sage,.075);seat.rotation_euler.x=-.10
    back=cube('Sling chair upholstered back',(x,y+.29,.97),(.67,.13,.66),sage,.065);back.rotation_euler.x=.23
    rod('Chair lower front stretcher',(x-.34,y-.31,.52),(x+.34,y-.31,.52),.02,woodlight)
    for o in set(bpy.data.objects)-made:
        v=o.location-Vector((x,y,0));o.location=Vector((x+v.x*cos(angle)-v.y*sin(angle),y+v.x*sin(angle)+v.y*cos(angle),v.z));o.rotation_euler.z+=angle
lounge_chair(-.85,.78,-.43)
# Media hearth / sideboard with fluted oak drawers.
cube('Floating sideboard carcass',(-3.9,5.72,.80),(4.9,.46,.58),wood,.025)
cube('Thin limestone cabinet top',(-3.9,5.71,1.115),(5.0,.50,.07),travertine,.02)
for i in range(5):
    x=-5.87+i*.985
    cube('Sideboard drawer face',(x,5.468,.80),(.96,.035,.53),wood,.01)
    cube('Recessed bronze pull',(x,5.44,1.015),(.34,.017,.012),bronze,.004)
# Large minimal canvas and raised black ink geometry.
cube('Gallery frame',(-1.30,5.94,2.25),(2.12,.055,1.43),wood,.012)
cube('Gallery warm canvas',(-1.30,5.902,2.25),(2.02,.018,1.33),linen,.005)
for i,(x,z,sx,sz) in enumerate([(-1.7,2.2,.47,.76),(-1.15,2.47,.55,.22),(-.91,1.95,.22,.35)]):
    cube('Abstract relief shape '+str(i),(x,5.885,z),(sx,.025,sz),blackstone,.06)
for xx,rr,h in [(-5.5,.16,.38),(-5.08,.105,.25)]:lathe('Hand-thrown console vessel',(xx,5.65,1.15),[(rr*.55,0),(rr,.06),(rr*.96,h*.65),(rr*.40,h*.9),(rr*.42,h),(rr*.30,h)],ceramic)
book('Console art book',(-3.5,5.65,1.15),(.57,.35,.035),1,.03)
book('Console linen book',(-3.47,5.65,1.185),(.51,.32,.03),4,-.06)
# Reading lamp in blackened bronze.
cyl('Reading lamp heavy foot',(-6.15,3.80,.38),.18,.06,charcoal,48)
rod('Reading lamp upright',(-6.15,3.8,.40),(-6.15,3.8,1.88),.014,bronze)
curve('Reading lamp neck',[(-6.15,3.8,1.85),(-6.12,3.76,2.03),(-5.9,3.7,2.08)],.015,bronze)
lathe('Reading lamp spun shade',(-5.9,3.7,1.89),[(.21,0),(.19,.06),(.09,.16),(.035,.19)],charcoal)
area('Reading pool',(-5.9,3.7,1.90),35,(1,.68,.35),.25,(-5.3,3.1,.7))

# Dining and functional kitchen.
active=collections['03 Dining and kitchen']
cube('Dining monolithic oak top',(2.55,1.85,1.10),(2.35,1.0,.12),woodlight,.12)
for x in [1.73,3.37]:cube('Dining sculptural trestle',(x,1.85,.72),(.18,.77,.65),wood,.04)
rod('Table hidden stretcher',(1.7,1.85,.56),(3.4,1.85,.56),.045,wood)
# Dining chairs: joinery, curved back, upholstered seat.
def dining_chair(x,y,angle):
    root=bpy.data.objects.new('Crafted dining chair',None);active.objects.link(root);root.location=(x,y,0);root.rotation_euler.z=angle
    made=set(bpy.data.objects)
    for sx in [-1,1]:
        for sy in [-1,1]:rod('Tapered ash chair leg',(sx*.23,sy*.24,.34),(sx*.195,sy*.195,.83),.028,woodlight,.021)
    cube('Chair seat oak frame',(0,0,.79),(.50,.50,.055),woodlight,.065)
    cube('Chair soft linen seat',(0,-.005,.835),(.46,.46,.065),linen,.075)
    for sx in [-1,1]:rod('Chair back post',(sx*.22,.20,.78),(sx*.25,.23,1.35),.025,woodlight,.019)
    curve('Sweeping curved chair crest',[(-.28,.14,1.29),(-.25,.25,1.36),(0,.30,1.39),(.25,.25,1.36),(.28,.14,1.29)],.035,woodlight)
    curve('Wishbone back spine',[(-.17,.255,1.31),(0,.255,1.15),(.17,.255,1.31)],.018,woodlight)
    rod('Wishbone stem',(0,.25,.85),(0,.255,1.16),.019,woodlight)
    for o in set(bpy.data.objects)-made:o.parent=root
for x in [1.84,3.28]:dining_chair(x,1.02,pi);dining_chair(x,2.68,0)
# Dining still life.
lathe('Dining sculptural carafe',(2.55,1.89,1.17),[(.12,0),(.18,.10),(.16,.25),(.07,.34),(.065,.49),(.055,.50),(.047,.48)],ceramic)
for dx,dy in [(-.20,.04),(.12,-.08),(.02,.09)]:
    curve('Dried branch',[(2.55,1.89,1.62),(2.55+dx,1.89+dy,1.94),(2.55+dx*2,1.89+dy*2,2.09)],.005,bark)
for x in [1.65,3.38]:
    cyl('Handmade dinner plate',(x,1.84,1.18),.19,.018,ceramic,64,.01)
    cyl('Folded linen napkin',(x,1.84,1.198),.105,.009,linen,32,.01)
# Three thin pendant lamps with cords.
for x in [1.72,2.55,3.38]:
    rod('Pendant cable',(x,1.85,3.35),(x,1.85,2.48),.004,charcoal)
    lathe('Bronze pendant shade',(x,1.85,2.40),[(.24,0),(.23,.035),(.10,.11),(.035,.16)],bronze)
    cyl('Pendant opal diffuser',(x,1.85,2.405),.205,.009,led,48,.002)
    area('Dining warm pendant',(x,1.85,2.39),35,(1,.72,.44),.35,(x,1.85,1.1))
# Kitchen cabinetry at back.
cube('Kitchen base carcass',(2.25,5.62,.81),(3.6,.85,1.0),wood,.025)
for i in range(6):
    cube('Handleless oak kitchen door',(.77+i*.59,5.175,.82),(.575,.045,.93),wood,.008)
    cube('Kitchen finger pull shadow',(.77+i*.59,5.14,1.22),(.54,.015,.022),charcoal,.002)
cube('Basalt kitchen counter',(2.25,5.57,1.34),(3.72,.99,.10),blackstone,.025)
cube('Limestone splashback',(2.25,6.0,1.76),(3.7,.04,.72),travertine,.01)
cube('Thin floating shelf',(2.25,5.88,2.47),(3.75,.38,.065),woodlight,.018)
cube('Shelf integrated task lighting',(2.25,5.67,2.423),(3.5,.025,.018),led,.004)
area('Kitchen shelf light',(2.25,5.58,2.4),70,(1,.76,.48),2.4,(2.25,5.4,1.35))
cube('Undermount sink dark opening',(1.18,5.58,1.396),(.62,.48,.006),charcoal,.07)
curve('Kitchen bronze swan neck',[(1.18,5.90,1.38),(1.18,5.9,1.73),(1.18,5.65,1.81),(1.18,5.57,1.68)],.018,bronze)
rod('Faucet side handle',(1.33,5.89,1.40),(1.33,5.89,1.56),.013,bronze)
# Shelf crockery, cutting board, grooved timber island.
for i in range(5):cyl('Stacked ceramic bowls',(3.27,5.83,2.52+i*.019),.115,.018,ceramic,32,.01)
for x in [1.05,1.45,2.1]:lathe('Shelf ceramic vessel',(x,5.87,2.505),[(.07,0),(.10,.05),(.09,.2),(.055,.24)],ceramic)
cube('Solid oak chopping board',(3.57,5.50,1.41),(.40,.34,.03),woodlight,.03)
cube('Basalt island top',(2.75,3.95,1.36),(2.70,.90,.13),blackstone,.04)
cube('Kitchen island oak carcass',(2.75,3.95,.86),(2.5,.76,.88),wood,.025)
for i in range(34):cube('Fluted island detail',(1.53+i*.074,3.56,.88),(.035,.035,.84),woodlight,.008)
lathe('Fruit bowl',(2.8,3.90,1.43),[(.15,0),(.25,.04),(.30,.10),(.28,.12),(.22,.07)],ceramic)
for i in range(5):sphere('Small garden pear',(2.66+random.random()*.3,3.78+random.random()*.2,1.57),(.06,.06,.075),grasses[2],16,8)

# Terrace deck, outdoor seating and human-scale details.
active=collections['04 Terrace']
cube('Terrace cantilever slab',(.4,-2.45,.14),(15.3,3.35,.28),travertine,.04)
for x in range(-7,9):cube('Terrace stone joint',(x,-2.45,.286),(.008,3.25,.003),gravel)
for y in [-3.8,-2.8,-1.8]:cube('Terrace stone joint',(.4,y,.286),(15.2,.008,.003),gravel)
for i in range(3):cube('Broad garden descent step',(-3.1,-4.25-i*.43,.12-i*.095),(4.8,.46,.18),travertine,.02)
cube('Terrace shadow reveal',(.4,-4.13,.10),(15,.04,.05),charcoal,.005)
cube('Warm terrace underlight',(.4,-4.12,.075),(14.7,.015,.02),led,.004)
# Two low exterior lounge chairs east of front door.
for x in [3.5,5.4]:
    for xx in [x-.37,x+.37]:
        rod('Outdoor chair front leg',(xx,-2.95,.28),(xx,-2.77,.71),.032,woodlight)
        rod('Outdoor chair back leg',(xx,-2.05,.28),(xx,-2.25,1.05),.032,woodlight)
        rod('Outdoor chair arm',(xx,-2.97,.83),(xx,-2.1,.91),.028,woodlight)
    cube('Outdoor lounge cushion',(x,-2.53,.63),(.77,.80,.17),linen,.075)
    o=cube('Outdoor lounge back',(x,-2.13,.97),(.77,.16,.64),linen,.075);o.rotation_euler.x=.16
cyl('Outdoor bronze tray table',(4.47,-2.64,.62),.29,.04,bronze,64,.018)
cyl('Outdoor tray pedestal',(4.47,-2.64,.45),.045,.32,charcoal)
cyl('Outdoor tray base',(4.47,-2.64,.29),.18,.025,charcoal)
# Exterior planters with soil.
for x,y,sz in [(7.3,-2.7,.55),(-6.6,-2.4,.37)]:
    lathe('Thrown terracotta terrace planter',(x,y,.28),[(sz*.56,0),(sz*.71,.12),(sz,.62),(sz*.96,.72),(sz*.86,.72),(sz*.85,.61)],terracotta)
    cyl('Planter soil',(x,y,.90),sz*.83,.03,soil,48,0)

# Reflecting water and long garden strokes.
active=collections['05 Water garden']
cube('Garden sunken pool outer basin',(.6,-7.75,-.23),(7.2,5.15,.44),blackstone,.06)
cube('Reflective water surface',(.6,-7.75,-.025),(6.86,4.81,.016),water,.006)
for x in [-2.95,4.15]:cube('Pool limestone coping',(x,-7.75,.03),(.25,5.15,.18),travertine,.025)
for y in [-5.23,-10.27]:cube('Pool limestone end coping',(.6,y,.03),(7.2,.25,.18),travertine,.025)
# Thin floating crossing at asymmetrical far end.
for i in range(7):cube('Floating stone garden path',(-5.15,-5.4-i*.98,-.015),(1.45,.74,.16),travertine,.035,rot=(0,0,random.uniform(-.012,.012)))
# Dark low perimeter walls on rear/sides.
cube('Rear garden enclosure',(0,9.45,.54),(28,.32,1.7),stone,.05)
cube('West garden enclosure',(-11.7,0,.48),(.30,19,1.6),stone,.05)
# Corten edging and planted beds.
for name,loc,size in [('Western garden',(-9,-3.5,-.15),(4.8,15,.26)),('Eastern border',(8.55,-6.0,-.15),(6.5,10,.26)),('Rear grove',(0,8.0,-.15),(23,2.5,.26)),('Path island',(-3.65,-7.0,-.15),(1.25,7.2,.26))]:cube(name,loc,size,soil,.08)
for x,y,w,d in [(-9,-3.5,4.8,15),(8.55,-6,6.5,10)]:
    cube('Weathered bronze planting edge',(x-w/2,y,-.02),(.025,d,.22),bronze,.004)
    cube('Weathered bronze planting edge',(x+w/2,y,-.02),(.025,d,.22),bronze,.004)
# Surface pebbles along water edge and path.
for i in range(170):
    x=random.choice([-1,1])*random.uniform(7.8,11.3);y=random.uniform(-10.5,8.3)
    sphere('River pebble',(x,y,-.045),(random.uniform(.05,.16),random.uniform(.05,.13),random.uniform(.025,.065)),stone,8,4)

# Botanically suggestive olive trees with actual branching and thousands of leaves.
active=collections['06 Planting']
def mesh_obj(name,verts,faces,mats,indices=None):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);active.objects.link(o)
    for m in mats:me.materials.append(m)
    if indices:
        for p,idx in zip(me.polygons,indices):p.material_index=idx
    return o

def olive(name,base,height=4,radius=2):
    x,y,z=base
    trunk=[(x,y,z),(x-.09,y+.02,z+height*.28),(x+.11,y-.05,z+height*.53),(x+.06,y+.03,z+height*.72)]
    curve(name+' gnarled trunk',trunk,.12 if height>3 else .065,bark)
    branches=[]
    for i in range(9):
        a=i*2.399+random.uniform(-.2,.2);r=radius*random.uniform(.55,1);h=height*random.uniform(.72,1.06)
        end=(x+cos(a)*r,y+sin(a)*r,z+h)
        start=(x+.05,y,z+height*random.uniform(.40,.65))
        mid=(x+cos(a)*r*.55,y+sin(a)*r*.55,z+h*.82)
        curve(name+' irregular bough',[start,mid,end],.038 if height>3 else .022,bark)
        branches.append(end)
        for j in range(3):
            ang=a+random.uniform(-1.4,1.4);rr=random.uniform(.35,.70)*radius
            dest=(end[0]+cos(ang)*rr,end[1]+sin(ang)*rr,end[2]+random.uniform(-.25,.30))
            rod(name+' fine branch',mid,dest,.013,bark,.004);branches.append(dest)
    vs=[];fs=[];idx=[]
    for center in branches:
        for j in range(84 if height>3 else 45):
            a=random.uniform(0,2*pi);rr=radius*.44*math.sqrt(random.random());zz=random.gauss(0,.20*radius)
            pos=Vector((center[0]+cos(a)*rr,center[1]+sin(a)*rr,center[2]+zz))
            length=random.uniform(.055,.11)*max(.7,height/4);width=length*.28
            direction=Vector((cos(a),sin(a),random.uniform(-.65,.65))).normalized();side=Vector((-sin(a),cos(a),.3)).normalized()
            k=len(vs);vs.extend([pos-direction*length,pos+side*width,pos+direction*length,pos-side*width,pos+Vector((0,0,.014))]);fs.extend([(k,k+1,k+4),(k+1,k+2,k+4),(k+2,k+3,k+4),(k+3,k,k+4)]);idx.extend([random.randrange(4)]*4)
    mesh_obj(name+' silver green leaves',vs,fs,leaves,idx)
for name,base,h,r in [('Sculptural west olive',(-8.85,-1.9,-.02),4.3,1.55),('Poolside olive',(10.2,-5.0,-.02),4.3,1.45),('Left foreground olive',(-9.3,-9.4,-.02),4.0,1.5),('Rear olive A',(-5.5,8,-.02),4.7,1.8),('Rear olive B',(3.2,8.1,-.02),4.9,1.8),('Rear olive C',(9.3,7.4,-.02),4.1,1.3),('Terrace potted olive',(7.3,-2.7,.91),2.1,.73)]:olive(name,base,h,r)
# Rounded mounded shrubs with pointier individual foliage, merged meshes.
def shrub(x,y,r,h):
    vs=[];fs=[];ids=[]
    for i in range(350):
        a=random.random()*2*pi;t=random.uniform(.12,pi/2);rr=r*cos(t)*random.uniform(.5,1)
        p=Vector((x+cos(a)*rr,y+sin(a)*rr,h*sin(t)-.06));d=Vector((cos(a),sin(a),random.uniform(.1,1)))*.08
        s=Vector((-sin(a),cos(a),0))*.025;k=len(vs);vs.extend([p-d,p+s,p+d,p-s]);fs.append((k,k+1,k+2,k+3));ids.append(random.randrange(4))
    mesh_obj('Clipped Mediterranean shrub',vs,fs,leaves,ids)
for x,y,r,h in [(-7.5,-5,.7,.8),(-9.6,2.4,1.1,1),(-8,-7.1,.9,.75),(6.3,-7.9,.8,.8),(7.0,-9.8,1,.8),(10,-2.1,.8,1),(10,-7.1,1.1,.85),(-3.65,-8.6,.48,.48),(-3.6,-5.7,.40,.5)]:shrub(x,y,r,h)
# Grasses: each blade a bent ribbon with a real tapered tip.
vs=[];fs=[];ids=[]
for patch in range(155):
    if patch<65:x=random.uniform(-10.8,-6.5);y=random.uniform(-10.4,7.6)
    elif patch<133:x=random.uniform(5.5,11.2);y=random.uniform(-10.6,-3.9)
    else:x=random.uniform(-4.05,-3.35);y=random.uniform(-10,-4.4)
    for j in range(random.randint(35,70)):
        a=random.uniform(0,2*pi);r=random.uniform(0,.22);h=random.uniform(.25,.68);lean=random.uniform(.12,.37);w=random.uniform(.008,.016)
        bx=x+cos(a)*r;by=y+sin(a)*r;perp=Vector((-sin(a),cos(a),0))*w
        p=Vector((bx,by,-.02));p1=p+Vector((cos(a)*lean*.27,sin(a)*lean*.27,h*.55));p2=p+Vector((cos(a)*lean,sin(a)*lean,h))
        k=len(vs);vs.extend([p-perp,p+perp,p1+perp*.55,p1-perp*.55,p2]);fs.extend([(k,k+1,k+2,k+3),(k+3,k+2,k+4)]);ids.extend([random.randrange(4)]*2)
grass_mesh=mesh_obj('Thousands of meadow grass blades',vs,fs,grasses,ids)
for v in grass_mesh.data.vertices:
    if v.co.x < -6: v.co.x=min(v.co.x,-7.25)
# Lavender flower spikes as merged geometry.
vs=[];fs=[];ids=[]
for i in range(650):
    if i<350:x=random.uniform(-10,-7);y=random.uniform(-7,3)
    else:x=random.uniform(6,10.5);y=random.uniform(-10,-5.5)
    z=random.uniform(.25,.56);rad=.018
    for n in range(4):
        a=random.random()*2*pi;px=x+cos(a)*.018;py=y+sin(a)*.018;zz=z+n*.031;k=len(vs)
        vs.extend([(px-rad,py,zz),(px,py-rad,zz),(px+rad,py,zz),(px,py+rad,zz),(px,py,zz+.037)])
        fs.extend([(k,k+1,k+4),(k+1,k+2,k+4),(k+2,k+3,k+4),(k+3,k,k+4)]);ids.extend([random.randrange(3)]*4)
mesh_obj('Garden lavender flowers',vs,fs,lavenders,ids)
# Small aloe in west planter.
vs=[];fs=[]
for i in range(28):
    a=i*2.399;length=random.uniform(.35,.65);p=Vector((-6.6,-2.4,.92));tip=p+Vector((cos(a)*length*.65,sin(a)*length*.65,length));side=Vector((-sin(a),cos(a),0))*.06;k=len(vs);vs.extend([p-side,p+side,p+Vector((cos(a)*length*.5,sin(a)*length*.5,length*.5))+side*.6,tip,p+Vector((cos(a)*length*.5,sin(a)*length*.5,length*.5))-side*.6]);fs.append((k,k+1,k+2,k+3,k+4))
mesh_obj('Terrace sculptural aloe',vs,fs,[leaves[1]])

# Garden lighting and late afternoon sun.
active=collections['07 Lighting']
for x,y in [(-5.9,-5.3),(-5.9,-8.4),(5.0,-6.0),(6,-9.7),(-7.4,-3.7)]:
    cube('Bronze path lantern',(x,y,.22),(.09,.09,.48),charcoal,.012)
    cube('Lantern warm aperture',(x,y-.048,.40),(.052,.012,.065),led,.004)
    area('Path light',(x,y-.06,.40),9,(1,.58,.26),.12,(x,y-.8,-.1))
area('Soft living ceiling',(-3.7,2.5,3.25),220,(1,.77,.53),3.0,(-3.4,2,.4))
area('Living back wall wash',(-3.7,5.5,3.12),65,(1,.73,.43),2.5,(-3.7,5.9,1.7))
area('Terrace soft fill',(0,-1.2,3.2),85,(1,.75,.49),4,(0,-3,.2))
world=bpy.data.worlds.new('Late afternoon clear sky');scene.world=world;world.use_nodes=True
n=world.node_tree.nodes;l=world.node_tree.links;n.clear();out=n.new('ShaderNodeOutputWorld');bg=n.new('ShaderNodeBackground');sky=n.new('ShaderNodeTexSky');sky.sky_type='NISHITA';sky.sun_disc=False;sky.sun_elevation=math.radians(18);sky.sun_rotation=math.radians(235);sky.altitude=.1;sky.air_density=1.1;sky.dust_density=1.0
bg.inputs['Strength'].default_value=.26;l.new(sky.outputs['Color'],bg.inputs['Color']);l.new(bg.outputs['Background'],out.inputs['Surface'])
d=bpy.data.lights.new('Low warm afternoon sun','SUN');d.energy=1.65;d.angle=math.radians(3);d.color=(1,.82,.65)
o=bpy.data.objects.new('Low warm afternoon sun',d);active.objects.link(o);o.location=(-13,-11,12);o.rotation_euler=(Vector((0,0,0))-o.location).to_track_quat('-Z','Y').to_euler()
# A low natural landscape and additional branching trees beyond the garden wall.
active=collections['06 Planting']
vs=[];fs=[]
for j in range(12):
    y=12+j*6
    for i in range(45):
        x=-90+i*4
        z=-.3 + (2.2+2.4*sin(x*.045+y*.025)+1.6*sin(x*.11+y*.06))*min(1,j/5)
        vs.append((x,y,z))
for j in range(11):
    for i in range(44):
        k=j*45+i;fs.append((k,k+1,k+46,k+45))
terrainmat=textured('25 | Distant muted hillside',(.13,.15,.09),(.29,.28,.17),7,.98,.05,.1)
mesh_obj('Softly rolling hillside',vs,fs,[terrainmat])
for i,(x,y,h,r) in enumerate([(-17,14,5,2),(-10,19,5.6,2.1),(-2,18,4.8,2.1),(7,19,5.5,2.2),(16,15,5.2,2),(25,20,6,2.4),(-27,20,5.5,2.3)]):
    olive('Distant olive '+str(i),(x,y,-.1),h,r)

# Cameras: architectural verticals, furniture-first interior, garden intimacy.
active=collections['08 Cameras']
def camera(name,loc,target,lens,shift=0,fstop=8):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);active.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=lens;d.sensor_width=36;d.shift_y=shift
    d.dof.use_dof=True;d.dof.focus_distance=(Vector(target)-o.location).length;d.dof.aperture_fstop=fstop;d.dof.aperture_blades=9;d.clip_end=400
    return o
hero=camera('01 | Garden residence',(17.5,-24.5,6.5),(.2,-.4,1.35),42,.02,11)
interior=camera('02 | Quiet living',(-5.8,-.20,1.80),(-1.20,3.15,1.28),25,0,7.1)
garden=camera('03 | Reflective courtyard',(6.3,-11.8,1.65),(-1.3,-1.7,1.35),34,0,8)
# Hero saved as initial view in Blender.
scene.camera=hero
scene.render.resolution_x=1920;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.render.fps=24
scene.world.color=(.1,.1,.1)
scene['project']='STILLWATER HOUSE';scene['design']='Limestone, smoked oak, bronze and a Mediterranean water garden';scene['units']='meters';scene['seed']=20261121
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Stillwater-House.blend'),compress=True)
summary={'project':'Stillwater House','blender':bpy.app.version_string,'objects':len(scene.objects),'materials':len(bpy.data.materials),'mesh_vertices':sum(len(o.data.vertices) for o in scene.objects if o.type=='MESH'),'cameras':[c.name for c in [hero,interior,garden]],'procedural_seed':20261121,'external_assets':[],'mode':args.mode}
(OUT/'scene-manifest.json').write_text(json.dumps(summary,indent=2));print('SCENE_READY',json.dumps(summary),flush=True)
if args.mode!='build':
    shots=[(hero,'01-Garden-Residence',1920,1200),(interior,'02-Quiet-Living',1800,1200),(garden,'03-Reflective-Courtyard',1800,1200)]
    if args.mode=='preview':shots=[(hero,'preview',1000,625)]
    for cam,name,w,h in shots:
        scene.camera=cam;scene.render.resolution_x=w;scene.render.resolution_y=h
        scene.render.filepath=str(OUT/'renders'/f'{name}.png');t=time.time();bpy.ops.render.render(write_still=True)
        print('RENDER_COMPLETE',name,round(time.time()-t,1),flush=True)
    scene.camera=hero;scene.render.resolution_x=1920;scene.render.resolution_y=1200
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Stillwater-House.blend'),compress=True)
print('COMPLETE',flush=True)
