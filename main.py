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
# rows = 5
# cols = 5
depth = 1

glass_squares = bpy.data.collections.new('GlassSquares')
light_squares = bpy.data.collections.new('LightSquares')

bpy.context.scene.collection.children.link(glass_squares)
bpy.context.scene.collection.children.link(light_squares)

bpy.ops.mesh.primitive_cube_add(
    # size=random.uniform(0.2, 0.9),
    size=1.0,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, 0),
    # rotation=(random.random(), random.random(), random.random()),
    scale=(1, 1, 1)
)
glass_x_array = bpy.context.active_object.modifiers.new(name='glass-x-array', type='ARRAY')
glass_x_array.count = cols
glass_x_array.relative_offset_displace[0] = 2
glass_x_array.relative_offset_displace[1] = 0
glass_x_array.relative_offset_displace[2] = 0
glass_z_array = bpy.context.active_object.modifiers.new(name='glass-z-array', type='ARRAY')
glass_z_array.count = rows
glass_z_array.relative_offset_displace[0] = 0
glass_z_array.relative_offset_displace[1] = 0
glass_z_array.relative_offset_displace[2] = 2
glass_squares.objects.link(bpy.context.active_object)

bpy.ops.mesh.primitive_cube_add(
    # size=random.uniform(0.2, 0.9),
    size=0.2,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, 0),
    # rotation=(random.random(), random.random(), random.random()),
    scale=(1, 1, 1)
)
light_x_array = bpy.context.active_object.modifiers.new(name='light-x-array', type='ARRAY')
light_x_array.count = cols
light_x_array.relative_offset_displace[0] = 10
light_x_array.relative_offset_displace[1] = 0
light_x_array.relative_offset_displace[2] = 0
light_z_array = bpy.context.active_object.modifiers.new(name='light-z-array', type='ARRAY')
light_z_array.count = rows
light_z_array.relative_offset_displace[0] = 0
light_z_array.relative_offset_displace[1] = 0
light_z_array.relative_offset_displace[2] = 10
light_squares.objects.link(bpy.context.active_object)

bpy.ops.object.select_all(action='DESELECT')

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
glass_material = bpy.data.materials.new("glass-material")
glass_material.use_nodes = True
for node in glass_material.node_tree.nodes:
    glass_material.node_tree.nodes.remove(node)
glass_bsdf = glass_material.node_tree.nodes.new('ShaderNodeBsdfGlass')
glass_bsdf.inputs["Roughness"].default_value = random.uniform(0, 0.2)
glass_bsdf.inputs["IOR"].default_value = random.uniform(0, 20)
glass_bsdf.distribution = 'MULTI_GGX'
glass_out = glass_material.node_tree.nodes.new('ShaderNodeOutputMaterial')
glass_material.node_tree.links.new(glass_bsdf.outputs['BSDF'], glass_out.inputs['Surface'])

for obj in glass_squares.objects:
    obj.data.materials.append(glass_material)

light_material = bpy.data.materials.new("light-material")
light_material.use_nodes = True
for node in light_material.node_tree.nodes:
    light_material.node_tree.nodes.remove(node)
emission = light_material.node_tree.nodes.new('ShaderNodeEmission')
emission.inputs["Strength"].default_value = random.uniform(0, 200)
emission.inputs["Color"].default_value = (
    random.uniform(0.5, 1),
    random.uniform(0.5, 1),
    random.uniform(0.5, 1),
    random.uniform(0.5, 1)
)
light_out = light_material.node_tree.nodes.new('ShaderNodeOutputMaterial')
light_material.node_tree.links.new(emission.outputs['Emission'], light_out.inputs['Surface'])


for obj in light_squares.objects:
    obj.data.materials.append(light_material)

# world stuff
world = bpy.data.worlds.new("scene-world")
world.use_nodes = True
for node in world.node_tree.nodes:
    world.node_tree.nodes.remove(node)
world_out = world.node_tree.nodes.new('ShaderNodeOutputWorld')
sky = world.node_tree.nodes.new('ShaderNodeTexSky')
sky.sky_type = 'NISHITA'
sky.sun_disc = False
sky.sun_elevation = random.uniform(0, .6)
sky.sun_rotation = random.uniform(0, 4)
sky.air_density = random.uniform(0, 10)
sky.dust_density = random.uniform(0, 10)
sky.ozone_density = random.uniform(0, 10)
world.node_tree.links.new(sky.outputs['Color'], world_out.inputs['Surface'])

world.color = (
    random.uniform(0.0, 0.2),
    random.uniform(0.0, 0.2),
    random.uniform(0.0, 0.2)
)

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

scene.render.resolution_x = 16 * 100
scene.render.resolution_y = 9 * 100
scene.render.resolution_percentage = 40

bpy.context.scene.render.filepath = os.path.join(
    os.curdir,
    'untitled-cycles.png'
)
bpy.context.scene.render.engine = 'CYCLES'
bpy.ops.render.render(write_still=True)

bpy.ops.wm.save_as_mainfile(filepath="output.blend")
