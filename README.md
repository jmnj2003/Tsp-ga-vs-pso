# Travelling Salesman Problem: Genetic Algorithm vs Particle Swarm Optimization

Finding the shortest round trip through **10 Malaysian cities** with two nature-inspired optimizers: a **Genetic Algorithm (GA)** and a **discrete Particle Swarm Optimization (PSO)**. Both are written from scratch in Python and compared over 5 runs on route length, convergence speed and consistency.

**Result:** the GA found the **true optimal route (3,984.61 km)** in 3 of 5 runs, which I confirmed by brute force. PSO ran about 5× faster but was less reliable.
---

## Problem

Visit every city exactly once and return to the start, using the shortest total distance.

| # | City | Longitude | Latitude |
|---|---|---|---|
| 1 | Kuala Lumpur | 101.6869 | 3.1390 |
| 2 | George Town | 100.3292 | 5.4145 |
| 3 | Johor Bahru | 103.7414 | 1.4927 |
| 4 | Ipoh | 101.0901 | 4.5975 |
| 5 | Kuching | 110.3549 | 1.5397 |
| 6 | Kota Kinabalu | 116.0735 | 5.9804 |
| 7 | Shah Alam | 101.5185 | 3.0733 |
| 8 | Malacca City | 102.2501 | 2.1896 |
| 9 | Alor Setar | 100.3697 | 6.1216 |
| 10 | Miri | 113.9914 | 4.3995 |

Distance is the straight-line distance between coordinates, using 1° ≈ 111 km.

## Algorithms

### Genetic Algorithm

| Component | Choice |
|---|---|
| Encoding | Permutation of city indices (closed loop) |
| Selection | Tournament (k = 3) |
| Crossover | Ordered crossover (OX), which keeps every route valid |
| Mutation | Swap two cities, rate 0.1 |
| Elitism | The best route always survives to the next generation |
| Settings | Population 100, up to 500 generations |

### Discrete PSO for permutations

Standard PSO moves particles through continuous space, but a TSP route is an ordering of cities. In this version:

- A particle's **position** is a route.
- Its **velocity** is a list of **swap operations**.
- **Inertia** keeps part of the previous swaps (w = 0.7).
- **Personal best (c1 = 1.5)** and **global best (c2 = 1.5)** add swaps that move the route towards those routes.
- Velocity is capped at 10 swaps per step. A repair step makes sure every city is still visited exactly once.
- Settings: swarm of 50 particles, up to 300 iterations.

## Results (5 runs each)

| | GA | PSO |
|---|---|---|
| **Best route** | **3,984.61 km** ✅ optimal | 3,988.60 km (2nd-best possible) |
| Worst route | **4,055.62 km** | 4,102.63 km |
| Mean | **3,999.61 km** | 4,060.21 km |
| Std. deviation | **28.05 km** | 39.62 km |
| Runs that found the optimum | **3 / 5** | 0 / 5 |
| Mean iterations to last improvement | 293 | **171** |
| Time per run | about 5–6 s | **about 1.2 s** |

### Checking against the true optimum

With 10 cities there are only 181,440 distinct tours, so [`verify_optimal.py`](verify_optimal.py) checks all of them:

```
Optimal tour length: 3984.61 km
Kuala Lumpur → Shah Alam → Ipoh → George Town → Alor Setar → Kota Kinabalu
→ Miri → Kuching → Johor Bahru → Malacca City → Kuala Lumpur
```

The GA's best route **is** the global optimum. PSO's best (3,988.60 km) is the **second-shortest tour possible**, only 4 km longer.

### What the results show

- **GA gives better and more consistent routes.** Ordered crossover and elitism keep good sub-routes (such as the West Coast chain from Alor Setar to Johor Bahru) and build on them.
- **PSO converges faster but settles early.** Swap-based velocities pull every particle towards the same global best, so the swarm loses variety and often gets stuck at about 4,060 km.
- **The trade-off:** use GA when route quality and repeatability matter most, and PSO when speed matters more.

**Caveats for a fair comparison:**

- The GA uses more fitness evaluations per run (100 × 500) than PSO (50 × 300), which partly explains both its better routes and its longer run time.
- "Iterations" here means the iteration of the last improvement of at least 1 km.
- Five runs is a small sample.

## Getting started

```bash
git clone https://github.com/jmnj2003/tsp-ga-vs-pso.git
cd tsp-ga-vs-pso
pip install -r requirements.txt
jupyter notebook tsp_ga_vs_pso.ipynb   # run GA + PSO and the 5-run comparison
python verify_optimal.py               # brute-force check of the true optimum
```

## Project structure

```
├── tsp_ga_vs_pso.ipynb   # GA, PSO, 5-run comparison, plots
├── verify_optimal.py     # brute-force check of the optimal tour
└── requirements.txt
```
