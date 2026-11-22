"""Direct mesh primitives avoid repeated dependency-graph updates during generation."""
def cube(name,loc,scale,mat,bevel=0,rot=None):
    x,y,z=[v*.5 for v in scale]
    vs=[(-x,-y,-z),(-x,-y,z),(-x,y,-z),(-x,y,z),(x,-y,-z),(x,-y,z),(x,y,-z),(x,y,z)]
    fs=[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]
    fs=[tuple(reversed(f)) for f in fs]
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);active.objects.link(o);o.location=loc
    if rot:o.rotation_euler=rot
    if mat:me.materials.append(mat)
    if bevel:
        mod=o.modifiers.new('Soft crafted edges','BEVEL');mod.width=bevel;mod.segments=3
        o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    return o

def sphere(name,loc,scale,mat,seg=24,rings=12):
    vs=[];fs=[]
    for j in range(rings+1):
        p=pi*j/rings
        for i in range(seg):
            a=2*pi*i/seg;vs.append((scale[0]*sin(p)*cos(a),scale[1]*sin(p)*sin(a),scale[2]*cos(p)))
    for j in range(rings):
        for i in range(seg):fs.append((j*seg+i,j*seg+(i+1)%seg,(j+1)*seg+(i+1)%seg,(j+1)*seg+i))
    fs=[tuple(reversed(f)) for f in fs]
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);active.objects.link(o);o.location=loc;me.materials.append(mat)
    for face in me.polygons:face.use_smooth=True
    return o

def _cone(name,loc,r1,r2,depth,mat,verts,bevel):
    vs=[]
    for z,r in [(-depth*.5,r1),(depth*.5,r2)]:
        vs.extend([(r*cos(2*pi*i/verts),r*sin(2*pi*i/verts),z) for i in range(verts)])
    fs=[tuple(reversed(range(verts))),tuple(range(verts,2*verts))]
    fs.extend([(i,(i+1)%verts,(i+1)%verts+verts,i+verts) for i in range(verts)])
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);active.objects.link(o);o.location=loc;me.materials.append(mat)
    for face in me.polygons[2:]:face.use_smooth=True
    if bevel:
        mod=o.modifiers.new('Edge glint','BEVEL');mod.width=bevel;mod.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o

def cyl(name,loc,radius,depth,mat,verts=32,bevel=.015):
    return _cone(name,loc,radius,radius,depth,mat,verts,bevel)

def rod(name,a,b,r,mat,r2=None):
    d=Vector(b)-Vector(a);mid=(Vector(a)+Vector(b))*.5
    o=_cone(name,mid,r,r if r2 is None else r2,d.length,mat,12,.004 if r2 is None else 0)
    o.rotation_euler=d.to_track_quat('Z','Y').to_euler();return o
