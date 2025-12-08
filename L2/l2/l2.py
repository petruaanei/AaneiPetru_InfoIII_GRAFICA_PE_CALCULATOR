import numpy as np
from numpy import linalg as LA
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pygame as pg

a=np.array([3,0])
b=np.array([0,2])
c=np.array([1,1])
u=np.array([1,0,0])
v=np.array([0,1,0])
w=np.array([0,0,1])

norma_a=LA.norm(a)
norma_b=LA.norm(b)
norma_c=LA.norm(c)
norma_u=LA.norm(u)
norma_v=LA.norm(v)
norma_w=LA.norm(w)

print(f"Vector a: {a}")
print(f"Norma a: {norma_a}")
print(f"Vector b: {b}")
print(f"Norma b: {norma_b}")
print(f"Vector c: {c}")
print(f"Norma c: {norma_c}")
print(f"Vector u: {u}")
print(f"Norma u: {norma_u}")
print(f"Vector v: {v}")
print(f"Norma v: {norma_v}")
print(f"Vector w: {w}")
print(f"Norma w: {norma_w}")

suma_ab= a+b
suma_ac= a+c
suma_bc= b+c
dif_ba= b-a
dif_ca= c-a
dif_bc= b-c

print(f"Suma ab: {suma_ab}")
print(f"Suma ac: {suma_ac}")
print(f"Suma bc: {suma_bc}")
print(f"Diferenta ba: {dif_bc}")
print(f"Diferenta ca: {dif_ca}")
print(f"Diferenta bc: {dif_bc}")

prodsc_ab=a@b
prodsc_ac=a@c
prodsc_bc=b@c
prodsc_uv=u@v
prodsc_uw=u@w
prodsc_vw=v@w

print(f"Prod scalar ab: {prodsc_ab}")
print(f"Prod scalar ac: {prodsc_ac}")
print(f"Prod scalar bc: {prodsc_bc}")
print(f"Prod scalar uv: {prodsc_uv}")
print(f"Prod scalar uw: {prodsc_uw}")
print(f"Prod scalar vw: {prodsc_vw}")

unghi_ab= prodsc_ab/(norma_a*norma_b)
unghi_ab_rad=np.degrees(unghi_ab)
print(f"Unghi ab: {unghi_ab_rad}")

unghi_ac= prodsc_ac/(norma_a*norma_c)
unghi_ac_rad=np.degrees(unghi_ac)
print(f"Unghi ac: {unghi_ac_rad}")

unghi_bc= prodsc_bc/(norma_b*norma_c)
unghi_bc_rad=np.degrees(unghi_bc)
print(f"Unghi bc: {unghi_bc_rad}")

unghi_uv= prodsc_uv/(norma_u*norma_v)
unghi_uv_rad=np.degrees(unghi_uv)
print(f"Unghi uv: {unghi_uv_rad}")

unghi_uw= prodsc_uw/(norma_u*norma_w)
unghi_uw_rad=np.degrees(unghi_uw)
print(f"Unghi uw: {unghi_uw_rad}")

unghi_vw= prodsc_vw/(norma_v*norma_w)
unghi_vw_rad=np.degrees(unghi_vw)
print(f"Unghi vw: {unghi_vw_rad}")

prodvect_uv=np.cross(u,v)
prodvect_uw=np.cross(u,w)
prodvect_vw=np.cross(v,w)
print(f"Prod vectorial uv: {prodvect_uv}")
print(f"Prod vectorial uw: {prodvect_uw}")
print(f"Prod vectorial vw: {prodvect_vw}")

norma_a_patrat=LA.norm(a)**2
norma_b_patrat=LA.norm(b)**2
norma_c_patrat=LA.norm(c)**2
norma_u_patrat=LA.norm(u)**2
norma_v_patrat=LA.norm(v)**2
norma_w_patrat=LA.norm(w)**2

scalar_ab=prodsc_ab/norma_b_patrat
scalar_ac=prodsc_ac/norma_c_patrat

scalar_ba =prodsc_ab/norma_a_patrat
scalar_bc=prodsc_bc/norma_c_patrat

scalar_ca =prodsc_ac/norma_a_patrat
scalar_cb=prodsc_bc/norma_b_patrat

scalar_uv=prodsc_uv/norma_v_patrat
scalar_uw=prodsc_uw/norma_w_patrat

scalar_vw=prodsc_vw/norma_w_patrat
scalar_vu=prodsc_uv/norma_u_patrat

scalar_wu =prodsc_uw/norma_u_patrat
scalar_wv =prodsc_vw/norma_v_patrat

proiectie_apeb=scalar_ab * b
proiectie_apec=scalar_ac * c

proiectie_bpea=scalar_ba * a
proiectie_bpec=scalar_bc * c

proiectie_cpea=scalar_ca * a
proiectie_cpeb=scalar_cb * b

proiectie_upev=scalar_uv * v
proiectie_upew=scalar_uw * w

proiectie_vpeu=scalar_vu * u
proiectie_vpew=scalar_vw * w

proiectie_wpeu=scalar_wu * u
proiectie_wpev=scalar_wv * v

print(f"Proiectia lui a pe b:{proiectie_apeb}")
print(f"Proiectia lui a pe c:{proiectie_apec}")

print(f"Proiectia lui b pe a:{proiectie_bpec}")
print(f"Proiectia lui b pe c:{proiectie_bpec}")

print(f"Proiectia lui c pe a:{proiectie_cpea}")
print(f"Proiectia lui c pe b:{proiectie_cpeb}")

print(f"Proiectia lui u pe v:{proiectie_upev}")
print(f"Proiectia lui u pe w:{proiectie_upew}")

print(f"Proiectia lui v pe u:{proiectie_vpeu}")
print(f"Proiectia lui v pe w:{proiectie_vpew}")

print(f"Proiectia lui w pe v:{proiectie_wpev}")
print(f"Proiectia lui w pe u:{proiectie_wpeu}")

def triunghi2D():

    P0 = np.array([0, 0])
    P1 = a
    P2 = b
    x = [P0[0], P1[0], P2[0], P0[0]]
    y = [P0[1], P1[1], P2[1], P0[1]]
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, 'ro-')
    plt.quiver(0, 0, a[0], a[1], angles='xy', scale_units='xy', scale=1)
    plt.quiver(0, 0, b[0], b[1], angles='xy', scale_units='xy', scale=1)
    plt.title("Triunghi")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def dreptunghi2D():

    P0 = np.array([0, 0])
    P1 = a
    P2 = a + b
    P3 = b
    x = [P0[0], P1[0], P2[0], P3[0], P0[0]]
    y = [P0[1], P1[1], P2[1], P3[1], P0[1]]
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, 'go-')
    plt.quiver(0, 0, a[0], a[1], angles='xy', scale_units='xy', scale=1)
    plt.quiver(0, 0, b[0], b[1], angles='xy', scale_units='xy', scale=1)
    plt.quiver(a[0], a[1], b[0], b[1], angles='xy', scale_units='xy', scale=1)
    plt.quiver(b[0], b[1], a[0], a[1], angles='xy', scale_units='xy', scale=1)
    plt.title("Dreptunghi")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def poligon2D():
    P0 = np.array([0, 0])
    P1 = a
    P2 = a + c
    P3 = a + b + c
    P4 = b + c
    P5 = b

    x = [P0[0], P1[0], P2[0], P3[0], P4[0], P5[0], P0[0]]
    y = [P0[1], P1[1], P2[1], P3[1], P4[1], P5[1], P0[1]]
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, 'bo-')
    plt.quiver(0, 0, a[0], a[1], angles='xy', scale_units='xy', scale=1)
    plt.quiver(a[0], a[1], c[0], c[1], angles='xy', scale_units='xy', scale=1)
    plt.quiver(a[0] + c[0], a[1] + c[1], b[0], b[1],angles='xy', scale_units='xy', scale=1)
    plt.quiver(b[0], b[1], c[0], c[1], angles='xy', scale_units='xy', scale=1)
    plt.title("Poligon")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()

def cub3D():

    o=np.array([0,0,0])
    pts = np.array([
        o,
        u,
        u+v,
        v,
        o+w,
        u+w,
        u+v+w,
        v+w
    ])
    edges = np.array([
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7),
    ])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i, j in edges:
        xs = [pts[i, 0], pts[j, 0]]
        ys = [pts[i, 1], pts[j, 1]]
        zs = [pts[i, 2], pts[j, 2]]
        ax.plot(xs, ys, zs, '-ro')
    ax.set_title("Cub")
    ax.set_box_aspect([1, 1, 1])
    plt.show()


def tetraedru3D():
    o = np.array([0, 0, 0])
    pts = np.array([
        o,
        u,
        v,
        w
    ])

    edges = np.array([
        (0, 1), (1, 2), (2, 0),
        (0, 3), (1, 3), (2, 3)
    ])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i, j in edges:
        xs = [pts[i, 0], pts[j, 0]]
        ys = [pts[i, 1], pts[j, 1]]
        zs = [pts[i, 2], pts[j, 2]]
        ax.plot(xs, ys, zs, '-go')
    ax.set_title("Tetraedru")
    ax.set_box_aspect([1, 1, 1])
    plt.show()


def prisma3D():
    o=np.array([0, 0, 0])
    pts = np.array([
       o,
       u,
       v,
       o+w,
       u+w,
       v+w
   ])
    edges = np.array([
        (0, 1), (1, 2), (2, 0),
        (3, 4), (4, 5), (5, 3),
        (0, 3), (1, 4), (2, 5)
    ])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i, j in edges:
        xs = [pts[i, 0], pts[j, 0]]
        ys = [pts[i, 1], pts[j, 1]]
        zs = [pts[i, 2], pts[j, 2]]
        ax.plot(xs, ys, zs, '-bo')
    ax.set_title("Prisma")
    ax.set_box_aspect([1, 1, 1])
    plt.show()

triunghi2D()
dreptunghi2D()
poligon2D()
cub3D()
tetraedru3D()
prisma3D()
