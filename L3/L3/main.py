import numpy as np
import matplotlib.pyplot as plt
import pygame

def translatie_2d(tx, ty):
    return np.array([[1, 0, tx],
                     [0, 1, ty],
                     [0, 0, 1]], dtype=float)

def scalare_2d(sx, sy):
    return np.array([[sx, 0, 0],
                     [0, sy, 0],
                     [0, 0, 1]], dtype=float)

def rotatie_2d(ang_rad):
    c, s = np.cos(ang_rad), np.sin(ang_rad)
    return np.array([[c, -s, 0],
                     [s,  c, 0],
                     [0,  0, 1]], dtype=float)

def reflect_ox():
    return np.array([[1, 0, 0],
                     [0,-1, 0],
                     [0, 0, 1]], dtype=float)

def reflect_oy():
    return np.array([[-1, 0, 0],
                     [ 0, 1, 0],
                     [ 0, 0, 1]], dtype=float)

def reflect_origin():
    return np.array([[-1, 0, 0],
                     [ 0,-1, 0],
                     [ 0, 0, 1]], dtype=float)

def shear_2d(shx=0.0, shy=0.0):
    return np.array([[1, shx, 0],
                     [shy, 1, 0],
                     [0,   0, 1]], dtype=float)


def triunghi():
    pts = np.array([[-0.6, 0.6, 0.0],
                    [-0.4,-0.4, 0.8],
                    [ 1.0, 1.0, 1.0]])
    return pts

def patrat(w=1.0, h=1.0):
    hw, hh = w/2.0, h/2.0
    pts = np.array([[-hw,  hw,  hw, -hw],
                    [-hh, -hh,  hh,  hh],
                    [ 1.0, 1.0, 1.0, 1.0]])
    return pts

def poligon_regular(n=6, r=0.6):
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    x = r * np.cos(angles)
    y = r * np.sin(angles)
    ones = np.ones_like(x)
    return np.vstack([x, y, ones])

def aplica(M, pts):
    return M @ pts

def plot_2d(pts, ax=None, title="-", show=True, color='C0'):
    X = pts[0, :]
    Y = pts[1, :]
    Xc = np.append(X, X[0])
    Yc = np.append(Y, Y[0])
    if ax is None:
        plt.figure(figsize=(5,5))
        plt.plot(Xc, Yc, marker='o', color=color)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(True)
        plt.title(title)
        if show:
            plt.show()
    else:
        ax.plot(Xc, Yc, marker='o', color=color)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True)
        ax.set_title(title)

def meniul_principal():
    shapes = {
        '1': ("Triunghi", triunghi()),
        '2': ("Patrat", patrat(1.0,1.0)),
        '3': ("Dreptunghi", patrat(1.0,0.6)),
        '4': ("Poligon", poligon_regular(5)),
    }
    current_name = "Patrat"
    current_pts = patrat(1.0,1.0).copy()
    composed = np.eye(3)
    while True:
        print("\nMeniu")
        print("0 - Selectarea figurii")
        print("1 - Afișeaza figurile 2D")
        print("2 - Aplica transformari")
        print("3 - Afiseaza figura 2D transformata")
        print("4 - Afiseaza matricea compusa curenta")
        print("5 - Pygame")
        print("6 - Transformari compuse")
        print("7 - Iesire")
        opt = input("Alege o optiune: ").strip()
        if opt == "0":
            print("Alege o forma")
            for k,v in shapes.items():
                print(f"{k}) {v[0] if v[1] is not None else v[0]}")
            ch = input("Alegere: ").strip()
            if ch in shapes and ch != '6':
                current_name, current_pts = shapes[ch][0], shapes[ch][1].copy()
                composed = np.eye(3)
                print(f"Setat: {current_name}")
        elif opt == "1":
            print("Figuri disponibile (afisare):")
            figs = [triunghi(), patrat(1.0,1.0), patrat(1.0,0.6), poligon_regular(5)]
            titles = ["Triunghi", "Patrat", "Dreptunghi", "Poligon"]
            fig, axs = plt.subplots(2,2, figsize=(10,6))
            axs = axs.flatten()
            for i, (f,t) in enumerate(zip(figs, titles)):
                plot_2d(f, ax=axs[i], title=t)
            axs[-1].axis('on')
            plt.tight_layout()
            plt.show()
        elif opt == "2":
            print("Introdu secventa de transformari:")
            seq = []
            while True:
                code = input("Transformare (T/S/R/RX/RY/RO/SH) sau 'stop' când termini: ").strip().upper()
                if code == 'STOP':
                    break
                if code not in ('T','S','R','RX','RY','RO','SH'):
                    print("Cod invalid.")
                    continue
                if code == 'T':
                    tx = float(input("tx: "))
                    ty = float(input("ty: "))
                    seq.append(translatie_2d(tx,ty))
                elif code == 'S':
                    sx = float(input("sx: "))
                    sy = float(input("sy: "))
                    seq.append(scalare_2d(sx,sy))
                elif code == 'R':
                    deg = float(input("unghi în grade (ex 30 sau -45): "))
                    seq.append(rotatie_2d(np.deg2rad(deg)))
                elif code == 'RX':
                    seq.append(reflect_ox())
                elif code == 'RY':
                    seq.append(reflect_oy())
                elif code == 'RO':
                    seq.append(reflect_origin())
                elif code == 'SH':
                    shx = float(input("shx (shear X by Y): "))
                    shy = float(input("shy (shear Y by X): "))
                    seq.append(shear_2d(shx, shy))
                print("Adaugat. Introdu urmatoarea transformare sau 'stop'.")
            comp = np.eye(3)
            for M in seq:
                comp = M @ comp
            composed = comp @ composed
            current_pts = aplica(comp, current_pts)
        elif opt == "3":
            print(f"Afisare: {current_name} (initial si transformat)")
            fig, ax = plt.subplots(1,1, figsize=(6,6))
            plot_2d(aplica(np.eye(3), current_pts), ax=ax, title=f"{current_name} (curent)", show=False, color='C1')
            plt.show()
        elif opt == "4":
            print("Matrice compusa curenta:")
            np.set_printoptions(precision=4, suppress=True)
            print(composed)
        elif opt == "5":
            interactive_2d_pygame(current_pts, current_name)
        elif opt == "6":
            print("Construieste manual o matrice compusa (ex: T @ R @ S).")
            seq = []
            while True:
                code = input("Transformare (T/S/R/RX/RY/RO/SH) sau 'stop': ").strip().upper()
                if code == 'STOP':
                    break
                if code not in ('T','S','R','RX','RY','RO','SH'):
                    print("Cod invalid.")
                    continue
                if code == 'T':
                    tx = float(input("tx: ")); ty = float(input("ty: "))
                    seq.append(translatie_2d(tx,ty))
                elif code == 'S':
                    sx = float(input("sx: ")); sy = float(input("sy: "))
                    seq.append(scalare_2d(sx,sy))
                elif code == 'R':
                    deg = float(input("deg: "))
                    seq.append(rotatie_2d(np.deg2rad(deg)))
                elif code == 'RX':
                    seq.append(reflect_ox())
                elif code == 'RY':
                    seq.append(reflect_oy())
                elif code == 'RO':
                    seq.append(reflect_origin())
                elif code == 'SH':
                    shx = float(input("shx: ")); shy = float(input("shy: "))
                    seq.append(shear_2d(shx, shy))
            if len(seq) == 0:
                print("Nicio transformare introdusa.")
                continue
            comp = np.eye(3)
            for M in seq:
                comp = M @ comp
            print("Matrice compusa:")
            np.set_printoptions(precision=4, suppress=True)
            print(comp)
            current_pts = aplica(comp, current_pts)
            composed = comp @ composed
            print("Aplicata pe figura curenta.")
        elif opt == "7":
            break
        else:
            print("Opțiune invalida.")

def interactive_2d_pygame(initial_pts, title="-"):
    pygame.init()
    W, H = 900, 700
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)

    pts_base = initial_pts.copy()
    M = np.eye(3)

    trans_step = 0.02
    rot_step = np.deg2rad(5)
    scale_up = 1.05
    scale_down = 0.95
    shear_step = 0.05
    view_scale = 250
    cx, cy = W//2, H//2

    info_lines_static = [
        "Sageti = translatie",
        "Q/E = rotire ",
        "W/S = scalare ",
        "A/Z = forfecare X",
        "X/C = forfecare Y",
        "F = reflexie Ox",
        "G = reflexie Oy",
        "H = reflexie origine",
        "R = reset",
        "esc = iesire",
        "1/2/3 = Triunghi/Patrat/Poligon"
    ]
    presets = [triunghi(), patrat(1.0,1.0), poligon_regular(6)]
    preset_names = ["Triunghi", "Patrat", "Poligon"]
    preset_idx = 0
    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                if ev.key == pygame.K_r:

                    M = np.eye(3)
                    pts_base = initial_pts.copy()
                if ev.key == pygame.K_1:
                    pts_base = presets[0].copy(); preset_idx = 0; M = np.eye(3)
                if ev.key == pygame.K_2:
                    pts_base = presets[1].copy(); preset_idx = 1; M = np.eye(3)
                if ev.key == pygame.K_3:
                    pts_base = presets[2].copy(); preset_idx = 2; M = np.eye(3)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            M = translatie_2d(-trans_step, 0) @ M
        if keys[pygame.K_RIGHT]:
            M = translatie_2d(trans_step, 0) @ M
        if keys[pygame.K_UP]:
            M = translatie_2d(0, trans_step) @ M
        if keys[pygame.K_DOWN]:
            M = translatie_2d(0, -trans_step) @ M
        if keys[pygame.K_q]:
            M = rotatie_2d(rot_step) @ M
        if keys[pygame.K_e]:
            M = rotatie_2d(-rot_step) @ M
        if keys[pygame.K_w]:
            M = scalare_2d(scale_up, scale_up) @ M
        if keys[pygame.K_s]:
            M = scalare_2d(scale_down, scale_down) @ M
        if keys[pygame.K_a]:
            M = shear_2d(shear_step, 0) @ M
        if keys[pygame.K_z]:
            M = shear_2d(-shear_step, 0) @ M
        if keys[pygame.K_x]:
            M = shear_2d(0, shear_step) @ M
        if keys[pygame.K_c]:
            M = shear_2d(0, -shear_step) @ M
        if keys[pygame.K_f]:
            M = reflect_ox() @ M
        if keys[pygame.K_g]:
            M = reflect_oy() @ M
        if keys[pygame.K_h]:
            M = reflect_origin() @ M
        screen.fill((28, 30, 34))
        transformed = aplica(M, pts_base)
        pts = []
        for i in range(transformed.shape[1]):
            x_obj, y_obj = transformed[0, i], transformed[1, i]
            x_px = cx + x_obj * view_scale
            y_px = cy - y_obj * view_scale
            pts.append((int(x_px), int(y_px)))
        if len(pts) > 1:
            for i in range(len(pts)):
                pygame.draw.line(screen, (200,200,220), pts[i], pts[(i+1)%len(pts)], 3)
                pygame.draw.circle(screen, (255,100,100), pts[i], 5)
        y = 8
        for line in info_lines_static:
            surf = font.render(line, True, (220,220,220))
            screen.blit(surf, (8, y))
            y += 18
        Mtext = np.array2string(M, precision=2, suppress_small=True)
        lines_mat = Mtext.splitlines()
        y += 6
        screen.blit(font.render("Matrice compusa:", True, (200,200,100)), (8, y)); y += 16
        for ln in lines_mat:
            surf = font.render(ln.strip(), True, (180,180,180))
            screen.blit(surf, (8, y))
            y += 16
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    return
if __name__ == "__main__":
    meniul_principal()
