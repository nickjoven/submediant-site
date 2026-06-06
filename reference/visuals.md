# Visual Assets

Gallery of all visual and interactive resources across the framework, organized by type.

---

## Interactive HTML Applications

| Application | Description |
|---|---|
| [Stern-Brocot Walk](https://github.com/nickjoven/harmonics/blob/main/sync_cost/applications/stern_brocot_walk.html) | Navigate the Stern-Brocot tree interactively. Explore mediant construction, Farey neighbors, and the rational hierarchy. |
| [Ontology Viewer](https://github.com/nickjoven/harmonics/blob/main/sync_cost/applications/ontology.html) | Framework concept map. Visual index of how derivations, primitives, and predictions connect. |
| [Mobius Views](https://github.com/nickjoven/harmonics/blob/main/sync_cost/applications/mobius_views.html) | Mobius strip visualizations. The non-orientable topology underlying the two-root structure. |
| [Mobius Projector](https://github.com/nickjoven/harmonics/blob/main/sync_cost/applications/mobius_projector.html) | Projection tool for Mobius strip geometry. |
| [Our Address](https://nickjoven.github.io/submediant-site/our_address.html) | The universe's computational clock. Stern-Brocot coordinates, progress, and predictions. |
| [Intersections](https://nickjoven.github.io/intersections/) | Stick-slip dynamics with interactive Plotly and Canvas visualizations. Lagrangian relaxation, Stribeck curves, and bifurcation thresholds. |
| [Stribeck Optics](https://nickjoven.github.io/stribeck-optics/) | Optical friction visualization. Stribeck curve mapped to refractive phenomena. |
| [First Principles](https://nickjoven.github.io/submediant-site/first-principles.html) | sin(ωt) to Einstein. The complete derivation in 10 steps, with an evolving waveform background. |
| [Oscillations](https://nickjoven.github.io/submediant-site/oscillations.html) | 47 oscillations of f(x) = 1/(1+x). Pipes screensaver, Fibonacci sequence, pure math of 1/φ. |
| [Derivation Graph](graph) | Interactive D3 force-directed graph of the framework's derivation chain and repository structure. |
| [Double Pendulum](https://github.com/nickjoven/harmonics/blob/main/sync_cost/applications/double_pendulum.html) | Double pendulum tongue structure. Mode-locking visible in phase portraits of the driven coupled pendulum. |
| [Three-Body Catalog](https://github.com/nickjoven/harmonics/blob/main/sync_cost/applications/three_body_catalog.html) | Catalog of three-body periodic orbits — the classical counterpart to three coupled oscillators. |
| [Zone Plate](https://nickjoven.github.io/submediant-site/zone-plate.html) | Feynman path-sum demonstration. Block the specular point with an obstruction, apply a diffractive film, watch the light return via non-specular paths. |

---

## Animations

| File | Description |
|---|---|
| [stairs.gif](https://github.com/nickjoven/harmonics/blob/main/stairs.gif) | Devil's staircase construction. Tongues filling the frequency axis as coupling increases. |
| [triangles.gif](https://github.com/nickjoven/harmonics/blob/main/triangles.gif) | Stern-Brocot tree triangulation. Mediant insertion building the rational hierarchy. |
| [orbit.gif](https://github.com/nickjoven/harmonics/blob/main/orbit.gif) | Circle map orbit. Phase evolution showing mode-locking and quasiperiodicity. |
| [spiral.gif](https://github.com/nickjoven/harmonics/blob/main/spiral.gif) | Spiral convergence. Floquet decay inside an Arnold tongue. |
| [rose.gif](https://github.com/nickjoven/harmonics/blob/main/rose.gif) | Rose curve from rational frequency ratios. Winding number geometry on the circle. |
| [genesis.gif](https://github.com/nickjoven/harmonics/blob/main/genesis.gif) | Genesis animation — primordial structure emerging from the tree. |

---

## Diagrams

| File | Description |
|---|---|
| [minimum_self_predicting_universe.svg](https://github.com/nickjoven/harmonics/blob/main/sync_cost/minimum_self_predicting_universe.svg) | The minimum self-predicting universe. Schematic of the four-primitive alphabet and its compositions. |
| [staircase_forming.svg](https://github.com/nickjoven/harmonics/blob/main/sync_cost/staircase_forming.svg) | Staircase formation. How Arnold tongues fill the frequency axis at increasing coupling. |

---

## Phase Portraits and Plots

### Proslambenomenos

Phase portraits from the original Kuramoto-Einstein mapping.

| File | Description |
|---|---|
| [phase_newtonian.png](https://github.com/nickjoven/proslambenomenos/blob/main/docs/img/phase_newtonian.png) | Phase portrait: Newtonian regime ($g \gg a_0$). Decoupled orbits. |
| [phase_deep_mond.png](https://github.com/nickjoven/proslambenomenos/blob/main/docs/img/phase_deep_mond.png) | Phase portrait: MOND regime ($g \ll a_0$). Entrained orbits. |
| [phase_boundary.png](https://github.com/nickjoven/proslambenomenos/blob/main/docs/img/phase_boundary.png) | Phase portrait: transition regime ($g \approx a_0$). The synchronization boundary. |

### Harmonics Derivation Plots

Computational outputs from the derivation scripts.

| Script source | Content |
|---|---|
| `circle_map.py` | Arnold tongues, devil's staircase at varying $K$ |
| `golden_ratio_pivot.py` | Zoom into $1/\varphi$, identifying the pivot scale |
| `phi_squared_zoom.py` | Exact $\varphi^2$ self-similarity at the golden ratio |
| `k_omega_mapping.py` | The $k \leftrightarrow \Omega$ mapping: spectral tilt rate and amplitude |
| `staircase_geometry.py` | 3D representations: Arnold surface, Poincare disk, curvature |
| `born_rule_tongues.py` | Tongue boundary geometry confirming $\Delta\theta \propto \sqrt{\varepsilon}$ |
| `collapse_tongues.py` | Floquet convergence rate and collapse duration |
| `fidelity_calibration.py` | RAR interpolating function from tongue self-consistency |
| `a0_high_z.py` | High-redshift $a_0(z)$ predictions and observational comparison |

All scripts are in the [harmonics/sync_cost/derivations](https://github.com/nickjoven/harmonics/tree/main/sync_cost/derivations) directory.
