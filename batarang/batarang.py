"""Parametric "stuck in the wall" magnetic batarang.

A bevelled batarang with one wing sliced off at an angle. Two magnets sit in
the sliced face, so on a fridge or steel plate it looks like it was thrown
into the surface.

Usage:  python3 batarang.py [--span 127.5] [--thickness 10] [--magnet-d 6] [--magnet-h 2]
Outputs batarang.stl (lying flat, ready to print) and preview.png.
Requires: numpy scipy shapely trimesh manifold3d matplotlib
"""
import argparse
from pathlib import Path

import numpy as np
import shapely
import trimesh
from scipy.spatial import Delaunay
from shapely import affinity
from shapely.geometry import LineString, Polygon

p = argparse.ArgumentParser()
p.add_argument("--span", type=float, default=127.5, help="full wingtip-to-wingtip width before the cut, mm")
p.add_argument("--thickness", type=float, default=10, help="thickness at the centre, mm")
p.add_argument("--edge", type=float, default=1.2, help="thickness left at the bevelled edge, mm")
p.add_argument("--bevel", type=float, default=4.4, help="bevel width, mm")
p.add_argument("--magnet-d", type=float, default=6, help="magnet diameter, mm")
p.add_argument("--magnet-h", type=float, default=2, help="magnet height, mm")
p.add_argument("--clearance", type=float, default=0.2, help="added to pocket diameter and depth, mm")
p.add_argument("--magnet-spacing", type=float, default=8.5, help="centre-to-centre distance, mm")
p.add_argument("--cut-x", type=float, default=26, help="where the wall slices the right wing (at span 150), mm from centre")
p.add_argument("--cut-angle", type=float, default=30, help="in-plane lean of the batarang against the wall, deg")
p.add_argument("--cut-tilt", type=float, default=8, help="out-of-plane lean, deg")
a = p.parse_args()
T, E, B = a.thickness, a.edge, a.bevel

# ---- 2D outline (drawn at 150 mm span, then scaled) -------------------------
def bez(p0, c, p1, n=60):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * t * (1 - t) * np.array(c) + t ** 2 * np.array(p1)

half = np.vstack([
    [(0, 7), (3.2, 14)],                      # V notch, ear tip
    bez((6.5, 6.5), (30, -2), (75, 26)),      # deep concave top edge up to a high wing tip
    bez((75, 26), (52, 6), (33, -20)),        # crescent trailing edge down to the flank point
    bez((33, -20), (15, -2), (0, -32)),       # inner scallop to the long tail point
])
pts = np.vstack([half, (half * [-1, 1])[-2:0:-1]])
k = a.span / 150
outline = affinity.scale(Polygon(pts), k, k, origin=(0, 0))
outline = outline.buffer(-0.5, 32).buffer(0.5, 32)       # blunt the tips

# ---- bevelled solid: height field over the outline --------------------------
def ring_points(geom, step=0.4):
    out = []
    for g in getattr(geom, "geoms", [geom]):
        for r in [g.exterior, *g.interiors]:
            n = max(8, int(r.length / step))
            out += [r.interpolate(i / n, normalized=True).coords[0] for i in range(n)]
    return out

levels = 16
xy = []
for i in range(levels + 1):
    inset = outline.buffer(-B * i / levels, 16)
    if not inset.is_empty:
        xy += ring_points(inset)
minx, miny, maxx, maxy = outline.bounds
gx, gy = np.meshgrid(np.arange(minx, maxx, 1.5), np.arange(miny, maxy, 1.5))
grid = np.c_[gx.ravel(), gy.ravel()]
core = outline.buffer(-B - 0.5)
xy = np.vstack([xy, grid[shapely.contains_xy(core, grid[:, 0], grid[:, 1])]])

tri = Delaunay(xy).simplices
cen = xy[tri].mean(axis=1)
tri = tri[shapely.contains_xy(outline.buffer(1e-6), cen[:, 0], cen[:, 1])]

d = shapely.distance(outline.exterior, shapely.points(xy))
z = E / 2 + np.minimum(d, B) / B * (T - E) / 2
n = len(xy)
verts = np.vstack([np.c_[xy, z], np.c_[xy, -z]])
edges = np.sort(np.vstack([tri[:, [0, 1]], tri[:, [1, 2]], tri[:, [2, 0]]]), axis=1)
directed = np.vstack([tri[:, [0, 1]], tri[:, [1, 2]], tri[:, [2, 0]]])
_, inv, cnt = np.unique(edges, axis=0, return_inverse=True, return_counts=True)
rim = directed[cnt[inv.ravel()] == 1]
i, j = rim[:, 0], rim[:, 1]
faces = np.vstack([tri, tri[:, ::-1] + n, np.c_[i, i + n, j + n], np.c_[i, j + n, j]])
solid = trimesh.Trimesh(verts, faces, process=True)
assert solid.is_watertight, "bevelled blank is not watertight"
if solid.volume < 0:
    solid.invert()

# ---- slice one wing off where it "enters the wall" --------------------------
phi, tilt = np.radians(a.cut_angle), np.radians(a.cut_tilt)
normal = np.array([np.cos(phi) * np.cos(tilt), np.sin(phi) * np.cos(tilt), np.sin(tilt)])
along = np.array([-np.sin(phi), np.cos(phi), 0.0])       # direction along the cut face, in-plane
origin = np.array([a.cut_x * k, 0, 0])

box = trimesh.creation.box([400, 400, 400])
to_wall = trimesh.geometry.align_vectors([1, 0, 0], normal)
box.apply_translation([-200, 0, 0]); box.apply_transform(to_wall); box.apply_translation(origin)
blank = solid.intersection(box)

# centre the magnets on the full-thickness part of the cut face
line = LineString([origin[:2] - along[:2] * 200, origin[:2] + along[:2] * 200])
flat = line.intersection(outline.buffer(-B))
flat = max(getattr(flat, "geoms", [flat]), key=lambda g: g.length)
mid = np.array([*flat.centroid.coords[0], 0.0])
pocket_d, pocket_h = a.magnet_d + a.clearance, a.magnet_h + a.clearance
part = blank
for s in (1, -1):
    c = mid + s * along * a.magnet_spacing / 2
    c -= normal * (c - origin).dot(normal)                # drop onto the cut plane
    for r, h, check in ((pocket_d / 2 + 0.8, pocket_h + 0.6, True), (pocket_d / 2, pocket_h, False)):
        cyl = trimesh.creation.cylinder(radius=r, height=2 * h, sections=96)
        cyl.apply_transform(trimesh.geometry.align_vectors([0, 0, 1], normal))
        cyl.apply_translation(c)
        if check:   # pocket plus 0.8 mm wall must be buried in plastic
            buried = cyl.intersection(box)
            lost = buried.volume - buried.intersection(blank).volume
            assert lost < 0.5, f"magnet pocket breaks through the surface ({lost:.1f} mm3); raise --thickness or adjust --cut-x / --cut-angle"
        else:
            part = part.difference(cyl)

assert part.is_watertight
part.apply_translation([0, 0, T / 2])                    # lie flat on the bed
out = Path(__file__).parent
part.export(out / "batarang.stl")
x, y, zz = part.extents
print(f"batarang.stl: {x:.1f} x {y:.1f} x {zz:.1f} mm, volume {part.volume/1000:.1f} cm3")
print(f"cut face flat {flat.length:.1f} mm long; 2 pockets dia {pocket_d:.2f} x {pocket_h:.2f} deep, {a.magnet_spacing:g} mm apart")

# ---- preview ----------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def draw(ax, mesh, elev, azim, title):
    light = np.array([0.3, -0.5, 0.8]); light /= np.linalg.norm(light)
    shade = 0.25 + 0.6 * np.clip(mesh.face_normals @ light, 0, 1)
    ax.add_collection3d(Poly3DCollection(mesh.triangles, facecolors=np.c_[shade * .55, shade * .55, shade * .6], edgecolor="none"))
    lo, hi = mesh.bounds; c = (lo + hi) / 2; r = (hi - lo).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1), zoom=1.45); ax.view_init(elev, azim); ax.set_axis_off(); ax.set_title(title, fontsize=10)

fig = plt.figure(figsize=(13, 5), dpi=150)
draw(fig.add_subplot(131, projection="3d"), part, 89, -90, "as printed (top)")
draw(fig.add_subplot(132, projection="3d"), part, 30, -60, "bevels")
draw(fig.add_subplot(133, projection="3d"), part, 20, 10, "cut face with magnet pockets")
fig.subplots_adjust(0, 0, 1, 0.95, 0, 0)
fig.savefig(out / "preview.png")
