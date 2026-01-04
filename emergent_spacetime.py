#!/usr/bin/env python3
"""
Emergent_Spacetime
==================

A conceptual toy-universe simulation exploring how time, distance,
light-cone structure, and curvature-like effects can emerge from
causal relationships alone, without assuming spacetime as a
fundamental entity.

This project is intended as an exploratory and educational model
for studying emergent spacetime and gravity-like behavior.

Author: Hrishikesh Jha
License: MIT
"""

import random
from collections import defaultdict, deque
import statistics

import networkx as nx
import matplotlib.pyplot as plt


class CausalUniverse:
    """
    Interactive toy universe based on causality.

    The universe is constructed from discrete events connected
    through causal influence. Time, distance, and geometry are
    emergent properties derived from this causal structure.
    """

    def __init__(self, base_causes=1, energy_strength=1.0):
        self.graph = defaultdict(list)
        self.events = []
        self.energy = {}
        self.base_causes = base_causes
        self.energy_strength = energy_strength

        # Primordial event (Big-Bang analogue)
        self.create_event(energy=1.0)

    def create_event(self, energy=1.0):
        eid = len(self.events)
        self.events.append(eid)
        self.energy[eid] = energy
        return eid

    def local_density(self, event):
        return len(self.graph[event])

    def update(self):
        if random.random() < 0.6:
            # Default low-energy event
            new_energy = 1.0

            # Occasional high-energy (mass-like) event
            if random.random() < 0.1:
                new_energy = random.choice(
                    [2, 5, 10]
                ) * self.energy_strength

            new_event = self.create_event(new_energy)
            older_events = self.events[:-1]

            if older_events:
                weights = [
                    (1 + self.local_density(e)) * self.energy[e]
                    for e in older_events
                ]

                num_causes = min(
                    self.base_causes + int(statistics.mean(weights)),
                    len(older_events)
                )

                causes = random.choices(
                    older_events,
                    weights=weights,
                    k=num_causes
                )

                for c in set(causes):
                    self.graph[c].append(new_event)

    def run(self, steps):
        for _ in range(steps):
            self.update()

    def causal_distance(self, start, end):
        visited = set()
        queue = deque([(start, 0)])

        while queue:
            node, dist = queue.popleft()
            if node == end:
                return dist
            if node in visited:
                continue
            visited.add(node)
            for nxt in self.graph[node]:
                queue.append((nxt, dist + 1))
        return None

    def light_cone(self, origin, depth):
        reachable = set()
        queue = deque([(origin, 0)])

        while queue:
            node, d = queue.popleft()
            if d > depth:
                continue
            reachable.add(node)
            for nxt in self.graph[node]:
                queue.append((nxt, d + 1))
        return reachable


# ---------------- VISUALIZATION ----------------

def build_graph(universe):
    G = nx.DiGraph()
    for src, targets in universe.graph.items():
        for tgt in targets:
            G.add_edge(src, tgt)
    return G


def causal_layout(universe, origin):
    layers = {}
    for e in universe.events:
        d = universe.causal_distance(origin, e)
        layers[e] = d if d is not None else len(universe.events)

    pos = {}
    layer_count = {}
    for e, l in layers.items():
        layer_count.setdefault(l, 0)
        pos[e] = (l, -layer_count[l])
        layer_count[l] += 1
    return pos


def show_universe(universe, mode):
    G = build_graph(universe)

    if mode == "graph":
        pos = causal_layout(universe, 0)
        plt.figure(figsize=(12, 6))
        nx.draw(G, pos, with_labels=True, node_size=500, arrows=True)
        plt.title("Causal Structure")
        plt.axis("off")

    elif mode == "curvature":
        densities = {e: universe.local_density(e) for e in universe.events}
        dense = max(densities, key=densities.get)
        sparse = min(densities, key=densities.get)

        pos = causal_layout(universe, dense)

        dense_cone = universe.light_cone(dense, 6)
        sparse_cone = universe.light_cone(sparse, 6)

        colors = []
        for n in G.nodes():
            if n == dense:
                colors.append("red")
            elif n == sparse:
                colors.append("blue")
            elif n in dense_cone:
                colors.append("orange")
            elif n in sparse_cone:
                colors.append("cyan")
            else:
                colors.append("lightgray")

        plt.figure(figsize=(14, 7))
        nx.draw(G, pos, node_color=colors,
                node_size=600, with_labels=True, arrows=True)
        plt.title("Curved Causal Cones")
        plt.axis("off")

    elif mode == "energy":
        massive = max(universe.energy, key=universe.energy.get)
        pos = causal_layout(universe, massive)
        cone = universe.light_cone(massive, 6)

        colors = []
        sizes = []
        for n in G.nodes():
            if n == massive:
                colors.append("darkred")
                sizes.append(1000)
            elif n in cone:
                colors.append("orange")
                sizes.append(600)
            else:
                colors.append("lightgray")
                sizes.append(400)

        plt.figure(figsize=(14, 7))
        nx.draw(G, pos, node_color=colors,
                node_size=sizes, with_labels=True, arrows=True)
        plt.title("Energy Source (Mass) Curving Causality")
        plt.axis("off")

    plt.show()


# ---------------- USER INTERFACE ----------------

if __name__ == "__main__":

    print("\n--- CAUSAL TOY UNIVERSE ---\n")

    steps = int(input("Number of time steps (e.g. 100): "))
    c_speed = int(input("Base causal speed (1–5): "))
    gravity = float(input("Energy (gravity) strength (e.g. 1.0): "))

    print("\nVisualization options:")
    print("1 → Causal graph")
    print("2 → Curved causal cones")
    print("3 → Energy (mass) curvature")

    choice = input("Choose visualization (1/2/3): ")

    universe = CausalUniverse(
        base_causes=c_speed,
        energy_strength=gravity
    )
    universe.run(steps)

    if choice == "1":
        show_universe(universe, "graph")
    elif choice == "2":
        show_universe(universe, "curvature")
    elif choice == "3":
        show_universe(universe, "energy")
    else:
        print("Invalid choice.")
