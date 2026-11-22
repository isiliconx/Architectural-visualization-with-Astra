"""Package the verified scene and all three final PNGs using only the standard library."""
from pathlib import Path
import hashlib,json,struct,zipfile

root=Path(__file__).parent
sources=['base_scene.py','geometry.py','build_scene.py','garden_extension.py','backdrop.py','render_scene.py','verify_scene.py','package_release.py','stillwater_ii_notebook.py','README.md','LICENSE-ASSETS.md','PLAN.md','scene-manifest.json','validation.json','render-environment.json','preservation.json']
shots=[('01-Expanded-Residence',2600,1700),('02-Poolside-Architecture',2400,1600),('03-Garden-Leisure',2600,1700)]
receipts=[]
for i,(name,w,h) in enumerate(shots,1):
    path=root/'renders'/f'{name}.png'
    header=path.read_bytes()[:24]
    assert header[:8]==b'\x89PNG\r\n\x1a\n',path
    assert struct.unpack('>II',header[16:24])==(w,h),path
    rec=json.loads((root/f'render-receipt-{i}.json').read_text())
    assert (rec['width'],rec['height'])==(w,h),rec
    receipts.append(rec)
(root/'render-receipts.json').write_text(json.dumps(receipts,indent=2))
assert json.loads((root/'validation.json').read_text())['status']=='passed'
assert json.loads((root/'preservation.json').read_text())['all_original_manifest_hashes_match']

def checksums(paths):
    return '\n'.join(f"{hashlib.file_digest((root/name).open('rb'),'sha256').hexdigest()}  {name}" for name in paths)+'\n'

def package(name,paths):
    with zipfile.ZipFile(root/name,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for item in paths:z.write(root/item,item)
    with zipfile.ZipFile(root/name) as z:assert z.testzip() is None
    print(name,(root/name).stat().st_size,'bytes')

(root/'SOURCE-SHA256SUMS').write_text(checksums(sources))
package('Stillwater-II-Source.zip',sources+['SOURCE-SHA256SUMS'])
files=sources+['SOURCE-SHA256SUMS','render-receipts.json','Stillwater-House-II.blend']+[f'renders/{name}.png' for name,_,_ in shots]
(root/'SHA256SUMS').write_text(checksums(files))
package('Stillwater-House-II-Complete.zip',files+['SHA256SUMS'])
print('RELEASE_VERIFIED')
