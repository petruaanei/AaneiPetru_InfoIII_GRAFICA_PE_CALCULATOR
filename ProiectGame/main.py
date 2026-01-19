from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
window.title = 'Lost Island'
window.exit_button.visible = False
window.fps_counter.enabled = False
window.collider_counter.enabled = False
window.entity_counter.enabled = False
random.seed(7)

def safe_texture(path: str):
    try:
        t = load_texture(path)
        return path if t else None
    except:
        return None

def safe_model_path(path: str):
    try:
        m = load_model(path)
        return path if m else None
    except:
        return None

def in_circle(x, z, r):
    return (x*x + z*z) <= r*r

def random_point_in_ring(r_min, r_max):
    while True:
        x = random.uniform(-r_max, r_max)
        z = random.uniform(-r_max, r_max)
        if in_circle(x, z, r_max) and not in_circle(x, z, r_min):
            return Vec3(x, 0, z)

def random_point_on_island():
    return random_point_in_ring(7, 52)

def far_enough(pos: Vec3, used: list, min_dist: float) -> bool:
    for u in used:
        if distance(pos, u) < min_dist:
            return False
    return True

def scatter_positions(count: int, min_dist: float, max_tries: int = 8000):
    used = []
    tries = 0
    while len(used) < count and tries < max_tries:
        tries += 1
        p = random_point_on_island()
        if far_enough(p, used, min_dist):
            used.append(p)
    return used

game_started = False
game_over = False
win = False
max_hp = 100
hp = 100
max_hunger = 100
hunger = 100
parts_collected = 0
parts_needed = 3
WALK_SPEED = 6
SPRINT_SPEED = 11

menu_panel = Entity(parent=camera.ui, enabled=True)
Text("Lost Island", parent=menu_panel, scale=2, y=0.25,origin=(0,0),x=0,color=color.black)
btn_start = Button(text="Start", parent=menu_panel, scale=(0.25, 0.08), y=0.05,color=color.dark_gray,text_color=color.green)
btn_exit  = Button(text="Exit",  parent=menu_panel, scale=(0.25, 0.08), y=-0.07,color=color.dark_gray,text_color=color.red)

hud = Entity(parent=camera.ui, enabled=False)
hud_hp     = Text(text="HP: 100", parent=hud, x=-0.87, y=0.45, scale=1.2, color=color.red)
hud_hunger = Text(text="Hunger: 100", parent=hud, x=-0.87, y=0.40, scale=1.2, color=color.green)
hud_parts  = Text(text="Radio parts: 0/3", parent=hud, x=-0.87, y=0.35, scale=1.2, color=color.blue)
hud_radio  = Text(text="Radio: ?", parent=hud, x=-0.87, y=0.30, scale=1.2, color=color.orange)
hint_text  = Text(text="", parent=hud, y=-0.35, scale=1.3, origin=(0, 0), color=color.black)
end_text   = Text(text="", parent=camera.ui, enabled=False, scale=2, y=0.1, origin=(0, 0),color=color.black)

def set_hint(s: str):
    hint_text.text = s

def update_hud():
    hud_hp.text = f"HP: {int(hp)}"
    hud_hunger.text = f"Hunger: {int(hunger)}"
    hud_parts.text = f"Radio parts: {parts_collected}/{parts_needed}"
    dist = int(distance(player.position, radio_pos))
    hud_radio.text = f"Radio: {dist}m"

Sky()
scene.fog_density = 0.016
scene.fog_color = color.rgb(135, 165, 195)
AmbientLight(color=color.rgba(55, 60, 75, 255))
sun = DirectionalLight(shadows=True)
sun.color = color.rgba(255, 244, 220, 255)
sun.look_at(Vec3(1, -1.2, 0.5))
try:
    sun.shadow_map_resolution = 2048
except:
    pass

tex_sand = safe_texture('textures/sand_normal') or safe_texture('sand')
tex_water_ground = safe_texture('textures/water_normal') or safe_texture('water') or safe_texture('textures/water')
tex_wood = safe_texture('textures/wood_normal') or safe_texture('wood')

beach = Entity(model='plane', scale=160, y=0, collider='mesh')
if tex_water_ground:
    beach.texture = tex_water_ground
    beach.texture_scale = (35, 35)
else:
    beach.color = color.rgb(140, 140, 140)
beach.receive_shadows = True

interior = Entity(model='plane', scale=110, y=0.001)
interior.collider = None
if tex_sand:
    interior.texture = tex_sand
    interior.texture_scale = (35, 35)
else:
    interior.color = color.rgb(220, 210, 170)
interior.receive_shadows = True

water = Entity( model='plane',scale=900,y=-1.1,z=0,double_sided=True)
if tex_water_ground:
    water.texture = tex_water_ground
    water.texture_scale = (120, 120)
else:
    water.color = color.rgb(40, 120, 160)

water.alpha = 0.7
water.collider = None
water.receive_shadows = False

player = FirstPersonController(y=2.2, origin_y=-0.7, speed=WALK_SPEED)
player.cursor.visible = True

player.collider = BoxCollider(player, center=Vec3(0, 1, 0), size=Vec3(1.0, 2.0, 1.0))
player.gravity = 1
player.enabled = False

MODEL_PALM   = safe_model_path('models/coconut_palm.glb')   or safe_model_path('models/coconut_palm')
MODEL_ROCK1  = safe_model_path('models/rock_01.glb')     or safe_model_path('models/rock_01')
MODEL_ROCK2  = safe_model_path('models/rock_02.glb')     or safe_model_path('models/rock_02')
MODEL_CRATE  = safe_model_path('models/crate.glb')       or safe_model_path('models/crate')
MODEL_RADIO  = safe_model_path('models/radio_tower.glb') or safe_model_path('models/radio_tower')
MODEL_APPLE    = safe_model_path('models/apple.glb')        or safe_model_path('models/apple')
MODEL_BOTTLE   = safe_model_path('models/water_bottle.glb') or safe_model_path('models/water_bottle')
MODEL_BATTERY  = safe_model_path('models/battery.glb')      or safe_model_path('models/battery')
MODEL_CAMPFIRE = safe_model_path('models/campfire.glb')     or safe_model_path('models/campfire')

static_objects = []

def spawn_palm(pos):
    if not MODEL_PALM:
        e = Entity(model='cylinder', position=pos + Vec3(0,1,0), scale=(0.7,2,0.7), color=color.rgb(120,90,60))
        e.collider = BoxCollider(e, center=Vec3(0,1,0), size=Vec3(0.9, 2.0, 0.9))
        e.cast_shadows = True
        static_objects.append(e)
        return

    e = Entity(model=MODEL_PALM, position=pos, scale=2.2, rotation_y=random.uniform(0,360))
    e.collider = BoxCollider(e, center=Vec3(0, 1.25, 0), size=Vec3(0.75, 2.5, 0.75))
    e.cast_shadows = True
    e.receive_shadows = True
    static_objects.append(e)

def spawn_rock(pos):
    m = MODEL_ROCK1 or MODEL_ROCK2
    if MODEL_ROCK1 and MODEL_ROCK2:
        m = MODEL_ROCK1 if random.random() < 0.5 else MODEL_ROCK2

    s = random.uniform(1.2, 1.8)

    if not m:
        e = Entity(model='sphere', position=pos + Vec3(0, 0.6, 0), scale=s, color=color.rgb(110,110,110), collider='sphere')
        e.cast_shadows = True
        static_objects.append(e)
        return

    e = Entity(model=m, position=pos + Vec3(0, 0.08, 0), scale=s, rotation_y=random.uniform(0,360), collider='box')
    e.cast_shadows = True
    e.receive_shadows = True
    static_objects.append(e)

def spawn_crate(pos):
    s = 1.1
    if not MODEL_CRATE:
        e = Entity(model='cube', position=pos + Vec3(0,0.55,0), scale=(1,1,1), color=color.rgb(140,110,80), collider='box')
        e.cast_shadows = True
        static_objects.append(e)
        return

    e = Entity(model=MODEL_CRATE, position=pos, scale=s, rotation_y=random.uniform(0,360), collider='box')
    e.cast_shadows = True
    e.receive_shadows = True
    static_objects.append(e)

for _ in range(12):
    spawn_palm(random_point_in_ring(10, 48))
for _ in range(14):
    spawn_rock(random_point_in_ring(8, 46))
for _ in range(10):
    spawn_crate(random_point_in_ring(20, 54))

house_center = Vec3(16, 0, 8)
house_root = Entity(position=house_center)

house_floor = Entity(parent=house_root, model='plane', scale=(8, 8), y=0.0015, rotation_x=90)
if tex_sand:
    house_floor.texture = tex_sand
    house_floor.texture_scale = (8, 8)
else:
    house_floor.color = color.rgb(220, 210, 170)
house_floor.collider = None
house_floor.receive_shadows = True

wall_h = 3.0
wall_t = 0.30

wall_L = Entity(parent=house_root, model='cube', scale=(wall_t, wall_h, 8),
                x=-(4 + wall_t/2), y=wall_h/2, collider='box')
wall_R = Entity(parent=house_root, model='cube', scale=(wall_t, wall_h, 8),
                x=+(4 + wall_t/2), y=wall_h/2, collider='box')
wall_B = Entity(parent=house_root, model='cube', scale=(8, wall_h, wall_t),
                z=-(4 + wall_t/2), y=wall_h/2, collider='box')

door_gap = 2.4
front_seg_w = (8 - door_gap) / 2
wall_F1 = Entity(parent=house_root, model='cube', scale=(front_seg_w, wall_h, wall_t),
                 x=-(door_gap/2 + front_seg_w/2), z=(4 + wall_t/2), y=wall_h/2, collider='box')
wall_F2 = Entity(parent=house_root, model='cube', scale=(front_seg_w, wall_h, wall_t),
                 x=+(door_gap/2 + front_seg_w/2), z=(4 + wall_t/2), y=wall_h/2, collider='box')

roof = Entity(parent=house_root, model='cube', scale=(8.3, 0.35, 8.3), y=wall_h + 0.15)
roof.collider = None

for w in [wall_L, wall_R, wall_B, wall_F1, wall_F2, roof]:
    if tex_wood:
        w.texture = tex_wood
        w.texture_scale = (2, 2)
    else:
        w.color = color.rgb(140, 100, 70)
    w.cast_shadows = True
    w.receive_shadows = True

gate_pivot = Entity(parent=house_root, position=Vec3(0, 0, 4 + wall_t/2))
gate = Entity(parent=gate_pivot, model='cube', scale=(0.25, 2.7, 2.2),
              position=Vec3(0, 1.35, 0), collider='box')
if tex_wood:
    gate.texture = tex_wood
else:
    gate.color = color.rgb(140, 100, 70)
gate.cast_shadows = True
gate.receive_shadows = True
gate_open = False

interactables = []
pickup_entities = []

class Pickup(Entity):
    def __init__(self, kind, glb_model_path, glb_scale, glb_y=0.0, **kwargs):
        super().__init__(**kwargs)
        self.kind = kind
        interactables.append(self)
        pickup_entities.append(self)

        self.collider = BoxCollider(self, center=Vec3(0,0.45,0), size=Vec3(0.9,0.9,0.9))
        self.base_y = self.y + 0.20
        self.y = self.base_y
        self.rotation_y = random.uniform(0, 360)

        if glb_model_path:
            v = Entity(parent=self, model=glb_model_path, scale=glb_scale, y=glb_y, rotation_y=random.uniform(0, 360))
            v.cast_shadows = True
            v.receive_shadows = True
        else:
            self.model = 'cube'
            self.scale = 0.35
            self.color = color.yellow if kind == 'food' else color.cyan
            self.alpha = 0.85
            self.cast_shadows = True
            self.receive_shadows = True

def update_pickups_anim():
    for p in pickup_entities:
        if not p or not p.enabled:
            continue
        p.rotation_y += time.dt * 60
        p.y = p.base_y + math.sin(time.time()*2 + p.x*0.2) * 0.08

def spawn_pickups_random():
    NUM_APPLES  = 8
    NUM_BOTTLES = 8
    NUM_BATTERY = parts_needed
    total = NUM_APPLES + NUM_BOTTLES + NUM_BATTERY

    positions = scatter_positions(total, min_dist=4.2)
    idx = 0

    for _ in range(NUM_APPLES):
        pos = positions[idx]; idx += 1
        Pickup(kind='food', glb_model_path=MODEL_APPLE, glb_scale=4.8, glb_y=0.07, position=pos)

    for _ in range(NUM_BOTTLES):
        pos = positions[idx]; idx += 1
        Pickup(kind='food', glb_model_path=MODEL_BOTTLE, glb_scale=0.75, glb_y=0.00, position=pos)

    for _ in range(NUM_BATTERY):
        pos = positions[idx]; idx += 1
        Pickup(kind='part', glb_model_path=MODEL_BATTERY, glb_scale=0.70, glb_y=0.00, position=pos)

spawn_pickups_random()

radio_pos = Vec3(-18, 0, 18)
radio_terminal = Entity(position=radio_pos)
radio_terminal.collider = None
interactables.append(radio_terminal)

if MODEL_RADIO:
    radio_visual = Entity(parent=radio_terminal, model=MODEL_RADIO, scale=0.02, y=0)
else:
    radio_visual = Entity(parent=radio_terminal, model='cube', color=color.light_gray, scale=2, y=1)

radio_visual.cast_shadows = True
radio_visual.receive_shadows = True

radio_terminal.collider = BoxCollider(
    radio_terminal,
    center=Vec3(0, 2.8, 0),
    size=Vec3(1.2, 6.0, 1.2)
)

radio_light = PointLight(parent=radio_terminal, color=color.rgba(255, 220, 220, 255))
radio_light.y = 6
radio_light.intensity = 3

campfire_pos = Vec3(0, 0, -12)
campfire_root = Entity(position=campfire_pos)

if MODEL_CAMPFIRE:
    campfire_visual = Entity(parent=campfire_root, model=MODEL_CAMPFIRE, scale=1.1, y=0)
else:
    campfire_visual = Entity(parent=campfire_root, model='cone', color=color.rgb(255, 130, 40), scale=1.2, y=0.55)

campfire_visual.cast_shadows = True
campfire_visual.receive_shadows = True

campfire_light = PointLight(parent=campfire_root, color=color.rgba(255, 140, 60, 255), shadows=False)
campfire_light.y = 2.2
campfire_light.intensity = 3.2

embers = []
for _ in range(40):
    p = Entity(model='quad',
               color=color.rgba(255, 140, 0, 180),
               scale=0.08,
               position=campfire_root.position + Vec3(random.uniform(-0.45, 0.45),
                                                     random.uniform(0.0, 0.5),
                                                     random.uniform(-0.45, 0.45)),
               billboard=True)
    embers.append(p)

def try_interact():
    global hp, hunger, parts_collected, gate_open, win

    if distance(player.position, gate_pivot.world_position) < 2.6:
        gate_open = not gate_open
        return

    nearest, nearest_d = None, 999
    for e in interactables:
        if not e or not e.enabled:
            continue
        d = distance(player.position, e.position)
        if d < nearest_d:
            nearest, nearest_d = e, d

    if nearest is None or nearest_d > 2.3:
        return

    if nearest == radio_terminal:
        if parts_collected >= parts_needed:
            win = True
        else:
            set_hint(f"Need {parts_needed - parts_collected} more radio parts.")
        return

    if hasattr(nearest, 'kind'):
        global hunger, hp
        if nearest.kind == 'food':
            hunger = min(max_hunger, hunger + 35)
            hp = min(max_hp, hp + 8)
            destroy(nearest)
        elif nearest.kind == 'part':
            parts_collected += 1
            destroy(nearest)

def input(key):
    if key == 'e' and game_started and not game_over:
        try_interact()
    if key == 't' and game_started and not game_over:
        player.position = radio_pos + Vec3(0, 2, 0)

def start_game():
    global game_started
    game_started = True
    menu_panel.enabled = False
    hud.enabled = True
    mouse.locked = True
    player.enabled = True
    player.position = house_center + Vec3(0, 2, 0)
    player.rotation_y = 0

def exit_game():
    application.quit()

btn_start.on_click = start_game
btn_exit.on_click = exit_game

player.enabled = False

def update():
    global hp, hunger, game_over, win, gate_open

    if not game_started or game_over:
        return
    if held_keys['shift']:
        player.speed = SPRINT_SPEED
    else:
        player.speed = WALK_SPEED

    hunger -= time.dt * 2.0
    hunger = max(0, hunger)
    if hunger <= 0:
        hp -= time.dt * 6
    hp = max(0, hp)

    if distance(player.position, campfire_root.position) < 3:
        hp = min(max_hp, hp + time.dt * 2.2)

    target_rot = 92 if gate_open else 0
    gate_pivot.rotation_y = lerp(gate_pivot.rotation_y, target_rot, time.dt * 6)
    water.y = -1.1 + math.sin(time.time() * 0.45) * 0.08

    campfire_root.scale = 1 + math.sin(time.time() * 6) * 0.02
    campfire_light.intensity = 3.2 + math.sin(time.time() * 10) * 0.35

    for p in embers:
        p.y += time.dt * 0.75
        p.alpha -= time.dt * 0.6
        if p.alpha <= 0:
            p.position = campfire_root.position + Vec3(random.uniform(-0.45, 0.45),
                                                       random.uniform(0.0, 0.5),
                                                       random.uniform(-0.45, 0.45))
            p.alpha = 0.8

    update_pickups_anim()

    set_hint("")
    if distance(player.position, gate_pivot.world_position) < 2.6:
        set_hint("Press E to open/close door")
    else:
        for e in interactables:
            if e and e.enabled and distance(player.position, e.position) < 2.3:
                if e == radio_terminal:
                    if parts_collected >= parts_needed:
                        set_hint("Press E to call for help (WIN)")
                    else:
                        set_hint("Press E (Radio Tower)")
                elif hasattr(e, 'kind') and e.kind == 'food':
                    set_hint("Press E to eat (+Hunger)")
                elif hasattr(e, 'kind') and e.kind == 'part':
                    set_hint("Press E to pick up radio part")
                break

    update_hud()

    if hp <= 0:
        game_over = True
        end_text.text = "GAME OVER\nYou didn’t survive."
        end_text.enabled = True
        mouse.locked = False

    if win:
        game_over = True
        end_text.text = "YOU WON!\nHelp is coming."
        end_text.enabled = True
        mouse.locked = False

app.run()
