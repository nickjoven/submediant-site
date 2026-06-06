# Coherence

The framework's dynamics do not wander. Wherever the recurrence acts it
resolves onto a structure that preserves *something* — a settling point, a
quantity carried across a jump, a closed set, a return, a bounded support, a
universal fork. These are six ways the apparatus stays coherent: six places
the dynamics terminate. Each is backed by a derivation in
[harmonics](https://github.com/nickjoven/harmonics).

## Halt — dynamics terminate at fixed points

The flow settles; the settling point is the result.

| Settles on | Source |
|---|---|
| Born rule — attractor convergence under dissipative gradient flow | [born_rule.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/born_rule.md) |
| $K_\ast$ — fixed point under the generation law ($K_\ast^{14} = q_2^{-q_3} = 1/8$) | [CHAIN_KSTAR.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/CHAIN_KSTAR.md) |
| Boundary weight $w_\ast \approx 0.83$ — self-consistent fixed point at $q = 6$ | [boundary_weight.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/boundary_weight.md) |
| Natural irrationals $\{\varphi, \pi, e, \sqrt{n}\}$ — substrate-recursion settle points (inviolable #8) | [bicone_golden_z2_identification.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/bicone_golden_z2_identification.md) |

## Shock — discontinuities propagate while conserving a quantity across the jump

The transition is not smooth, but something crosses it intact.

| Jump | Conserved / mechanism | Source |
|---|---|---|
| A non-local process flips $Q \bmod 2$ | $Q \bmod 2$ is conserved under every *local* process; to change it a process must encircle the antiperiodic direction (hence non-local) | [q_mod2_conservation_theorem.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/q_mod2_conservation_theorem.md) |
| Hubble-boundary mode truncation: $14 \to 12.66$ at $w_\ast \approx 0.83$ | cardinality carried across the jump | [boundary_weight.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/boundary_weight.md) |
| $K = 1 \leftrightarrow K < 1$: tongue coverage jumps $0.138 \to 1.0$ at $K = 1$ | a genuine discontinuity. **Note:** this is recorded as a *null* — $w_\ast$ is **not** derivable from tongue coverage; it is fixed by the C5 closure (so cite the jump, not a $w_\ast$ derivation) | [continuity_in_K_nulls.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/continuity_in_K_nulls.md) (N11) |
| Measurement projection: lossless $\to$ lossy | resolution carried across the jump | [measurement_collapse.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/measurement_collapse.md) |

## Closure — operations close on their structural sets

The operation never leaves the set it acts on.

| Closes | Source |
|---|---|
| Mediant $(a+c)/(b+d)$ stays in the rationals; integers under arithmetic | [mediant_derivation.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/mediant_derivation.md) |
| Mihailescu: $q_2^2 - 1 = q_3$ and $q_3^2 - 1 = q_2^3$ (i.e. $4 - 1 = 3$, $9 - 1 = 8$) — an algebraic closure | [observer_register_closure.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/observer_register_closure.md) |
| Natural-irrationals closure (inviolable #8) | [bicone_golden_z2_identification.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/bicone_golden_z2_identification.md) |

## Recurrence — cyclic structure returns

Traverse far enough and you come back.

| Returns | Source |
|---|---|
| $K^2$ antiperiodic identification — closes after two $L_x$ traversals | [q_mod2_conservation_theorem.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/q_mod2_conservation_theorem.md) |
| Farey symmetry $r \to 1 - r$ | [imf_bowed_cascade.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/imf_bowed_cascade.md) |
| Stern–Brocot self-duality $x \to 1/x$ | [CHAIN_KSTAR.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/CHAIN_KSTAR.md) |

## Locality — changes propagate within bounded support

Nothing acts beyond its reach.

| Bound | Source |
|---|---|
| Diameter condition: support $< L_x$ | [q_mod2_conservation_theorem.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/q_mod2_conservation_theorem.md) |
| Speed-of-light bound (slow-regime binding) | [speed_of_light.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/speed_of_light.md) |
| Context window $L_x$ in the tick-continuum construction | [tick_continuum_construction.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/tick_continuum_construction.md) |

## Bifurcation — saddle-node universality at decisions

Every fork has the same shape near the branch point.

| Fork | Source |
|---|---|
| Born rule exponent $2$ from the $x^2 + \mu = 0$ normal form | [born_rule.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/born_rule.md) |
| Stribeck threshold crossover at $N = 3$ ($P(\omega_0)/P(\omega_d) \approx 1.03$; requires variable coupling) | [planck_scale.md](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/planck_scale.md), [planck_threshold.py](https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/planck_threshold.py) |

---

*Citations resolve into [harmonics/sync_cost/derivations](https://github.com/nickjoven/harmonics/tree/main/sync_cost/derivations). Quantitative values track [MANIFEST.yml](https://github.com/nickjoven/harmonics/blob/main/MANIFEST.yml); see [Declined Identities](declined.html) for bare $K = 1$ values the framework does not predict at $M_Z$.*
