# Import javascript modules
import imaplib
import imghdr
from js import THREE, window, document, Object, console
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math


#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer
    
    # Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0xF0EEE9)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.y = 20
    camera.position.x = 0
    camera.lookAt(THREE.Vector3.new(100,100,100))
    
    scene.add(camera)

    # Directional light
    color = 0xFFFFFF
    intensity = 0.5
    light = THREE.DirectionalLight.new(color, intensity)
    light.position.set(0, 20, -10)
    scene.add(light)

    # Directional light
    color = 0xFFFFFF
    intensity = 0.7
    light = THREE.DirectionalLight.new(color, intensity)
    light.position.set(-10, 20, 10)
    scene.add(light)

    # Spotlight
    spotLight1 = THREE.SpotLight.new(color, intensity)
    spotLight1.position.set(15, 15, 15)
    spotLight1.target.position.set(0, 0, 0)
    spotLight1.castShadow = True
    scene.add(spotLight1)
    
    spotLight1 = THREE.SpotLight.new(color, intensity)
    spotLight1.position.set(10, 10, 30)
    spotLight1.castShadow = True
    spotLight1.target.position.set(10, 10, 0)
    scene.add(spotLight1)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
  
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)
    '''THREE.Orbit.Controls.target(THREE.Vector3.new(100,100,100))'''
    # Axis Helper
    '''axesHelper = THREE.AxesHelper.new(10)
    scene.add(axesHelper)'''
    #-----------------------------------------------------------------------
    # Set up GUI
    global floorsettings, default_apartment_type, default_apartment_variant, floor_length_x, floor_length_y, floor_ratio_1, floor_ratio_2, floor_ratio_3, floor_ratio_4,floor_ratio_5, floor_ratio_6








    #-----------------------------------------------------------------------
    default_apartment_type = 1
    default_apartment_variant = 1
    floor_length_x = 14
    floor_length_y = 12
    
    floor_ratio_1 = 1/2
    floor_ratio_2 = 1/2
    floor_ratio_3 = 1/2
    floor_ratio_4 = 1/2
    floor_ratio_5 = 1/2
    floor_ratio_6 = 1/2
    

    floorsettings = {
        "default_apartment_type": default_apartment_type,
        "default_apartment_variant": default_apartment_variant,
        "length_x": floor_length_x,
        "length_y": floor_length_y,
        "ratio_1": floor_ratio_1,
        "ratio_2": floor_ratio_2,
        "ratio_3": floor_ratio_3,
        "ratio_4": floor_ratio_4,
        "ratio_5": floor_ratio_5,
        "ratio_6": floor_ratio_6,
    }
    floorsettings = Object.fromEntries(to_js(floorsettings))

    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Apatrment_Generation')
    param_folder.add(floorsettings,'default_apartment_type', 1,3,1)
    param_folder.add(floorsettings,'default_apartment_variant', 1,4,1)

    param_folder = gui.addFolder('Floor Settings')
    param_folder.add(floorsettings,'length_x', 1,20)
    param_folder.add(floorsettings,'length_y', 1,20)

    param_folder = gui.addFolder('Ratios')
    param_folder.add(floorsettings,'ratio_1', 0.2,0.8)
    param_folder.add(floorsettings,'ratio_2', 0.2,0.8)
    param_folder.add(floorsettings,'ratio_3', 0.2,0.8)
    param_folder.add(floorsettings,'ratio_4', 0.2,0.8)
    param_folder.add(floorsettings,'ratio_5', 0.2,0.8)
    param_folder.add(floorsettings,'ratio_6', 0.2,0.8)
    
    '''param_folder.open()'''

    #-----------------------------------------------------------------------
    # Create Materials
    # Mesh Material
    global material, material1, line_material
    material = THREE.MeshPhongMaterial.new()
    material.color = THREE.Color.new(0xFFFFFF)
    material.transparent = True
    material.opacity = 1

    material1 = THREE.MeshPhongMaterial.new()
    material1.color = THREE.Color.new(0x815FFF)
    material1.transparent = True
    material1.opacity = 1
    # Line Material
    line_material = THREE.LineBasicMaterial.new()
    line_material.color = THREE.Color.new(0x1B1B1B)
    #-----------------------------------------------------------------------
    # Lists
    global final_rooms, lines, new_rooms, offset_rooms, shapes, room_sqaremeters

    #Roomlists
    # rooms = [room_1, room_2, ..., room_n] room_n = [point_1, point_2, point_3, point_4]
    final_rooms = []
    lines = []
    new_rooms = []
    offset_rooms = []
    shapes = []
    room_sqaremeters = []
    

    # Impliment 
    # Original room
    firstroom = define_room(0, 0, floor_length_x, 0, floor_length_x , floor_length_y, 0, floor_length_y)
    new_rooms.append(firstroom)

    
    
    
    #Apartements
    Apartement(floorsettings.default_apartment_type,floorsettings.default_apartment_variant)
   
    
    #offset rooms for Wall vertices
    offset_out(new_rooms[0], 0.2)
    offset_in(final_rooms, 0.1)


    '''drawrooms(offset_rooms)
    drawrooms(offset_room_out)'''
    
    extrude(offset_room_out, offset_rooms)
    extrude_floor(offset_room_out)
    #squaremeters functions
    '''squaremeters(offset_rooms)'''

    render()
#-----------------------------------------------------------------------
# HELPER FUNCTIONS

# room definition
def define_room(p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y):
    room = []
    p1 = p1_x, p1_y
    p2 = p2_x, p2_y
    p3 = p3_x, p3_y
    p4 = p4_x, p4_y
    room.append(p1)
    room.append(p2) 
    room.append(p3) 
    room.append(p4)
    return room

# Function to subdivide a room vertically
def subdivide_vertical(room, ratio):
    global new_rooms
    new_room1 = define_room(room[0][0], room[0][1], room[1][0] - ((room[1][0]-room[0][0]) * ratio), room[1][1], room[2][0] - ((room[2][0]-room[3][0]) * ratio), room[2][1], room[3][0], room[3][1])
    new_room2 = define_room(room[1][0] - ((room[1][0]-room[0][0]) * ratio), room[0][1], room[1][0], room[1][1], room[2][0], room[2][1], room[2][0] - ((room[2][0]-room[3][0]) * ratio), room[3][1])
    new_rooms.append(new_room1)
    new_rooms.append(new_room2)

# Function to subdivide a room horizontally
def subdivide_horizontal(room, ratio):
    global new_rooms
    new_room1 = define_room(room[0][0], room[0][1], room[1][0], room[1][1], room[2][0], room [2][1] - ((room [2][1] - room [1][1]) * ratio), room[3][0], room[3][1] - (room[3][1] - room[0][1])* ratio)
    new_room2 = define_room(room[0][0], room[3][1] - ((room[3][1] - room[0][1]) * ratio), room[1][0], room[2][1] - ((room[2][1] - room[1][1]) * ratio), room[2][0], room[2][1], room[3][0], room[3][1])
    new_rooms.append(new_room1)
    new_rooms.append(new_room2)

# tree function for room variants      
def variante(syntax, ratios):
    
    index = -1
    for letter in syntax:
        index +=1
        if letter == 'V':
            subdivide_vertical(new_rooms[index], ratios[index])
        elif letter == 'H':
            subdivide_horizontal(new_rooms[index], ratios[index])
        else:
            pass
            final_rooms.append(new_rooms[index])


#--------------------------
# Apartement variation functions
#A1 = Loft Default
def Apartement_1(number):
    if number == 1:
        variante(['V', 'H', 'H', 0, 0,0 ,0],[1/3, 1/3, 1/2, 0, 0, 0,0])
    elif number == 2:
        variante(['H', 'H', 'V', 0, 0,0 ,0],[1/2, 1/3, 1/4, 0, 0, 0,0])
    elif number == 3:
        variante(['V', 0,'H', 'H', 0, 0 ,0],[1/4,0,2/5, 3/5, 0, 0,0])
    elif number == 4:
        variante(['V','H',0, 'H', 0, 0 ,0],[1/2, 1/3,0, 1/4, 0, 0,0])
    pass

#A1 = Loft GUI
def Apartement_1_GUI(number):
    if number == 1:
        variante(['V', 'H', 'H', 0, 0,0 ,0],[gui_LR_size, gui_MB_size, gui_K_size, 0, 0, 0,0])
    elif number == 2:
        variante(['H', 'H', 'V', 0, 0,0 ,0],[gui_LR_size, gui_MB_size, gui_K_size, 0, 0, 0,0])
    elif number == 3:
        variante(['V', 0,'H', 'H', 0, 0 ,0],[gui_LR_size,0,gui_MB_size, gui_K_size, 0, 0,0])
    elif number == 4:
        variante(['V','H',0, 'H', 0, 0 ,0],[gui_LR_size, gui_K_size,0, gui_MB_size, 0, 0,0])
    pass

#  --------------------------

#A2 = Single Default
def Apartement_2(number):
    if number == 1:
        variante(['V', 'H', 'H', 'V',0,0, 0, 0, 0],[1/2,1/2,1/3,1/2, 0,0,0,0,0])
    elif number == 2:
        variante(['H', 'V', 'H', 'H',0,0, 0, 0, 0],[1/2,2/3,3/4,2/3, 0,0,0,0,0])
    elif number == 3:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],[5/7,1/2,1/3,0,0,0, 2/5,0,0])
    elif number == 4:
        variante(['V', 'H', 'H', 0, 0, 0, 'H', 0, 0],[1/3,1/3,2/3,0,0,0, 2/3,0,0])
    pass


#A2 = Single GUI
def Apartement_2_GUI(number):
    if number == 1:
        variante(['V', 'H', 'H', 'V',0,0, 0, 0, 0],[1/2, gui_K_size,gui_LR_size, gui_BE_size, 0,0,0,0,0])
    elif number == 2:
        variante(['H', 'V', 'H', 'H',0,0, 0, 0, 0],[gui_LR_size,gui_BE_size,3/4,gui_K_size, 0,0,0,0,0])
    elif number == 3:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],[gui_LR_size,gui_MB_size,gui_K_size,0,0,0,gui_BA_size,0,0])
    elif number == 4:
        variante(['V', 'H', 'H', 0, 0, 0, 'H', 0, 0],[gui_LR_size,gui_K_size,gui_MB_size,0,0,0,gui_BE_size,0,0])
    pass


#--------------------------
#A3 = Family Default
def Apartement_3(number):
    if number == 1:
        variante(['H', 'V',0, 'V','V', 0, 'H',0, 0, 0,0],[3/5,1/2,0,1/2,1/3, 0,2/5,0,0,0,0])
    elif number == 2:
        variante(['V', 'H', 'V', 'V',0,0, 0, 0, 'H', 0, 0],[1/2,1/2,3/4,1/2,0, 0,0,0,1/2,0,0])
    elif number == 3:
        variante(['H', 'V','V', 'H', 0, 0, 0, 0,'V', 0, 0],[3/7,1/2,1/3,1/2, 0,0,0,0,2/5,0,0])
    elif number == 4:
        variante(['V', 'H', 'V', 'V',0,0, 0, 0, 'H', 0, 0],[1/2,1/2,3/4,1/2,0, 0,0,0,1/2,0,0])
    pass

#A3 = Family GUI
def Apartement_3_GUI(number):
    if number == 1:
        variante(['H', 'V',0, 'V','V', 0, 'H',0, 0, 0],[gui_LR_size,1/2,0,gui_K_size,gui_MB_size, 0,gui_BA_size,0,0,0])
    elif number == 2:
        variante(['V', 'H', 'V', 'V',0,0, 0, 0, 'H', 0, 0],[gui_LR_size, gui_K_size, 3/4,gui_MB_size,0, 0, 0, 0, gui_BA_size, 0, 0])
    elif number == 3:
        variante(['H', 'V','V', 'H', 0, 0, 0, 0,'V', 0, 0],[gui_LR_size,gui_K_size,1/3,gui_MB_size, 0,0,0,0,gui_BA_size,0,0])
    elif number == 4:
        variante(['V', 'H', 'V', 'V',0,0, 0, 0, 'H', 0, 0],[gui_LR_size, gui_K_size, 3/4,gui_MB_size,0, 0, 0, 0, gui_BA_size, 0, 0])
    pass





#--------------------------

# Apartment function Default
def Apartement(type, number):

    if type == 1:
        Apartement_1(number)
    elif type == 2:
         Apartement_2(number)
    elif type == 3:
         Apartement_3(number)
    pass

# Apartment function GUI
def Apartement_GUI(type, number):

    if type == 1:
        Apartement_1_GUI(number)
    elif type == 2:
         Apartement_2_GUI(number)
    elif type == 3:
         Apartement_3_GUI(number)
    pass

#randomize syntax
import random

def randomize_syntax():
    syntax = []
    for i in range(7):
        random_number = random.random()
        if random_number < 0.33:
            syntax.append("V")
        elif random_number < 0.67:
            syntax.append("H")
        else:
            syntax.append(0)
    return syntax

syntax = randomize_syntax()




#--------------------------
#offset room outside function by changing the vertices
def offset_out(room, d):
    global new_rooms, offset_room_out
    offset_room_out = []
    offset_room = define_room(room[0][0] - d , room[0][1] - d , room[1][0] + d , room[1][1] - d , room[2][0] + d , room [2][1] + d, room[3][0] - d, room[3][1] + d)
    offset_room_out.append(offset_room)

#offset room inside function by changing the vertices
def offset_in(rooms, d):
    global new_rooms, offset_rooms
    for room in rooms:
        offset_room = define_room(room[0][0] + d , room[0][1] + d , room[1][0] - d , room[1][1] + d , room[2][0] - d , room [2][1] - d, room[3][0] + d, room[3][1] - d)
        offset_rooms.append(offset_room)

#lists for update

# extrude roomShapes
def extrude(boundary, rooms):
    global wall
    shape_geometry = THREE.Shape.new()
    #boundary extrusion
    shape_geometry.moveTo(boundary[0][0][0],boundary[0][0][1])
    shape_geometry.lineTo(boundary[0][1][0],boundary[0][1][1])
    shape_geometry.lineTo(boundary[0][2][0],boundary[0][2][1])
    shape_geometry.lineTo(boundary[0][3][0],boundary[0][3][1])
    shape_geometry.lineTo(boundary[0][0][0],boundary[0][0][1])

    #holes
    for room in rooms:

        room_hole = THREE.Path.new()
        
        room_hole.moveTo(room[0][0],room[0][1])
        room_hole.lineTo(room[1][0],room[1][1])
        room_hole.lineTo(room[2][0],room[2][1])
        room_hole.lineTo(room[3][0],room[3][1])
        room_hole.lineTo(room[0][0],room[0][1])

        shape_geometry.holes.push(room_hole)

    
    extrudeSettings = (1,1,False,0,0,0,0)
    extrudeSettings = {
	"steps": 10,
	"depth": 3,
	"bevelEnabled": False,
    }
    extrudeSettings = Object.fromEntries(to_js(extrudeSettings))
    geometry = THREE.ExtrudeGeometry.new( shape_geometry, extrudeSettings)
    
    wall = THREE.Mesh.new(geometry, material)
    wall.translateX(-(floor_length_x*0.8))
    wall.translateZ(-(floor_length_y*1/2))
    wall.rotateX(3.14159265359*1/2)
    scene.add(wall)


def extrude_floor(boundary):
    global floor
    shape_geometry = THREE.Shape.new()
    #boundary extrusion
    shape_geometry.moveTo(boundary[0][0][0],boundary[0][0][1])
    shape_geometry.lineTo(boundary[0][1][0],boundary[0][1][1])
    shape_geometry.lineTo(boundary[0][2][0],boundary[0][2][1])
    shape_geometry.lineTo(boundary[0][3][0],boundary[0][3][1])
    shape_geometry.lineTo(boundary[0][0][0],boundary[0][0][1])
    
    extrudeSettings = (-1,-1,False,0,0,0,0)
    extrudeSettings = {
	"steps": 10,
	"depth": 0.5,
	"bevelEnabled": False,
    }
    extrudeSettings = Object.fromEntries(to_js(extrudeSettings))
    geometry = THREE.ExtrudeGeometry.new( shape_geometry, extrudeSettings)
    
    floor = THREE.Mesh.new(geometry, material1)
    floor.translateX(-(floor_length_x*0.8))
    floor.translateZ(-(floor_length_y*1/2))
    floor.translateY(-3)
    floor.rotateX(3.14159265359*1/2)
    scene.add(floor)

#---------------------------
#unnecessary functions

# Function to get list of room squaremeters
def squaremeters(rooms):

    for room in rooms:
        
        x_size = (room[1][0] - room[0][0])
        y_size = (room[3][1] - room[0][1])
        squaremeters = x_size * y_size
        room_sqaremeters.append(squaremeters)

    print(room_sqaremeters)

# Function for total Squaremeters
def apartement_squaremeters(squaremeter_list):
    
    total_squaremeters = sum(squaremeter_list)
    return total_squaremeters

# draw rooms
def drawrooms(rooms):

    
    for line in lines:
        scene.remove(line)

    for room in rooms:
        points = []
        point1 = THREE.Vector2.new(room[0][0],room[0][1])
        point2 = THREE.Vector2.new(room[1][0],room[1][1])
        point3 = THREE.Vector2.new(room[2][0],room[2][1])
        point4 = THREE.Vector2.new(room[3][0],room[3][1])

        points.append(point1)
        points.append(point2)
        points.append(point3)
        points.append(point4)
        points.append(point1)

        line_geometry = THREE.BufferGeometry.new()
        line_geometry.setFromPoints(to_js(points))
        line = THREE.Line.new(line_geometry, line_material)
        lines.append(line)
        scene.add(line)
#-----------------------------------------------------------------------------------

# update
def update():
    global  wall, room, gui_floor_length_x, gui_floor_length_y, final_rooms, lines, new_rooms, offset_rooms, shapes, room_sqaremeters, floor_ratio_1, floor_ratio_2, floor_ratio_3, floor_ratio_4, floor_ratio_5, floor_ratio_6

    

   
    #-----------------------------------------------------------------------------------
     #-----------------------------------------------------------------------------------
    #GET THE VALUES FROM THE LOCAL STORAGE
    #get the value of type and value of Variant from the local storage
    global gui_floor_length_x, gui_floor_length_y, gui_LR_size, gui_K_size, gui_MB_size, gui_BE_size, gui_BA_size, gui_apartment_type, gui_apartment_variant, temp_a_t, temp_a_v

    '''default_apartment_type = (window.localStorage.getItem("type"))
    floorsettings.default_apartment_type_id = (document.getElementById("type").value)

    floorsettings.apartment_variant = window.localStorage.getItem("type")

    #vtest = document.getElementById("type").value
    console.log(floorsettings.default_apartment_type)
    vtest2 = window.localStorage.getItem("Variant")'''







    #get the type of the apartment
    gui_apartment_type    = (window.localStorage.getItem("apartement_type"))

    #get the variant of the apartment
    gui_apartment_variant = (window.localStorage.getItem("apartement_variant"))

    #get the floor lenghts from the local storage
    gui_floor_length_x = float(window.localStorage.getItem("apartementSize_lenghtX"))
    gui_floor_length_y = float(window.localStorage.getItem("apartementSize_lenghtY"))
    gui_LR_size        = float(window.localStorage.getItem("livingroomSize"))/100
    gui_K_size         = float(window.localStorage.getItem("KitchenSize"))/100
    gui_BE_size        = float(window.localStorage.getItem("BedroomSize"))/100
    gui_BA_size        = float(window.localStorage.getItem("BathroomSize"))/100
    gui_MB_size        = float(window.localStorage.getItem("MasterbedroomSize"))/100
    





    '''test1 = float(document.getElementById("apartementSize_lenghtX").value)
    test2 = float(document.getElementById("apartementSize_lenghtY").value)
    gui_LR_size = float(document.getElementById("livingroomSize").value)/100
    gui_K_size = float(document.getElementById("KitchenSize").value)/100
    gui_MB_size = float(document.getElementById("BedroomSize").value)/100
    gui_BE_size = float(document.getElementById("BathroomSize").value)/100
    gui_BA_size = float(document.getElementById("MasterbedroomSize").value)/100'''



     #-----------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------

    temp_a_t = 1
    temp_a_v = 1




     #update for Buttons
    if  gui_apartment_type != temp_a_t or gui_apartment_variant != temp_a_v:
        
        temp_a_t = gui_apartment_type
        temp_a_v = gui_apartment_variant

        scene.remove(wall)
        scene.remove(floor)
        room = []
        final_rooms = []
        lines = []
        new_rooms = []
        offset_rooms = []
        shapes = []
        room_sqaremeters = []
    

        update_room = define_room(0, 0, gui_floor_length_x, 0, gui_floor_length_x , gui_floor_length_y, 0, gui_floor_length_y)
        new_rooms.append(update_room)


        floor_ratio_1 = 20/100
        floor_ratio_2 = 20/100
        floor_ratio_3 = 20/100
        floor_ratio_4 = 20/100
        floor_ratio_5 = 20/100


        if gui_LR_size != floor_ratio_1 or gui_K_size != floor_ratio_2 or gui_MB_size != floor_ratio_3 or gui_BE_size != floor_ratio_4 or gui_BA_size != floor_ratio_5:
            Apartement_GUI(int(gui_apartment_type),int(gui_apartment_variant))
        else:
            Apartement(int(gui_apartment_type),int(gui_apartment_variant))

        offset_out(new_rooms[0], 0.2)
        offset_in(final_rooms, 0.1)
        
        extrude(offset_room_out, offset_rooms)
        extrude_floor(offset_room_out)
        scene.add(wall)
        scene.add(floor)

    else:
        pass
    








    ''' #update Sliders
    if gui_LR_size != floor_ratio_1 or gui_K_size != floor_ratio_2 or gui_MB_size != floor_ratio_3 or gui_BE_size != floor_ratio_4 or gui_BA_size != floor_ratio_5:

        



        scene.remove(wall)
        scene.remove(floor)
        room = []
        final_rooms = []
        lines = []
        new_rooms = []
        offset_rooms = []
        shapes = []
        room_sqaremeters = []

    

        update_room = define_room(0, 0, gui_floor_length_x, 0, gui_floor_length_x , gui_floor_length_y, 0, gui_floor_length_y)
        new_rooms.append(update_room)

        Apartement_GUI(int(gui_apartment_type),int(gui_apartment_variant))

        offset_out(new_rooms[0], 0.2)
        offset_in(final_rooms, 0.1)
        
        extrude(offset_room_out, offset_rooms)
        extrude_floor(offset_room_out)
        scene.add(wall)
        scene.add(floor)

    else:
        pass

        '''













    #------------------------------
    '''
    #update type
    if  gui_apartment_type != default_apartment_type or gui_apartment_variant != default_apartment_variant or test1 != floor_length_x or test2 != floor_length_y:
        
        scene.remove(wall)
        scene.remove(floor)
        room = []
        final_rooms = []
        lines = []
        new_rooms = []
        offset_rooms = []
        shapes = []
        room_sqaremeters = []
    

        update_room = define_room(0, 0, test1, 0, test1 , test2, 0, test2)
        new_rooms.append(update_room)
        
        Apartement(gui_apartment_type,gui_apartment_variant)
        
        offset_out(new_rooms[0], 0.2)
        offset_in(final_rooms, 0.1)
        
        extrude(offset_room_out, offset_rooms)
        extrude_floor(offset_room_out)
        scene.add(wall)
        scene.add(floor)

    else:
        pass


        #now update the ratios
    if gui_LR_size != floor_ratio_1 or gui_K_size != floor_ratio_2 or gui_MB_size != floor_ratio_3 or gui_BE_size != floor_ratio_4 or gui_BA_size != floor_ratio_5 or floorsettings.ratio_6 != floor_ratio_6:
        
        scene.remove(wall)
        scene.remove(floor)
        room = []
        final_rooms = []
        lines = []
        new_rooms = []
        offset_rooms = []
        shapes = []
        room_sqaremeters = []

    

        update_room = define_room(0, 0, test1, 0, test1 , test2, 0, test2)
        new_rooms.append(update_room)

        Apartement_GUI(gui_apartment_type,gui_apartment_variant)

        offset_out(new_rooms[0], 0.2)
        offset_in(final_rooms, 0.1)
        
        extrude(offset_room_out, offset_rooms)
        extrude_floor(offset_room_out)
        scene.add(wall)
        scene.add(floor)

    else:
        pass

        '''

























        
    '''    #update Variant
    if  floorsettings.default_apartment_variant != default_apartment_variant:
        scene.remove(wall)
        scene.remove(floor)
        room = []
        final_rooms = []
        lines = []
        new_rooms = []
        offset_rooms = []
        shapes = []
        room_sqaremeters = []
    

        update_room = define_room(0, 0, test1, 0, test1 , test2, 0, test2)
        new_rooms.append(update_room)

    
    
        
        Apartement_GUI(floorsettings.default_apartment_type,floorsettings.default_apartment_variant)
        
        offset_out(new_rooms[0], 0.2)
        offset_in(final_rooms, 0.1)
        
        extrude(offset_room_out, offset_rooms)
        extrude_floor(offset_room_out)
        scene.add(wall)
        scene.add(floor)

        
    else:
        pass

    
    #update functions for the floor lenghts
    if test1 != floor_length_x or test2 != floor_length_y:
        
        scene.remove(wall)
        scene.remove(floor)
        room = []
        floor_length_x = test1
        floor_length_y = test2

        final_rooms = []
        lines = []
        new_rooms = []
        offset_rooms = []
        shapes = []
        room_sqaremeters = []

        


        update_room = define_room(0, 0, test1, 0, test1 , test2, 0, test2)
        new_rooms.append(update_room)

        Apartement(floorsettings.default_apartment_type,floorsettings.default_apartment_variant,r_living_room_size,r_kitchen_size,r_Bedroom_size,r_bathroom_size,r_Masterbedroom_size)

        offset_out(new_rooms[0], 0.2)
        offset_in(final_rooms, 0.1)
        
        extrude(offset_room_out, offset_rooms)
        extrude_floor(offset_room_out)
        scene.add(wall)
        scene.add(floor)
    else:
        pass
    #update ratios
    if  gui_LR_size != floor_ratio_1 or gui_K_size != floor_ratio_2 or gui_MB_size != floor_ratio_3 or gui_BE_size != floor_ratio_4 or gui_BA_size != floor_ratio_5 or floorsettings.ratio_6 != floor_ratio_6:
        scene.remove(wall)
        scene.remove(floor)
        room = []
        final_rooms = []
        lines = []
        new_rooms = []
        offset_rooms = []
        shapes = []
        room_sqaremeters = []


        floor_ratio_1 = r_living_room_size = gui_LR_size
        floor_ratio_2 = r_kitchen_size = gui_K_size
        floor_ratio_3 = r_Bedroom_size = gui_MB_size
        floor_ratio_4 = r_bathroom_size = gui_BE_size
        floor_ratio_5 = r_Masterbedroom_size = gui_BA_size
    

        update_room = define_room(0, 0, test1, 0, test1 , test2, 0, test2)
        new_rooms.append(update_room)

        Apartement(floorsettings.default_apartment_type,floorsettings.default_apartment_variant,r_living_room_size,r_kitchen_size,r_Bedroom_size,r_bathroom_size,r_Masterbedroom_size)

        offset_out(new_rooms[0], 0.2)
        offset_in(final_rooms, 0.1)
        
        extrude(offset_room_out, offset_rooms)
        extrude_floor(offset_room_out)
        scene.add(wall)
        scene.add(floor)

        #------------------------default_apartment_type = 3
    #default_apartment_variant = 1
    else:
        pass'''


        










        
# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update()
    controls.update()
    composer.render()
    
    
    

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()


