"""Brute-force check of the true shortest tour for the 10-city problem.

With 10 cities there are only 9!/2 = 181,440 distinct round trips, so every one
can be checked. Used to confirm how close GA and PSO get to the real optimum.
"""
import itertools
from math import sqrt

CITIES = [
    ("Kuala Lumpur", 101.6869, 3.1390), ("George Town", 100.3292, 5.4145),
    ("Johor Bahru", 103.7414, 1.4927), ("Ipoh", 101.0901, 4.5975),
    ("Kuching", 110.3549, 1.5397), ("Kota Kinabalu", 116.0735, 5.9804),
    ("Shah Alam", 101.5185, 3.0733), ("Malacca City", 102.2501, 2.1896),
    ("Alor Setar", 100.3697, 6.1216), ("Miri", 113.9914, 4.3995),
]
n = len(CITIES)
# Same distance as the notebook: straight-line degrees × 111 km
D = [[sqrt((CITIES[j][1] - CITIES[i][1]) ** 2 + (CITIES[j][2] - CITIES[i][2]) ** 2) * 111
      for j in range(n)] for i in range(n)]

best_dist, best_route = float("inf"), None
for perm in itertools.permutations(range(1, n)):
    if perm[0] > perm[-1]:          # skip mirror-image tours
        continue
    route = (0,) + perm + (0,)
    dist = sum(D[route[k]][route[k + 1]] for k in range(n))
    if dist < best_dist:
        best_dist, best_route = dist, route

print(f"Optimal tour length: {best_dist:.2f} km")
print(" -> ".join(CITIES[i][0] for i in best_route))
