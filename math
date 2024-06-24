import sympy as sp
r, h = sp.symbols('r h')
V = sp.Symbol('V')
volume_eq = sp.Eq(sp.pi * r**2 * h, V)
h_expr = sp.solve(volume_eq, h)[0]
surface_area = 2 * sp.pi * r**2 + 2 * sp.pi * r * h
surface_area_expr = surface_area.subs(h, h_expr)
derivative = sp.diff(surface_area_expr, r)
critical_points = sp.solve(derivative, r)
surface_area_expr, critical_points
