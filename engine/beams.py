"""Euler-Bernoulli beam solver for girders and cantilevers (Prompt 3).

A girder is split into short elements. Each joint can move up/down (v) and rotate (theta).
Supports: "pin" stops v, "fixed" stops v and theta. We solve [K][U] = [F] again, then
recover the bending moment M(x) and shear force V(x) everywhere along the beam.

    bending stress   sigma = M * y / I        (y = distance from the middle of the section)
    shear stress     tau   = V * Q / (I * t)
    rectangle        I = b d^3 / 12,   Q_max = b d^2 / 8

Sign convention: loads w are DOWNWARD (N/m). Sagging moment (smile shape) is positive.
"""
from dataclasses import dataclass

import numpy as np


def rect_I(b, d):
    return b * d ** 3 / 12.0


def rect_Q_max(b, d):
    """First moment of area above the middle of a rectangle."""
    return b * d * d / 8.0


def bending_stress(M, I, y):
    """sigma = M y / I"""
    return M * y / I


def shear_stress(V, Q, I, t):
    """tau = V Q / (I t)"""
    return V * Q / (I * t)


def haunch_depth(x, x_pier, arm_length, d_pier, d_tip):
    """Variable-depth girder: deepest at the pier, tapering (parabola) to the tip."""
    r = min(abs(x - x_pier) / arm_length, 1.0) if arm_length > 0 else 1.0
    return d_tip + (d_pier - d_tip) * (1 - r) ** 2


@dataclass
class BeamResult:
    x: np.ndarray          # sample positions along the beam, m
    M: np.ndarray          # bending moment at x, N*m (sagging +)
    V: np.ndarray          # shear force at x, N
    deflection: np.ndarray # vertical displacement at the nodes, m (+ up)
    reactions: dict        # node -> (force N up, moment N*m ccw)
    elem_M: list           # (M_left, M_right) per element
    elem_V: list           # (V_left, V_right) per element


class BeamSolver:
    def __init__(self, xs, EI, supports):
        """xs: node positions (sorted). EI: one value per element (len(xs)-1).
        supports: {node_index: "pin" | "fixed"}"""
        self.xs = np.asarray(xs, dtype=float)
        self.EI = np.asarray(EI, dtype=float)
        if len(self.EI) != len(self.xs) - 1:
            raise ValueError("Need one EI per element")
        self.supports = dict(supports)

    def _k(self, e):
        L = self.xs[e + 1] - self.xs[e]
        c = self.EI[e] / L ** 3
        return c * np.array([
            [12, 6 * L, -12, 6 * L],
            [6 * L, 4 * L * L, -6 * L, 2 * L * L],
            [-12, -6 * L, 12, -6 * L],
            [6 * L, 2 * L * L, -6 * L, 4 * L * L],
        ])

    @staticmethod
    def _f_eq(w, L):
        """Equivalent joint loads for a uniform DOWNWARD load w over length L."""
        q = -w
        return np.array([q * L / 2, q * L * L / 12, q * L / 2, -q * L * L / 12])

    def solve(self, w=None, point_loads=None, samples_per_element=8):
        """w: per-element uniform downward load (N/m), list or scalar.
        point_loads: {node_index: downward force N}."""
        n = len(self.xs)
        ne = n - 1
        if w is None:
            w = np.zeros(ne)
        w = np.broadcast_to(np.asarray(w, dtype=float), (ne,))
        K = np.zeros((2 * n, 2 * n))
        F = np.zeros(2 * n)
        for e in range(ne):
            dofs = [2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3]
            K[np.ix_(dofs, dofs)] += self._k(e)
            F[dofs] += self._f_eq(w[e], self.xs[e + 1] - self.xs[e])
        for node, P in (point_loads or {}).items():
            F[2 * node] -= P
        fixed = []
        for node, kind in self.supports.items():
            fixed.append(2 * node)
            if kind == "fixed":
                fixed.append(2 * node + 1)
        free = [d for d in range(2 * n) if d not in set(fixed)]
        U = np.zeros(2 * n)
        K_ff = K[np.ix_(free, free)]
        if np.linalg.matrix_rank(K_ff) < len(free):
            raise ValueError("Beam is not supported enough to stand")
        U[free] = np.linalg.solve(K_ff, F[free])
        R = K @ U - F
        # Point loads applied straight onto a support go into that support's reaction.
        reactions = {node: (R[2 * node], R[2 * node + 1] if kind == "fixed" else 0.0)
                     for node, kind in self.supports.items()}

        xs_out, M_out, V_out, elem_M, elem_V = [], [], [], [], []
        for e in range(ne):
            L = self.xs[e + 1] - self.xs[e]
            dofs = [2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3]
            end = self._k(e) @ U[dofs] - self._f_eq(w[e], L)
            V1, M1 = end[0], end[1]
            M_left = -M1
            elem_M.append((M_left, M_left + V1 * L - w[e] * L * L / 2))
            elem_V.append((V1, V1 - w[e] * L))
            for k in range(samples_per_element + 1):
                if e > 0 and k == 0:
                    continue
                x = L * k / samples_per_element
                xs_out.append(self.xs[e] + x)
                M_out.append(M_left + V1 * x - w[e] * x * x / 2)
                V_out.append(V1 - w[e] * x)
        return BeamResult(np.array(xs_out), np.array(M_out), np.array(V_out),
                          U[0::2].copy(), reactions, elem_M, elem_V)
