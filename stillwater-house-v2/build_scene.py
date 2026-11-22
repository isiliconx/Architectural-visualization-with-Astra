"""Stillwater House II. Procedural editable architectural scene, meters.
Run: blender -b --python build_scene.py -- --output . --mode build
"""
import sys, argparse, math, json, time, runpy, random
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',default=str(Path(__file__).parent));p.add_argument('--mode',choices=['build','preview'],default='build');_v2_options=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(_v2_options.output).resolve();OUT.mkdir(parents=True,exist_ok=True);(OUT/'renders').mkdir(exist_ok=True)
# The original generator is kept self-contained in this release, without any V1 path dependency.
base=(Path(__file__).parent/'base_scene.py').read_text()
base=base[:base.index('# Hero saved as initial view in Blender.')]
base=base.replace("p.inputs['Transmission Weight']", "p.inputs['Transmission Weight']")
base=base.replace("o.data.energy", "o.data.energy")
# Area-light lobe controls appeared after Blender 4.3.
base=base.replace("d.transmission_factor=0;d.specular_factor=0;", "")
base=base.replace('# Earth, plinth, and low horizontal volumes.',(Path(__file__).parent/'geometry.py').read_text()+'\n# Earth, plinth, and low horizontal volumes.')
saved=sys.argv[:];sys.argv=['build_scene.py','--','--output',str(OUT),'--mode','build'];exec(compile(base,'base_scene.py','exec'),globals());sys.argv=saved
print('V1_BASE_READY',flush=True)
random.seed(20261122)
scene.cycles.device='CPU';scene.render.threads=8
# Clear the small garden, preserving the original furniture and material palette.
for name in ['04 Terrace','05 Water garden','06 Planting']:
 for obj in list(collections[name].objects):bpy.data.objects.remove(obj,do_unlink=True)
for obj in list(collections['07 Lighting'].objects):
 if obj.name.startswith(('Bronze path lantern','Lantern warm aperture','Path light')):bpy.data.objects.remove(obj,do_unlink=True)
bpy.data.objects.remove(bpy.data.objects['Ground to horizon'],do_unlink=True)
# Fresh collections partition the new architecture for manual editing.
for name in ['09 Upper residence','10 Stair lantern','11 Roof gardens','12 Wellness wing']:collection(name)
active=collections['01 Architecture']
# Limestone panelisation, base reveals and stone soffits give the larger volumes scale.
for y in [0,1.3,2.6,3.9,5.2]:
 cube('West wall stone bed',(-7.168,y+1.1,1.8),(.008,.009,3.0),gravel)
for z in [.8,1.6,2.4]:cube('West wall horizontal coursing',(-7.169,3.4,z),(.008,5.7,.009),gravel)

# The east ground pavilion extends the building without enlarging existing furniture.
active=collections['12 Wellness wing']
cube('East wing broad floating foundation',(11.7,3.0,.12),(7.0,8.2,.40),stone,.05)
cube('East wing oak interior floor',(11.75,3,.35),(6.7,7.8,.12),travertine,.02)
cube('East wing rear thermal wall',(11.8,6.97,1.91),(7.1,.28,3.17),plaster,.025)
cube('East wing stone end pier',(15.1,4.3,1.9),(.45,5.55,3.2),stone,.035)
cube('East pavilion floating roof',(11.8,2.87,3.67),(7.5,8.7,.30),stone,.055)
cube('East pavilion timber soffit',(11.8,2.85,3.49),(7.0,8.25,.08),wood,.008)
for x in [8.55,10.7,12.9,15.1]:cube('East garden glazing stile',(x,-.67,1.94),(.045,.085,3.0),charcoal,.006)
for left,right in [(8.58,10.67),(10.73,12.87),(12.93,15.07)]:cube('East pavilion garden glazing',((left+right)/2,-.68,1.94),(right-left,.014,2.97),glass)
for z in [.44,3.44]:cube('East glazing head and sill',(11.8,-.67,z),(6.65,.08,.04),bronze,.005)
cube('East pavilion corner glass',(15.13,.42,1.94),(.015,2.12,2.97),glass)
cube('East corner bronze stile',(15.13,1.49,1.94),(.07,.045,3.0),charcoal,.006)
# Wellness reading room with daybed, book wall and a view of the pool.
cube('Wellness woven carpet',(11.6,2.2,.43),(4.6,3.6,.025),rug,.025)
cube('Daybed timber platform',(12.9,3.9,.63),(2.0,2.8,.30),wood,.07)
cube('Daybed natural linen mattress',(12.9,3.9,.88),(1.91,2.7,.28),linen,.12)
for x in [12.4,13.3]:cube('Daybed linen pillow',(x,4.85,1.1),(.78,.55,.19),linen,.09)
cube('Daybed folded sage throw',(12.9,3.07,1.04),(1.93,.57,.055),sage,.025)
for x in [11.6,14.2]:
 cyl('Wellness bedside table',(x,4.6,.73),.33,.53,travertine,48,.03)
 lathe('Wellness porcelain lamp',(x,4.6,1.0),[(.10,0),(.14,.12),(.08,.26)],ceramic)
 lathe('Wellness linen shade',(x,4.6,1.25),[(.25,0),(.18,.25)],linen)
 area('Wellness bedside light',(x,4.6,1.47),24,(1,.74,.45),.3,(x,4.6,.5))
lounge_chair(9.6,1.1,-.55)
cyl('Reading room tea table',(10.6,1.9,.75),.4,.10,travertine,48,.025)
for z in [.8,1.45,2.1,2.75]:cube('Wellness library shelf',(10.0,6.55,z),(2.25,.42,.06),woodlight,.01)
for row in range(4):
 for i in range(13):
  x=8.97+i*.16;z=.85+row*.65;h=random.uniform(.25,.43)
  cube('Wellness library bound volume',(x,6.49,z+h/2),(.11,.25,h),bookm[(row+i)%5],.008)
area('East wing warm ceiling',(12,2.9,3.35),260,(1,.78,.57),3.5,(12,2,.6))

# Upper residence: long carved limestone frame, shaded glazing and open terrace.
active=collections['09 Upper residence']
cube('Upper residence floating floor',(4.3,3.3,3.91),(14.4,7.4,.36),stone,.07)
cube('Upper wraparound terrace',(4.3,1.95,4.12),(14.0,9.7,.12),travertine,.04)
cube('Upper residence rear limestone wall',(4.5,6.8,5.82),(14,.28,3.5),plaster,.025)
cube('Upper west return stone pier',(-2.5,4.1,5.82),(.36,5.6,3.5),stone,.03)
cube('Upper east stone pier',(11.2,4.6,5.82),(.40,4.7,3.5),stone,.03)
cube('Sculptural upper floating roof',(4.35,2.8,7.69),(15.15,9.1,.27),stone,.08)
cube('Bronze reveal under upper roof',(4.35,-1.75,7.59),(14.9,.035,.12),bronze,.008)
cube('Upper warm oak ceiling',(4.3,3.0,7.50),(14.6,8.3,.075),wood,.012)
for i in range(55):cube('Upper oak soffit rib',(-2.65+i*.257,2.9,7.43),(.044,8.2,.075),woodlight,.006)
# Full-height curtain wall recessed behind the terrace edge.
for x in [-2.25,.4,3.05,5.7,8.35,10.9]:cube('Upper glazing bronze mullion',(x,.30,5.82),(.047,.10,3.28),charcoal,.006)
for left,right in [(-2.22,.37),(.43,3.02),(3.08,5.67),(5.73,8.32),(8.38,10.87)]:cube('Upper room low-iron glazing',((left+right)/2,.31,5.82),(right-left,.016,3.23),glass)
for z in [4.2,7.45]:cube('Upper glazing head and sill',(4.34,.3,z),(13.2,.10,.045),charcoal,.006)
# Sliding bronze/timber fins are staggered rather than a repetitive full-screen box.
for x in [8.7+i*.22 for i in range(10)]:
 o=cube('Operable bronze oak shade fin',(x,.08,5.83),(.065,.38,3.2),woodlight,.013);o.rotation_euler.z=math.radians(-25)
# A transparent frameless terrace balustrade with a very thin bronze cap.
cube('Upper terrace crystal guard',(4.25,-2.83,4.71),(13.8,.018,1.07),glass,.005)
rod('Upper terrace bronze handrail',(-2.65,-2.83,5.25),(11.15,-2.83,5.25),.018,bronze)
for x in [-2.7,11.25]:
 cube('Upper terrace side crystal guard',(x,-1.22,4.71),(.018,3.15,1.07),glass,.005)
 rod('Upper terrace side handrail',(x,-2.8,5.25),(x,.3,5.25),.018,bronze)
# One central open bay is clear for circulation through the upstairs salon.
cube('Upper linen living rug',(2.8,3.1,4.24),(6,4.1,.03),rug,.03)
for x in [.1,1.3,2.5]:
 cube('Upper sofa ash plinth',(x,4.8,4.39),(1.2,1.15,.2),wood,.05)
 cube('Upper sofa linen seat',(x,4.65,4.62),(1.17,1.0,.27),linen,.13)
 cube('Upper sofa linen back',(x,5.14,4.95),(1.17,.24,.71),linen,.12)
for x in [-.5,3.1]:cube('Upper sofa padded arm',(x,4.72,4.78),(.23,1.15,.57),linen,.1)
for x,y,z,r in [(1.4,2.8,4.62,.85),(2.7,2.7,4.5,.5)]:
 cyl('Upper salon stone drum',(x,y,z-.12),r*.62,.25,travertine,64,.03)
 cyl('Upper salon honed table',(x,y,z),r,.1,travertine,64,.03)
# Raised furniture is individually editable; transformations keep human dimensions.
old=set(bpy.data.objects);lounge_chair(4.6,2.2,-.5)
for obj in set(bpy.data.objects)-old:obj.location.z+=3.9
lathe('Upper salon sculptural vessel',(1.3,2.7,4.68),[(.12,0),(.19,.17),(.11,.34),(.07,.4)],ceramic)
cube('Upper gallery canvas',(4.7,6.63,5.9),(2.4,.04,1.45),linen,.008)
for x,z,w,h in [(4.2,5.8,.6,.85),(4.8,6.17,.7,.2),(5.22,5.65,.3,.4)]:cube('Upper canvas raised composition',(x,6.60,z),(w,.03,h),terracotta,.05)
# Bedroom wing reads as warm timber and linen behind sliding louvers.
cube('Upper bedroom oak partition',(7.1,4.95,5.78),(.17,3.6,3.25),wood,.02)
cube('Upper suite bed platform',(9,4.4,4.45),(2.2,2.6,.42),wood,.07)
cube('Upper suite linen duvet',(9,4.35,4.77),(2.12,2.48,.3),linen,.14)
for x in [8.5,9.5]:cube('Upper suite pillows',(x,5.22,5.0),(.87,.55,.21),linen,.1)
cube('Upper suite upholstered headboard',(9,5.67,5.1),(2.38,.2,1.2),sage,.08)
area('Upper salon luminous ceiling',(2.8,3.7,7.25),295,(1,.77,.53),4.5,(2.8,3.6,4.4))
area('Upper suite luminous ceiling',(9.0,3.2,7.22),160,(1,.73,.43),2.5,(9,3.6,4.4))
# Terrace pair of teak sunbeds and a low ceramic table.
for x in [5.0,7.2]:
 cube('Upper terrace teak daybed',(x,-1.26,4.4),(1.38,2.1,.20),woodlight,.05)
 cube('Upper terrace linen daybed',(x,-1.26,4.57),(1.30,2.02,.20),linen,.1)
 cube('Upper terrace head cushion',(x,-.48,4.76),(1.15,.46,.18),linen,.08)
cyl('Upper terrace pedestal table',(6.1,-1.8,4.65),.29,.5,travertine,48,.02)
# Terrace strip gives the cantilever a low, warm edge rather than a bright neon line.
cube('Upper terrace concealed bronze drip',(4.3,-2.94,4.03),(14,.025,.04),bronze,.004)

print('UPPER_RESIDENCE_READY',flush=True)
# Taller stair lantern / atelier. Independent tapered limestone planes anchor the glass.
active=collections['10 Stair lantern']
cube('Stair tower foundation',(-5.0,8.25,.14),(5.1,4.5,.55),stone,.05)
cube('Stair lantern west blade',(-7.30,8.25,5.35),(.40,4.6,10.4),stone,.035)
cube('Stair lantern rear blade',(-5.0,10.42,5.35),(5.0,.38,10.4),stone,.035)
cube('Stair lantern thin east pier',(-2.62,9.75,5.35),(.27,1.7,10.4),stone,.03)
cube('Stair lantern floating cap',(-4.95,8.1,10.68),(5.45,5.05,.28),stone,.06)
cube('Atelier warm timber ceiling',(-4.9,8.08,10.49),(4.9,4.7,.07),wood,.01)
for x in [-7.06,-4.95,-2.82]:cube('Stair lantern bronze vertical',(x,6.03,5.4),(.055,.09,10.15),charcoal,.008)
for z in [.4,4.15,7.85,10.48]:cube('Stair lantern bronze horizontal',(-4.95,6.03,z),(4.3,.09,.05),charcoal,.006)
for left,right in [(-7.03,-4.99),(-4.91,-2.86)]:
 for bottom,top in [(.44,4.12),(4.18,7.82),(7.88,10.45)]:cube('Stair lantern low iron glazing',((left+right)/2,6.04,(bottom+top)/2),(right-left,.016,top-bottom),glass)
for level in [4.1,7.8]:cube('Stair lantern landing',(-4.9,9.8,level),(4.3,1.08,.18),travertine,.02)
# Actual stepped stair flights with a central open well.
for level in range(2):
 basez=.35+3.72*level
 for i in range(11):
  y=6.42+i*.285;z=basez+i*.169
  cube('West ascending oak stair tread',(-6.35,y,z),(1.35,.32,.09),woodlight,.018)
  cube('East returning oak stair tread',(-3.55,9.27-i*.285,basez+1.86+i*.169),(1.35,.32,.09),woodlight,.018)
 cube('Intermediate stair landing',(-4.95,9.52,basez+1.86),(4.2,.63,.14),travertine,.02)
 rod('West flight bronze handrail',(-5.7,6.4,basez+1.05),(-5.7,9.25,basez+2.74),.022,bronze)
 rod('East flight bronze handrail',(-4.2,9.27,basez+2.91),(-4.2,6.42,basez+4.6),.022,bronze)
 for i in range(6):
  rod('Stair rail bronze upright',(-5.7,6.4+i*.57,basez+i*.338),(-5.7,6.4+i*.57,basez+i*.338+1.05),.012,bronze)
# Third-level atelier and bridge from tower to main upper residence.
cube('Atelier upper floor',(-4.95,8.25,7.87),(4.35,4.2,.18),travertine,.02)
cube('Atelier writing desk',(-5.0,7.55,8.70),(2.35,.85,.09),woodlight,.04)
for x in [-5.9,-4.1]:cube('Atelier desk trestle',(x,7.55,8.3),(.13,.65,.75),wood,.02)
old=set(bpy.data.objects);dining_chair(-5,8.35,0)
for obj in set(bpy.data.objects)-old:
 if obj.parent is None:obj.location.z+=7.55
cube('Atelier open sketchbook',(-5.15,7.5,8.77),(.68,.42,.018),pages,.006)
lathe('Atelier glazed vessel',(-4.15,7.55,8.75),[(.08,0),(.15,.15),(.11,.28)],ceramic)
area('Atelier ceiling light',(-5,8.1,10.3),130,(1,.76,.5),2.5,(-5,8,8))
area('Stair lantern glow',(-5.2,8,7.6),180,(1,.70,.40),2.5,(-5.2,8,3))
cube('Upper link bridge floor',(-1.75,6.6,4.12),(2.1,1.65,.22),travertine,.035)
cube('Upper link bridge glass guard',(-1.7,7.39,4.77),(2.12,.018,1.1),glass,.005)
# The tower is laid in large coursed stone rather than a blank monolith.
active=collections['10 Stair lantern']
for z in [1.15,2.05,2.95,3.85,4.75,5.65,6.55,7.45,8.35,9.25,10.15]:
 cube('Lantern west blade stone bed',(-7.504,8.25,z),(.008,4.55,.008),gravel)
 cube('Lantern rear stone bed',(-5.0,10.614,z),(4.96,.008,.008),gravel)
for y in [7.1,8.2,9.3]:cube('Lantern west blade vertical joint',(-7.504,y,5.3),(.008,.008,10.2),gravel)
# Deep bronze downlights sit flush in the shaded soffit.
active=collections['09 Upper residence']
for x in [-1.4,1.7,4.8,7.9,10.5]:
 cyl('Upper soffit recessed bronze downlight',(x,-1.1,7.426),.065,.018,bronze,24,.005)
 cyl('Upper soffit warm opal lens',(x,-1.1,7.414),.045,.005,led,24,0)

# Thin upper-level terrace planting trough, keep plants below the sight line.
active=collections['11 Roof gardens']
for x,y,w,d in [(-2.1,-1.3,.72,2.65),(10.55,-1.28,.72,2.65),(12.8,3.8,4.15,1.1)]:
 cube('Roof garden limestone trough',(x,y,4.4),(w,d,.49),stone,.035)
 cube('Roof garden soil',(x,y,4.66),(w-.15,d-.15,.025),soil,.01)
 # clustered hemispheres are fine foliage masses at this scale, not cartoon topiary.
 for i in range(max(4,int(w*d*4))):
  xx=x+random.uniform(-w*.35,w*.35);yy=y+random.uniform(-d*.35,d*.35)
  sphere('Roof rosemary fine mound',(xx,yy,4.78),(.22,.22,.23),leaves[i%4],12,8)
# Solar canopy set behind the atelier rather than pasted over the main design.
for i in range(5):
 obj=cube('Atelier integrated photovoltaic panel',(-6.65+i*.84,8.4,10.88),(.79,2.65,.045),charcoal,.01);obj.rotation_euler.x=math.radians(6)
 for j in range(5):cube('Photovoltaic silver cell ribbon',(-6.65+i*.84,7.35+j*.52,10.88+(j*.52-1.05)*math.sin(math.radians(6))),(.75,.008,.008),bronze)
# Lateral garden pavilion foundations and tower expansion keep the terrace readable.
print('ARCHITECTURE_READY',flush=True)
exec(compile((Path(__file__).parent/'garden_extension.py').read_text(),'garden_extension.py','exec'),globals())
exec(compile((Path(__file__).parent/'backdrop.py').read_text(),'backdrop.py','exec'),globals())
# Golden afternoon with crisp but gentle shadows and warm furnished rooms.
world=scene.world;nodes=world.node_tree.nodes
for node in nodes:
 if node.type=='BACKGROUND':node.inputs['Strength'].default_value=.32
 if node.type=='TEX_SKY':node.sun_elevation=math.radians(22);node.sun_rotation=math.radians(225)
sun=bpy.data.objects.get('Low warm afternoon sun');sun.data.energy=2.0;sun.data.angle=math.radians(2.5);sun.data.color=(1,.87,.73);sun.location=(-18,-22,25);sun.rotation_euler=(Vector((0,0,0))-sun.location).to_track_quat('-Z','Y').to_euler()
scene.view_settings.exposure=-.35
for obj in scene.objects:
 if obj.type=='LIGHT' and obj.data.type=='AREA':
  obj.visible_glossy=False;obj.visible_camera=False;obj.visible_transmission=False
  if hasattr(obj.data,'transmission_factor'):obj.data.transmission_factor=0
  if hasattr(obj.data,'specular_factor'):obj.data.specular_factor=0
active=collections['08 Cameras']
for obj in list(active.objects):bpy.data.objects.remove(obj,do_unlink=True)
hero=camera('01 | Expanded garden residence',(33,-44,19),(2,-5.6,2.65),40,.0,14);hero.data.dof.use_dof=False
pool=camera('02 | Poolside architecture',(5,-25,4.8),(2,1,3.5),32,0,11);pool.data.dof.use_dof=False
atelier=camera('03 | Garden leisure',(-25,-30,11),(2.5,-5.6,2.45),34,0,12);atelier.data.dof.use_dof=False
scene.camera=hero;scene.render.resolution_x=2600;scene.render.resolution_y=1700;scene.render.resolution_percentage=100
scene.cycles.samples=192;scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.025
scene['project']='STILLWATER HOUSE II';scene['design']='Stepped limestone residence, glazed stair atelier and expansive leisure garden';scene['version']='2';scene['concept_only']='Original architectural concept; not construction or engineering documentation'
for _screen in bpy.data.screens:
 for _area in _screen.areas:
  if _area.type=='VIEW_3D':
   _area.spaces.active.region_3d.view_perspective='CAMERA'
   _area.spaces.active.shading.type='MATERIAL'
   _area.spaces.active.overlay.show_overlays=False
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Stillwater-House-II.blend'),compress=True)
summary={'project':'Stillwater House II','blender':bpy.app.version_string,'objects':len(scene.objects),'materials':len(bpy.data.materials),'mesh_vertices':sum(len(o.data.vertices) for o in scene.objects if o.type=='MESH'),'cameras':[hero.name,pool.name,atelier.name],'units':'meters','maximum_architecture_height_m':10.98,'main_residence_width_m':23,'external_assets':[],'original_preserved':True}
(OUT/'scene-manifest.json').write_text(json.dumps(summary,indent=2));print('SCENE_READY',json.dumps(summary),flush=True)
if _v2_options.mode=='preview':
 scene.render.resolution_x=1200;scene.render.resolution_y=785;scene.cycles.samples=40;scene.cycles.adaptive_threshold=.06;scene.render.filepath=str(OUT/'renders'/'draft-01.png');bpy.ops.render.render(write_still=True)
print('COMPLETE',flush=True)
