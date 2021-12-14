import math
import random
import bpy
import os

# select all stuff
for obj in bpy.context.scene.objects:
    obj.select_set(True)

# delete all stuff
bpy.ops.object.delete()

rows = 20
cols = 30
depth = 1

for y in range(depth):
    for i in range(rows * cols):
        bpy.ops.mesh.primitive_cube_add(
            # size=random.uniform(0.2, 0.9),
            size=1.0 - y * .3,
            enter_editmode=False,
            align='WORLD',
            location=((i % cols) * 2, y * 2, (i // cols) * 2),
            # rotation=(random.random(), random.random(), random.random()),
            scale=(1, 1, 1)
        )

for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
    else:
        obj.select_set(False)

emission_color = (
    random.uniform(0.0, 1),
    random.uniform(0.0, 1),
    random.uniform(0.0, 1),
    random.uniform(0.0, 1),
)

subsurface = random.uniform(0, .2)
subsurface_radius = (
    10,
    10,
    10
)
material = bpy.data.materials.new("square-material")
material.use_nodes = True
nodes = material.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
bsdf.inputs["Metallic"].default_value = random.uniform(0, 100)
# bsdf.inputs["Subsurface"].default_value = subsurface
# bsdf.inputs["Subsurface Radius"].default_value = subsurface_radius

highlighted_materials = bpy.data.materials.new("square-material")
highlighted_materials.use_nodes = True
nodes = highlighted_materials.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
# bsdf.inputs["Subsurface"].default_value = subsurface
# bsdf.inputs["Subsurface Radius"].default_value = subsurface_radius
bsdf.inputs["Emission Strength"].default_value = random.uniform(0, 0.4)
bsdf.inputs["Emission"].default_value = (
    1,
    1,
    1,
    1
)

for obj in bpy.context.selected_objects:
    obj.data.materials.append(highlighted_materials if random.random() >= 0.8 else material)

# world stuff
world = bpy.data.worlds.new("scene-world")

world.color = (
    random.uniform(0.0, 0.2),
    random.uniform(0.0, 0.2),
    random.uniform(0.0, 0.2)
)
# world.mist_settings.use_mist = True
# world.mist_settings.start = 1
# world.mist_settings.depth = 2
# world.mist_settings.falloff = 'LINEAR'
# world.mist_settings.intensity = 0.99

bpy.context.scene.world = world
# end world stuff


# light stuff
front_light = bpy.data.lights.new(name="light-front", type='POINT')
front_light.energy = random.uniform(100, 300)
front_light.color = (
    random.uniform(0, 30),
    random.uniform(0, 30),
    random.uniform(0, 30)
)

front_light_object = bpy.data.objects.new(name="scene-light-front", object_data=front_light)

bpy.context.collection.objects.link(front_light_object)

front_light_object.location = (
    random.uniform(10, 30),
    random.uniform(-4, -10),
    random.uniform(10, 20),
)

back_light = bpy.data.lights.new(name="light-back", type='POINT')
back_light.energy = random.uniform(50, 200)
back_light.color = (
    random.uniform(0, 30),
    random.uniform(0, 30),
    random.uniform(0, 30)
)

back_light_object = bpy.data.objects.new(name="scene-light-back", object_data=back_light)

bpy.context.collection.objects.link(back_light_object)

back_light_object.location = (
    random.uniform(0, 30),
    random.uniform(4, 20),
    random.uniform(0, 20),
)
# end light stuff

# camera stuff
bpy.ops.object.camera_add(enter_editmode=False)
bpy.context.scene.camera = bpy.context.object
scene = bpy.data.scenes["Scene"]

tx = 2.0
ty = -10.0
tz = 2.0

rx = 110.0
ry = 2.0
rz = -30.0

fov = 80
scene.camera.data.angle = fov*(math.pi/180.0)

scene.camera.rotation_mode = 'XYZ'
scene.camera.rotation_euler[0] = rx*(math.pi/180.0)
scene.camera.rotation_euler[1] = ry*(math.pi/180.0)
scene.camera.rotation_euler[2] = rz*(math.pi/180.0)

scene.camera.location.x = tx
scene.camera.location.y = ty
scene.camera.location.z = tz
# end camera stuff

bpy.ops.wm.save_as_mainfile(filepath="output.blend")

scene.render.resolution_x = 16 * 100
scene.render.resolution_y = 9 * 100
scene.render.resolution_percentage = 200

bpy.context.scene.render.filepath = os.path.join(
    os.curdir,
    'untitled-cycles.png'
)
bpy.context.scene.render.engine = 'CYCLES'
bpy.ops.render.render(write_still=True)

bpy.context.scene.render.filepath = os.path.join(
    os.curdir,
    'untitled-eevee.png'
)
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.ops.render.render(write_still=True)
