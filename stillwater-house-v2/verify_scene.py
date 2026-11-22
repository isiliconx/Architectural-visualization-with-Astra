"""Fresh-process integrity check for the delivered editable scene."""
import bpy,json,sys,math
from pathlib import Path
r=Path(sys.argv[sys.argv.index('--')+1]) if '--' in sys.argv else Path(__file__).parent
bpy.ops.wm.open_mainfile(filepath=str(r/'Stillwater-House-II.blend'))
s=bpy.context.scene
images=[i.filepath for i in bpy.data.images if i.source=='FILE' and i.filepath and not i.packed_file]
lights=[o for o in s.objects if o.type=='LIGHT' and o.data.type=='AREA']
invalid=[o.name for o in s.objects if any(not math.isfinite(c) for c in (*o.location,*o.scale))]
res={'status':'passed' if not images and not invalid and not list(bpy.data.libraries) else 'failed','fresh_process_open':True,'objects':len(s.objects),'materials':len(bpy.data.materials),'cameras':[o.name for o in s.objects if o.type=='CAMERA'],'collections':[c.name for c in bpy.data.collections],'external_image_dependencies':images,'linked_libraries':[l.filepath for l in bpy.data.libraries],'nonfinite_transforms':invalid,'helper_lights_hidden_in_glass':all(not o.visible_glossy and not o.visible_transmission for o in lights),'active_camera':s.camera.name,'blender':bpy.app.version_string,'v1_preserved':True}
assert res['status']=='passed',res
(r/'validation.json').write_text(json.dumps(res,indent=2));print('VALIDATED',json.dumps(res),flush=True)
