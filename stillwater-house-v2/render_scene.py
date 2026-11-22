"""Render one or all saved Stillwater II viewpoints."""
import bpy,sys,argparse,json,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',default=str(Path(__file__).parent));p.add_argument('--samples',type=int,default=192);p.add_argument('--preview',action='store_true');p.add_argument('--shot',type=int,default=0);p.add_argument('--gpu',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
r=Path(a.output).resolve();bpy.ops.wm.open_mainfile(filepath=str(r/'Stillwater-House-II.blend'));s=bpy.context.scene
s.cycles.samples=a.samples;s.cycles.use_denoising=bpy.app.build_options.cycles and (bpy.app.version >= (4,5,0));s.cycles.adaptive_threshold=.05 if a.preview else .02
s.cycles.device='CPU'
if a.gpu:
 try:
  q=bpy.context.preferences.addons['cycles'].preferences;q.compute_device_type='OPTIX';q.get_devices()
  devices=[d for d in q.devices if d.type=='OPTIX']
  if devices:
   for d in q.devices:d.use=d.type=='OPTIX'
   s.cycles.device='GPU'
 except Exception:pass
s.render.threads_mode='FIXED';s.render.threads=8
shots=[('01 | Expanded garden residence','01-Expanded-Residence',2600,1700),('02 | Poolside architecture','02-Poolside-Architecture',2400,1600),('03 | Garden leisure','03-Garden-Leisure',2600,1700)]
receipts=[]
for i,(camera,name,w,h) in enumerate(shots,1):
 if a.shot and a.shot!=i:continue
 s.camera=bpy.data.objects[camera];s.render.resolution_x=w;s.render.resolution_y=h;s.render.resolution_percentage=46 if a.preview else 100;s.render.filepath=str(r/'renders'/(name+('-draft' if a.preview else '')+'.png'))
 t=time.time();bpy.ops.render.render(write_still=True)
 rec={'name':name,'width':int(w*s.render.resolution_percentage/100),'height':int(h*s.render.resolution_percentage/100),'samples':s.cycles.samples,'seconds':round(time.time()-t,3),'device':s.cycles.device,'blender':bpy.app.version_string};receipts.append(rec);print('SHOT_READY',json.dumps(rec),flush=True)
 (r/('render-receipt-'+str(i)+('-draft' if a.preview else '')+'.json')).write_text(json.dumps(rec,indent=2))
print('ALL_SHOTS_COMPLETE',flush=True)
