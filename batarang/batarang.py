"""Parametric 3D-printable batarang with two magnet pockets.

Usage:  python3 batarang.py [--span 150] [--thickness 4] [--magnet-d 6] [--magnet-h 2]
Outputs batarang.stl and preview.png next to this script.
Requires: shapely trimesh manifold3d mapbox-earcut numpy matplotlib
"""
import argparse
from pathlib import Path

import trimesh
from shapely import affinity
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

p = argparse.ArgumentParser()
p.add_argument("--span", type=float, default=150, help="wingtip-to-wingtip width, mm")
p.add_argument("--thickness", type=float, default=4, help="blade thickness, mm")
p.add_argument("--magnet-d", type=float, default=6, help="magnet diameter, mm")
p.add_argument("--magnet-h", type=float, default=2, help="magnet height, mm")
p.add_argument("--clearance", type=float, default=0.2, help="added to pocket diameter and depth, mm")
p.add_argument("--magnet-spacing", type=float, default=40, help="centre-to-centre distance, mm (at span 150)")
a = p.parse_args()

# ---- 2D outline, drawn at 150 mm span then scaled ---------------------------
def circle(x, y, r):
    return Point(x, y).buffer(r, 128)

body = affinity.scale(circle(0, 0, 1), 75, 28)           # wing ellipse
cuts, ears = [], []
for s in (1, -1):
    cuts += [circle(s * 38, 40, 30),                      # concave top edge
             circle(s * 20, -34, 20),                     # inner bottom scallop
             circle(s * 55, -30, 17)]                     # outer bottom scallop
    ears.append(Polygon([(s * 2.5, 18), (s * 14, 18), (s * 9.5, 37)]))
outline = unary_union([body.difference(unary_union(cuts))] + ears)
outline = outline.buffer(1.5, 32).buffer(-1.5, 32)       # fillet inside corners
outline = outline.buffer(-0.8, 32).buffer(0.8, 32)       # blunt every tip (r = 0.8 mm)

k = a.span / 150
outline = affinity.scale(outline, k, k, origin=(0, 0))

# ---- 3D ---------------------------------------------------------------------
solid = trimesh.creation.extrude_polygon(outline, a.thickness)

pocket_d = a.magnet_d + a.clearance
pocket_h = a.magnet_h + a.clearance
floor = a.thickness - pocket_h
assert floor >= 0.8, f"only {floor:.2f} mm left above the magnet; raise --thickness"

mx = a.magnet_spacing / 2 * k
for s in (1, -1):
    c = Point(s * mx, 1 * k)
    assert outline.contains(c.buffer(pocket_d / 2 + 1.5)), "magnet pocket too close to the edge"
    cyl = trimesh.creation.cylinder(radius=pocket_d / 2, height=pocket_h + 1, sections=96)
    cyl.apply_translation([c.x, c.y, pocket_h - (pocket_h + 1) / 2])  # opens on z=0 face
    solid = solid.difference(cyl)

assert solid.is_watertight
out = Path(__file__).parent
solid.export(out / "batarang.stl")
x, y, z = solid.extents
print(f"batarang.stl: {x:.1f} x {y:.1f} x {z:.1f} mm, volume {solid.volume/1000:.1f} cm3")
print(f"pockets: 2 x dia {pocket_d:.2f} x {pocket_h:.2f} deep, {2*mx:.1f} mm apart, {floor:.2f} mm cover")

# ---- preview ----------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 4.5), dpi=150)
ax.fill(*outline.exterior.xy, color="#1b1b1f")
for s in (1, -1):
    ax.add_patch(plt.Circle((s * mx, k), pocket_d / 2, color="#c9ced6"))
ax.annotate("", (-a.span / 2, -34 * k), (a.span / 2, -34 * k), arrowprops=dict(arrowstyle="<->"))
ax.text(0, -38 * k, f"{x:.0f} mm", ha="center", va="top")
ax.text(0, -9 * k, f"2 x magnet pocket  dia {pocket_d:g} x {pocket_h:g} mm (back face)",
        ha="center", color="w", fontsize=8)
ax.set_aspect("equal"); ax.axis("off")
fig.savefig(out / "preview.png", bbox_inches="tight")
