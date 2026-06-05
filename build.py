#!/usr/bin/env python3
"""Build the submediant site from the harmonics repository.

Fetches derivation markdown, computational notebooks, and data from
harmonics, arranges them into a Jupyter Book structure, and builds
an executable HTML site.

Usage:
    python build.py                  # fetch from GitHub + build
    python build.py --local ../      # use local sibling repos + build
    python build.py --fetch-only     # fetch sources, skip jb build
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

try:
    import yaml
except ImportError:
    yaml = None

SITE_DIR = Path(__file__).parent
BOOK_DIR = SITE_DIR / "book"

# The reverse structure: polynomial first, evidence last
SECTIONS = {
    "00_narrative": {
        "title": "The Story",
        "files": [],
        "local": ["partial_agreement.md"],
    },
    "01_alphabet": {
        "title": "The Alphabet",
        "files": [
            ("harmonics", "sync_cost/derivations/minimum_alphabet.md"),
            ("harmonics", "sync_cost/derivations/mediant_derivation.md"),
            ("harmonics", "sync_cost/derivations/lie_group_characterization.md"),
            ("harmonics", "sync_cost/derivations/three_dimensions.md"),
            ("harmonics", "sync_cost/derivations/address_and_quantity.md"),
        ],
    },
    "02_field_equation": {
        "title": "The Field Equation",
        "files": [
            ("harmonics", "sync_cost/derivations/rational_field_equation.md"),
            ("harmonics", "sync_cost/derivations/variable_denominator.md"),
            ("harmonics", "sync_cost/derivations/rank1_temporal_causation.md"),
        ],
    },
    "03_einstein": {
        "title": "K = 1: Einstein",
        "files": [
            ("harmonics", "sync_cost/derivations/einstein_from_kuramoto.md"),
            ("harmonics", "sync_cost/derivations/continuum_limits.md"),
            ("harmonics", "sync_cost/derivations/adm_dictionary.md"),
            ("harmonics", "sync_cost/derivations/gap1_analytic_proof.md"),
            ("harmonics", "sync_cost/derivations/gap2_analytic_proof.md"),
        ],
    },
    "04_schrodinger": {
        "title": "K < 1: Schrödinger",
        "files": [
            ("harmonics", "sync_cost/derivations/two_forces.md"),
        ],
        "generated": ["04_schrodinger_intro.md"],
    },
    "04a_topology": {
        "title": "Topology",
        "files": [
            ("harmonics", "sync_cost/derivations/mobius_container.md"),
            ("harmonics", "sync_cost/derivations/klein_bottle.md"),
            ("harmonics", "sync_cost/derivations/xor_continuum_limit.md"),
            ("harmonics", "sync_cost/derivations/discrete_gauge.md"),
            ("harmonics", "sync_cost/derivations/half_mobius_boundary.md"),
            ("harmonics", "sync_cost/derivations/engineering_targets.md"),
            ("harmonics", "sync_cost/derivations/three_zeros.md"),
            ("harmonics", "sync_cost/derivations/klein_bottle_derivation.md"),
            ("harmonics", "sync_cost/derivations/half_twist_dynamics.md"),
        ],
    },
    "04b_cosmology": {
        "title": "Cosmological Parameters",
        "files": [
            ("harmonics", "sync_cost/derivations/vacuum_energy.md"),
            ("harmonics", "sync_cost/derivations/farey_partition.md"),
            ("harmonics", "sync_cost/derivations/hierarchy.md"),
            ("harmonics", "sync_cost/derivations/exponent.md"),
            ("harmonics", "sync_cost/derivations/farey_proof.md"),
            ("harmonics", "sync_cost/derivations/baryon_fraction.md"),
        ],
    },
    "05_predictions": {
        "title": "Predictions",
        "files": [
            ("harmonics", "sync_cost/derivations/born_rule.md"),
            ("harmonics", "sync_cost/derivations/spectral_tilt.md"),
            ("harmonics", "sync_cost/derivations/spectral_tilt_reframed.md"),
            ("harmonics", "sync_cost/derivations/high_z_mond.md"),
            ("harmonics", "sync_cost/derivations/fidelity_bound.md"),
        ],
    },
    "04c_extended": {
        "title": "Extended Derivations",
        "files": [
            ("harmonics", "sync_cost/derivations/denomination_boundary.md"),
            ("harmonics", "sync_cost/derivations/speed_of_light.md"),
            ("harmonics", "sync_cost/derivations/minkowski_signature.md"),
            ("harmonics", "sync_cost/derivations/duty_cycle_dictionary.md"),
            ("harmonics", "sync_cost/derivations/generation_mechanism.md"),
            ("harmonics", "sync_cost/derivations/cosmological_cycle.md"),
            ("harmonics", "sync_cost/derivations/conservation_computability.md"),
            ("harmonics", "sync_cost/derivations/figure_eight.md"),
            ("harmonics", "sync_cost/derivations/boundary_weight.md"),
            ("harmonics", "sync_cost/derivations/stribeck_vortex.md"),
            ("harmonics", "sync_cost/derivations/duty_dimension_proof.md"),
            ("harmonics", "sync_cost/derivations/isotropy_lemma.md"),
            ("harmonics", "sync_cost/derivations/xor_derivation.md"),
            ("harmonics", "sync_cost/derivations/CHAIN_KSTAR.md"),
        ],
    },
    "04d_gauge": {
        "title": "Gauge Sector",
        "files": [
            ("harmonics", "sync_cost/derivations/discrete_gauge_resolution.md"),
            ("harmonics", "sync_cost/derivations/gauge_sector_lovelock.md"),
            ("harmonics", "sync_cost/derivations/gell_mann_nishijima.md"),
            ("harmonics", "sync_cost/derivations/higgs_from_tongue_boundary.md"),
            ("harmonics", "sync_cost/derivations/coupling_scales.md"),
            ("harmonics", "sync_cost/derivations/higgs_reframing.md"),
            ("harmonics", "sync_cost/derivations/mass_sector_closure.md"),
            ("harmonics", "sync_cost/derivations/a1_from_saddle_node.md"),
            ("harmonics", "sync_cost/derivations/item12_C_from_K_star.md"),
            ("harmonics", "sync_cost/derivations/item12_cross_sector_ratios.md"),
            ("harmonics", "sync_cost/derivations/sector_constants_structure.md"),
        ],
    },
    "06_evidence": {
        "title": "Evidence",
        "files": [
            ("harmonics", "RESULTS.md"),
            ("harmonics", "sync_cost/FRAMEWORK.md"),
            ("harmonics", "sync_cost/derivations/a0_threshold.md"),
            ("harmonics", "sync_cost/derivations/planck_scale.md"),
            ("harmonics", "sync_cost/derivations/measurement_collapse.md"),
            ("harmonics", "sync_cost/derivations/PROOF_A_gravity.md"),
            ("harmonics", "sync_cost/derivations/PROOF_B_quantum.md"),
            ("harmonics", "sync_cost/derivations/FRAMEWORK_TOPOLOGY.md"),
        ],
    },
    "07_prior_work": {
        "title": "Prior Work",
        "files": [
            ("proslambenomenos", "proslambenomenos.md"),
            ("201", "joven_unifying_framework.md"),
            ("intersections", "joven_stick_slip_dark_matter.md"),
        ],
    },
}

REPOS = {
    "harmonics": "nickjoven/harmonics",
    "proslambenomenos": "nickjoven/proslambenomenos",
    "201": "nickjoven/201",
    "intersections": "nickjoven/intersections",
    "stribeck-optics": "nickjoven/stribeck-optics",
    "product": "nickjoven/product",
}

# Python scripts fetched alongside derivations (needed for link resolution)
SCRIPT_FILES = {
    "harmonics": [
        "sync_cost/derivations/circle_map.py",
        "sync_cost/derivations/born_rule_tongues.py",
        "sync_cost/derivations/golden_ratio_pivot.py",
        "sync_cost/derivations/stern_brocot_map.py",
        "sync_cost/derivations/phi_squared_zoom.py",
        "sync_cost/derivations/k_omega_mapping.py",
        "sync_cost/derivations/field_equation_cmb.py",
        "sync_cost/derivations/klein_bottle_kuramoto.py",
        "sync_cost/derivations/alphabet_check.py",
        "sync_cost/derivations/sigma_squared.py",
        "sync_cost/derivations/alphabet_depth21.py",
    ],
}

# Extra data files (images, datasets)
DATA_FILES = {
    "proslambenomenos": [
        "docs/img/phase_newtonian.png",
        "docs/img/phase_boundary.png",
        "docs/img/phase_deep_mond.png",
        "docs/img/ngc2403_score.png",
        "docs/img/oa_potential.png",
    ],
}

# Static assets (HTML visualizations, GIFs, images) copied to book/_static/
# These are NOT Jupyter Book chapters — they are standalone files served as-is.
STATIC_ASSETS = {
    "harmonics": [
        # HTML visualizations
        "sync_cost/applications/stern_brocot_walk.html",
        "sync_cost/applications/ontology.html",
        "sync_cost/applications/mobius_views.html",
        "sync_cost/applications/mobius_projector.html",
        "sync_cost/derivations/our_address.html",
        # GIF animations
        "stairs.gif",
        "triangles.gif",
        "orbit.gif",
        "spiral.gif",
        "rose.gif",
        "genesis.gif",
        # Interactive applications
        "sync_cost/applications/double_pendulum.html",
        "sync_cost/applications/three_body_catalog.html",
    ],
    "stribeck-optics": [
        "docs/index.html",
        "stribeck_optics_results.png",
    ],
    "product": [
        "farey-heat-sinks.html",
        "farey-integral-suppression.html",
        "farey-muzzle-devices.html",
        "farey-pc-cooling.html",
    ],
}

MANIFEST_PATH = "MANIFEST.yml"


# -- Derivation metadata for machine-readable graph and glossary -----------

DERIVATIONS = {
    1:  {"title": "Born Rule", "status": "derived",
         "claim": "P = |psi|^2 from basin measure and tongue geometry",
         "depends": [10], "section": "05_predictions"},
    2:  {"title": "Spectral Tilt (Original)", "status": "superseded",
         "claim": "CMB tilt from synchronization cost gradient",
         "depends": [], "section": "05_predictions",
         "note": "Superseded by Derivation 4"},
    3:  {"title": "MOND Acceleration Scale", "status": "derived",
         "claim": "a_0 = 1.25e-10 m/s^2 from synchronization cost",
         "depends": [9, 11], "section": "06_evidence"},
    4:  {"title": "Spectral Tilt (Reframed)", "status": "derived",
         "claim": "n_s from mode-locking structure on Stern-Brocot tree",
         "depends": [10], "section": "05_predictions"},
    5:  {"title": "Two Forces", "status": "derived",
         "claim": "Coherence and decoherence as the two structural forces",
         "depends": [10], "section": "04_schrodinger"},
    6:  {"title": "Planck Scale", "status": "derived",
         "claim": "Planck scale from N=3 minimum self-sustaining loop",
         "depends": [10, 14], "section": "06_evidence"},
    7:  {"title": "Measurement Collapse", "status": "derived",
         "claim": "Collapse as tongue traversal with duration tau ~ 1/sqrt(epsilon)",
         "depends": [1, 10], "section": "06_evidence"},
    8:  {"title": "High-z MOND", "status": "testable",
         "claim": "a_0(z) = cH(z)/(2*pi) tested against high-z surveys",
         "depends": [3, 9], "section": "05_predictions"},
    9:  {"title": "Fidelity Bound", "status": "derived",
         "claim": "Self-referential fidelity bound unifying MOND and collapse",
         "depends": [1, 7, 10, 11], "section": "05_predictions"},
    10: {"title": "Minimum Alphabet", "status": "derived",
         "claim": "Four irreducible primitives: integers, mediant, fixed-point, parabola",
         "depends": [29], "section": "01_alphabet"},
    11: {"title": "Rational Field Equation", "status": "derived",
         "claim": "Self-consistency on Stern-Brocot tree in exact rational arithmetic",
         "depends": [10], "section": "02_field_equation"},
    12: {"title": "Two Continuum Limits", "status": "derived",
         "claim": "K=1 gives ADM/Einstein; K<1 linearized gives Schrodinger/Madelung",
         "depends": [11, 14], "section": "03_einstein"},
    13: {"title": "Einstein from Kuramoto", "status": "derived",
         "claim": "Exact ADM from Kuramoto at K=1; uniqueness via Lovelock",
         "depends": [12, 14, 15], "section": "03_einstein"},
    14: {"title": "Three Dimensions", "status": "derived",
         "claim": "d=3 forced by mediant -> SL(2,Z) -> SL(2,R) and self-consistent adjacency",
         "depends": [10, 11], "section": "01_alphabet"},
    15: {"title": "Lie Group Characterization", "status": "derived",
         "claim": "SL(2,R) is the unique continuum substrate via four entrance conditions",
         "depends": [14], "section": "01_alphabet"},
    16: {"title": "Variable Denominator", "status": "derived",
         "claim": "Hz with changing denominator; de Sitter as orientable fixed point",
         "depends": [9, 11], "section": "02_field_equation"},
    17: {"title": "Rank-1 Temporal Causation", "status": "derived",
         "claim": "Arrow of time is the rank-1 Frechet factorization of the update map",
         "depends": [11], "section": "02_field_equation"},
    18: {"title": "Mobius Container", "status": "derived",
         "claim": "Antiperiodic BC forces rational phase divisions from single perturbation",
         "depends": [11, 14], "section": "04a_topology"},
    19: {"title": "Klein Bottle", "status": "derived",
         "claim": "XOR parity collapses 1764 mode pairs to 4 survivors at (q1,q2)=(2,3),(3,2)",
         "depends": [18], "section": "04a_topology"},
    20: {"title": "XOR Continuum Limit", "status": "derived",
         "claim": "XOR filter dissolves in continuum; frame bundle gives Pin+(3) not SU(3)",
         "depends": [19], "section": "04a_topology",
         "note": "Honest negative: does not produce the Standard Model gauge group"},
    21: {"title": "Two Open Paths", "status": "proposed",
         "claim": "Five binary-outcome computations to resolve discrete vs continuous gauge",
         "depends": [20], "section": "04a_topology"},
    22: {"title": "Engineering Targets", "status": "proposed",
         "claim": "Four physical devices from established results",
         "depends": [18, 19], "section": "04a_topology"},
    23: {"title": "Three Zeros", "status": "derived",
         "claim": "Three structurally distinct zeros yield 1+3 decomposition",
         "depends": [19], "section": "04a_topology"},
    24: {"title": "Vacuum Energy", "status": "derived",
         "claim": "Cosmological constant problem dissolves: Klein bottle has exactly 4 modes",
         "depends": [19], "section": "04b_cosmology"},
    25: {"title": "Farey Partition", "status": "derived",
         "claim": "Omega_Lambda = |F_6|/(|F_6|+6) = 13/19 = 0.6842 (observed: 0.685)",
         "depends": [19, 28], "section": "04b_cosmology"},
    26: {"title": "Hierarchy", "status": "derived",
         "claim": "Planck/Hubble ratio R = 6 * 13^54 (residual 0.48%)",
         "depends": [25, 27], "section": "04b_cosmology"},
    27: {"title": "Exponent", "status": "derived",
         "claim": "Exponent 54 = q2 * q3^d derived from spatial dimension and Klein bottle",
         "depends": [14, 19], "section": "04b_cosmology"},
    28: {"title": "Farey Proof", "status": "derived",
         "claim": "SO(2) structure at locked/unlocked boundary forces Farey counting",
         "depends": [19, 11], "section": "04b_cosmology"},
    29: {"title": "Mediant Derivation", "status": "derived",
         "claim": "Mediant is the unique operation satisfying three simultaneous constraints",
         "depends": [], "section": "01_alphabet"},
    30: {"title": "Denomination Boundary", "status": "derived",
         "claim": "Three open questions unified: devil's staircase in K-space is a brachistochrone",
         "depends": [19, 11], "section": "04c_extended"},
    31: {"title": "Speed of Light", "status": "derived",
         "claim": "c as gate propagation speed of the coherent medium at K=1",
         "depends": [11, 14, 17], "section": "04c_extended"},
    32: {"title": "Minkowski Signature", "status": "derived",
         "claim": "(3,1) signature from phase-state observability: 3 observable + 1 dark",
         "depends": [14, 19], "section": "04c_extended"},
    33: {"title": "Duty Cycle Dictionary", "status": "derived",
         "claim": "Coupling constants from Klein bottle duty cycles: sin^2(theta_W) = 8/35",
         "depends": [19], "section": "04c_extended"},
    34: {"title": "Generation Mechanism", "status": "derived",
         "claim": "Three generations from phase-state observability at Stern-Brocot depth",
         "depends": [10, 14, 19], "section": "04c_extended"},
    35: {"title": "Cosmological Cycle", "status": "derived",
         "claim": "Two-voice round in 13/19: gap-twin at 18.7% spacetime duty",
         "depends": [19, 25], "section": "04c_extended"},
    36: {"title": "Conservation as Computability", "status": "derived",
         "claim": "S^1 compact -> |r| <= 1 -> K_eff <= 1 -> circle map invertible -> information conserved",
         "depends": [10, 11], "section": "04c_extended"},
    37: {"title": "Figure-Eight Topology", "status": "derived",
         "claim": "Klein bottle self-intersection = lemniscate; sin^2(theta_W) = 8/35 is crossing probability",
         "depends": [19, 32], "section": "04c_extended"},
    38: {"title": "Boundary Weight", "status": "derived",
         "claim": "Omega_Lambda(w) = (11+2w)/(16+3w); w* = 0.83 at K* = 0.862",
         "depends": [25, 19], "section": "04c_extended"},
    39: {"title": "Half-Möbius Boundary", "status": "derived",
         "claim": "Z4 boundary condition from half-Möbius strip",
         "depends": [18], "section": "04a_topology"},
    40: {"title": "Stribeck Vortex", "status": "derived",
         "claim": "Vortex regime map: overcritical core (K>1) + subcritical annulus (K<1)",
         "depends": [11, 36], "section": "04c_extended"},
    41: {"title": "Discrete Gauge Resolution", "status": "derived",
         "claim": "Gauge structure is discrete: charges, center Z6, confinement from XOR",
         "depends": [20, 21], "section": "04d_gauge"},
    42: {"title": "Gauge-Sector Lovelock", "status": "derived",
         "claim": "SU(3) x SU(2) x U(1) -> Yang-Mills uniquely via Utiyama + Cartan",
         "depends": [41, 14, 13], "section": "04d_gauge"},
    43: {"title": "Gell-Mann–Nishijima", "status": "derived",
         "claim": "Q = T3 + Y/2 derived from Klein bottle identification geometry",
         "depends": [42, 19], "section": "04d_gauge"},
    44: {"title": "Higgs from Tongue Boundary", "status": "derived",
         "claim": "Higgs doublet is tongue boundary mode of open q=2 fiber",
         "depends": [1, 43, 19], "section": "04d_gauge"},
    45: {"title": "Coupling Scales", "status": "derived",
         "claim": "D0 = 1/2 from tree geometry; all dimensionless ratios determined; theta = 0",
         "depends": [44, 33], "section": "04d_gauge"},
    46: {"title": "ADM Dictionary", "status": "derived",
         "claim": "Each ADM entry uniquely identified by K=1 Kuramoto symmetries",
         "depends": [12, 13], "section": "03_einstein"},
    47: {"title": "Baryon Fraction", "status": "derived",
         "claim": "Omega_b = 13/264, Omega_DM = 35/132 from two-component closure",
         "depends": [25, 19], "section": "04b_cosmology"},
}


GLOSSARY = {
    "golden ratio": {
        "symbol": "phi",
        "definition": "The positive root of x^2 - x - 1 = 0, equal to (1+sqrt(5))/2. "
                      "The most irrational number; sits at the widest gap in the devil's staircase.",
        "aka": ["phi"],
    },
    "Stern-Brocot tree": {
        "definition": "The complete binary tree of all positive rationals, built by iterated "
                      "mediants starting from 0/1 and 1/0. The natural coordinate system for "
                      "the devil's staircase.",
    },
    "devil's staircase": {
        "definition": "The winding number W(Omega) of the circle map as a function of driving "
                      "frequency. A continuous, monotone function that is locally constant almost "
                      "everywhere (on the Arnold tongues) yet maps [0,1] onto [0,1].",
    },
    "Arnold tongue": {
        "definition": "A region in (Omega, K) parameter space where the circle map locks to "
                      "a rational winding number p/q. Width scales as K^q at small coupling.",
    },
    "mode-locking": {
        "definition": "The phenomenon where a driven oscillator synchronizes to a rational "
                      "multiple of the driving frequency. The locked states form the Arnold tongues.",
    },
    "Kuramoto model": {
        "definition": "A system of N coupled phase oscillators: d(theta_i)/dt = omega_i + "
                      "(K/N) sum sin(theta_j - theta_i). The mean-field model of synchronization.",
    },
    "mediant": {
        "definition": "The operation (a+c)/(b+d) on two fractions a/b and c/d. Derived in D29 "
                      "as the unique operation satisfying monotonicity, denominator-additivity, "
                      "and convergent-stability.",
        "derivation": 29,
    },
    "Born rule": {
        "definition": "The quantum measurement postulate P = |psi|^2. Here derived (D1) from "
                      "saddle-node universality at Arnold tongue boundaries: Delta(theta) ~ sqrt(epsilon).",
        "derivation": 1,
    },
    "order parameter": {
        "symbol": "r",
        "definition": "The magnitude of the mean field r*exp(i*psi) = (1/N) sum exp(i*theta_j). "
                      "r=1 means full synchronization (K=1, gravity); r<1 means partial (K<1, QM).",
    },
    "ADM formalism": {
        "definition": "The Arnowitt-Deser-Misner 3+1 decomposition of general relativity. "
                      "Spacetime is foliated into spatial slices with lapse N, shift N^i, "
                      "and 3-metric gamma_ij.",
    },
    "Lovelock theorem": {
        "definition": "In 4D, the only divergence-free symmetric rank-2 tensor built from the "
                      "metric and its first two derivatives is G_mu_nu + Lambda*g_mu_nu. "
                      "Forces Einstein's equation uniquely at K=1 (D13).",
        "derivation": 13,
    },
    "Madelung transform": {
        "definition": "Writing Psi = sqrt(rho)*exp(iS/hbar), converting Schrodinger into "
                      "continuity + Hamilton-Jacobi with a quantum pressure term. "
                      "The K<1 continuum limit of the field equation (D12).",
        "derivation": 12,
    },
    "Farey sequence": {
        "symbol": "F_n",
        "definition": "The ascending sequence of reduced fractions p/q in [0,1] with q <= n. "
                      "|F_6| = 13 determines the dark energy fraction Omega_Lambda = 13/19 (D25).",
        "derivation": 25,
    },
    "Klein bottle": {
        "definition": "A closed non-orientable surface: two antiperiodic directions with XOR "
                      "parity. The configuration space that collapses 1764 mode pairs to exactly "
                      "4 survivors (D19).",
        "derivation": 19,
    },
    "fidelity bound": {
        "definition": "The self-referential constraint: the measurement instrument IS the "
                      "measured dynamics. Unifies MOND transition and wavefunction collapse (D9).",
        "derivation": 9,
    },
    "MOND": {
        "definition": "Modified Newtonian Dynamics. Below acceleration a_0, gravitational "
                      "dynamics deviate from Newton. Here a_0 = cH_0/(2*pi) / sqrt(g*(1/phi)) "
                      "is derived, not postulated (D3).",
        "derivation": 3,
    },
    "spectral tilt": {
        "symbol": "n_s",
        "definition": "The scalar spectral index of primordial perturbations. n_s = 1 is "
                      "scale-invariant; observed n_s ~ 0.965. Derived from Stern-Brocot "
                      "level sampling rate (D4).",
        "derivation": 4,
    },
    "SL(2,R)": {
        "definition": "The group of 2x2 real matrices with determinant 1. The unique "
                      "continuum substrate: mediant -> SL(2,Z) -> SL(2,R). Its dimension "
                      "(2^2 - 1 = 3) forces d=3 spatial dimensions (D14, D15).",
        "derivation": 15,
    },
    "circle map": {
        "definition": "theta_{n+1} = theta_n + Omega - (K/2*pi)*sin(2*pi*theta_n). "
                      "The simplest model exhibiting mode-locking, Arnold tongues, "
                      "and the devil's staircase.",
    },
    "rational field equation": {
        "definition": "N(p/q) = N_total * g(p/q) * w(p/q, K_0*F[N]) on the Stern-Brocot "
                      "tree. The self-consistency condition whose K=1 limit is Einstein "
                      "and K<1 limit is Schrodinger (D11).",
        "derivation": 11,
    },
}


def fetch_file_github(repo_slug, path):
    url = f"https://raw.githubusercontent.com/{repo_slug}/main/{path}"
    return urlopen(Request(url), timeout=30).read()


def fetch_file_local(local_root, repo_name, path):
    return (Path(local_root) / repo_name / path).read_bytes()


def load_manifest(local_root=None):
    """Load MANIFEST.yml from harmonics (local or GitHub)."""
    try:
        if local_root:
            data = fetch_file_local(local_root, "harmonics", MANIFEST_PATH)
        else:
            data = fetch_file_github(REPOS["harmonics"], MANIFEST_PATH)
        text = data.decode("utf-8")
        if yaml:
            return yaml.safe_load(text)
        # Minimal fallback: extract flat scalar keys we actually need
        manifest = {}
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("#") or not line or ":" not in line:
                continue
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val.isdigit():
                val = int(val)
            manifest[key] = val
        return manifest
    except (FileNotFoundError, URLError, OSError) as e:
        print(f"  MANIFEST.yml — MISSING ({e}), using defaults")
        return {"derivation_count": 47, "derivation_range": "1–47",
                "free_parameters": 0, "free_functions": 0}


def fetch_sources(local_root=None):
    result = {}
    for section_id, section in SECTIONS.items():
        for repo_name, path in section.get("files", []):
            key = f"{repo_name}/{path}"
            if key in result:
                continue
            try:
                if local_root:
                    data = fetch_file_local(local_root, repo_name, path)
                else:
                    data = fetch_file_github(REPOS[repo_name], path)
                result[key] = (section_id, repo_name, path, data)
                print(f"  {key}")
            except (FileNotFoundError, URLError, OSError) as e:
                print(f"  {key} — MISSING ({e})")
    return result


def fetch_script_and_data_files(local_root=None):
    """Fetch Python scripts and data files needed for execution."""
    fetched = {}
    for name, paths in SCRIPT_FILES.items():
        slug = REPOS[name]
        for path in paths:
            try:
                if local_root:
                    data = fetch_file_local(local_root, name, path)
                else:
                    data = fetch_file_github(slug, path)
                fetched[f"{name}/{path}"] = (name, path, data)
                print(f"  {name}/{path} (script)")
            except (FileNotFoundError, URLError, OSError) as e:
                print(f"  {name}/{path} — MISSING ({e})")
    for name, paths in DATA_FILES.items():
        slug = REPOS[name]
        for path in paths:
            try:
                if local_root:
                    data = fetch_file_local(local_root, name, path)
                else:
                    data = fetch_file_github(slug, path)
                fetched[f"{name}/{path}"] = (name, path, data)
                print(f"  {name}/{path} (data)")
            except (FileNotFoundError, URLError, OSError) as e:
                print(f"  {name}/{path} — MISSING ({e})")
    return fetched


def fetch_static_assets(local_root=None):
    """Fetch static assets (HTML, GIF, PNG). Returns {repo: {path: bytes}}."""
    result = {}
    for name, paths in STATIC_ASSETS.items():
        result[name] = {}
        slug = REPOS[name]
        for path in paths:
            try:
                if local_root:
                    data = fetch_file_local(local_root, name, path)
                else:
                    data = fetch_file_github(slug, path)
                result[name][path] = data
                print(f"  {name}/{path} (static)")
            except (FileNotFoundError, URLError, OSError) as e:
                print(f"  {name}/{path} — MISSING ({e})")
    return result


def copy_static_assets(static_sources):
    """Copy fetched static assets into book/_static/."""
    static_dir = BOOK_DIR / "_static"
    static_dir.mkdir(parents=True, exist_ok=True)
    for repo, files in static_sources.items():
        for path, data in files.items():
            # Flatten into _static/ using just the filename
            filename = Path(path).name
            dest = static_dir / filename
            dest.write_bytes(data)
            print(f"  _static/{filename}")


CONTENT_DIR = SITE_DIR / "content"


def write_book_sources(sources, extra_files=None):
    if BOOK_DIR.exists():
        shutil.rmtree(BOOK_DIR)

    for key, (section_id, repo_name, path, data) in sources.items():
        dest = BOOK_DIR / section_id / Path(path).name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)

    # Write script and data files into the book tree (preserving repo/path)
    if extra_files:
        for key, (repo_name, path, data) in extra_files.items():
            dest = BOOK_DIR / repo_name / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)

    # Copy local content files
    for section_id, section in SECTIONS.items():
        for filename in section.get("local", []):
            src = CONTENT_DIR / filename
            dest = BOOK_DIR / section_id / filename
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            print(f"  {section_id}/{filename} (local)")


def resolve_script_references():
    """Rewrite .py script references and internal .md cross-references in book markdown.

    After write_book_sources() copies raw files into the book directory, local
    references like `born_rule_tongues.py` or `[text](PROOF_A_gravity.md)` break
    because those files aren't in the book.  This pass converts them to GitHub
    links or corrected relative paths.
    """
    import re

    # Build a reverse lookup: book filename -> (repo_name, original_path)
    # so we know which GitHub repo a given book file came from.
    file_origin = {}
    for section_id, section in SECTIONS.items():
        for repo_name, path in section.get("files", []):
            filename = Path(path).name
            file_origin[f"{section_id}/{filename}"] = (repo_name, path)

    # --- GitHub URL mappings keyed by repo + original source path ---
    REPO_SCRIPT_MAPS = {
        "harmonics": [
            ("sync_cost/derivations/",
             "https://github.com/nickjoven/harmonics/blob/main/sync_cost/derivations/"),
            ("seed/src/",
             "https://github.com/nickjoven/harmonics/blob/main/seed/src/"),
            ("",
             "https://github.com/nickjoven/harmonics/blob/main/"),
        ],
        "201": [
            ("", "https://github.com/nickjoven/201/blob/main/"),
        ],
        "intersections": [
            ("", "https://github.com/nickjoven/intersections/blob/main/"),
        ],
        "proslambenomenos": [
            ("", "https://github.com/nickjoven/proslambenomenos/blob/main/"),
        ],
    }

    def _github_url_for(book_rel_path, script_name):
        """Given a file's book-relative path, return the GitHub URL for a script."""
        origin = file_origin.get(book_rel_path)
        if not origin:
            return None
        repo_name, orig_path = origin
        maps = REPO_SCRIPT_MAPS.get(repo_name, [])
        orig_dir = str(Path(orig_path).parent)
        if orig_dir == ".":
            orig_dir = ""
        else:
            orig_dir = orig_dir + "/"
        for prefix, base_url in maps:
            if orig_dir.startswith(prefix):
                return base_url + script_name
        return None

    # Build a lookup: filename -> book-relative path for all .md files in the book
    md_index = {}
    for md_path in BOOK_DIR.rglob("*.md"):
        rel = md_path.relative_to(BOOK_DIR).as_posix()
        md_index.setdefault(md_path.name, []).append(rel)

    def _resolve_md_ref(book_rel_path, target):
        """Resolve a .md reference to a correct relative path within the book."""
        target_name = Path(target).name
        candidates = md_index.get(target_name, [])
        if not candidates:
            return None
        current_dir = str(Path(book_rel_path).parent)
        # Same directory? Already correct as a bare filename.
        for c in candidates:
            if str(Path(c).parent) == current_dir:
                return target_name
        # Otherwise compute relative path from the file's directory
        from_dir = Path(book_rel_path).parent
        best = Path(candidates[0])
        return os.path.relpath(best, from_dir)

    count_scripts = 0
    count_md_refs = 0

    for md_file in BOOK_DIR.rglob("*.md"):
        book_rel = md_file.relative_to(BOOK_DIR).as_posix()
        text = md_file.read_text(encoding="utf-8", errors="replace")
        original = text

        # 1) Fix markdown links to .py files: [text](script.py) -> [text](github_url)
        def _replace_link_py(m):
            nonlocal count_scripts
            full_match = m.group(0)
            link_text = m.group(1)
            script = m.group(2)
            if script.startswith(("http://", "https://")):
                return full_match
            url = _github_url_for(book_rel, script)
            if url:
                count_scripts += 1
                return f"[{link_text}]({url})"
            return full_match

        text = re.sub(r'\[([^\]]*)\]\(([^)]*\.py)\)', _replace_link_py, text)

        # 2) Fix backtick-wrapped .py references: `script.py` -> [`script.py`](github_url)
        #    Skip if already inside a markdown link [...](...) structure
        def _replace_backtick_py(m):
            nonlocal count_scripts
            prefix = m.group(1)
            script = m.group(2)
            if prefix.endswith("](") or prefix.endswith("["):
                return m.group(0)
            url = _github_url_for(book_rel, script)
            if url:
                count_scripts += 1
                return f"{prefix}[`{script}`]({url})"
            return m.group(0)

        text = re.sub(r'(^|[^[\](])`([a-zA-Z_]\w*\.py)`', _replace_backtick_py, text,
                       flags=re.MULTILINE)

        # 3) Fix internal .md cross-references: [text](file.md) -> corrected relative path
        #    Only fix bare filenames or simple relative refs, not URLs
        def _replace_link_md(m):
            nonlocal count_md_refs
            full_match = m.group(0)
            link_text = m.group(1)
            target = m.group(2)
            if target.startswith(("http://", "https://")):
                return full_match
            target_name = Path(target).name
            if not target_name.endswith(".md"):
                return full_match
            resolved = _resolve_md_ref(book_rel, target)
            if resolved and resolved != target:
                count_md_refs += 1
                return f"[{link_text}]({resolved})"
            return full_match

        text = re.sub(r'\[([^\]]*)\]\(([^)]*\.md)\)', _replace_link_md, text)

        if text != original:
            md_file.write_text(text, encoding="utf-8")

    print(f"  Resolved {count_scripts} script references, {count_md_refs} internal .md cross-references")


def generate_schrodinger_intro():
    """Generate the K < 1 bridging page pointing to Derivation 12 Part II."""
    text = """\
# K < 1: Schrödinger

At subcritical coupling ($K < 1$), the order parameter $r$ is small and a
finite fraction of oscillators remain **unlocked** — they sit in the gaps
of the devil's staircase with no definite winding number. These are the
quantum states.

The linearized Kuramoto equation in this regime, with nearest-neighbor
diffusive coupling on a spatial lattice, reduces to the **Schrödinger
equation** via the Madelung transform:

$$i\\hbar\\partial_t\\Psi = -\\frac{\\hbar^2}{2m}\\nabla^2\\Psi + V\\Psi$$

where:

| Kuramoto quantity | QM quantity |
|---|---|
| Unlocked oscillator density $\\rho(x,t)$ | $\\lvert\\Psi\\rvert^2$ |
| Accumulated phase perturbation $S(x,t)$ | Action / phase |
| Tongue-structure effective potential | $V(x)$ |
| Stern-Brocot RG diffusion $D_{\\text{eff}}$ | Quantum potential $\\frac{\\hbar^2}{2m}\\frac{\\nabla^2\\sqrt{\\rho}}{\\sqrt{\\rho}}$ |

The quantum potential — the term that distinguishes quantum from classical
mechanics — arises from the **Stern-Brocot renormalization group flow**:
per-level variance $\\sigma^2(d) \\sim \\phi^{-4d}$ sums to a convergent
constant $D_{\\text{eff}} = D_0 / (1 - \\phi^{-4})$.

The full derivation is in [Derivation 12: The Two Continuum Limits](../03_einstein/continuum_limits.md),
Part II.

## Three regimes, one equation

| Coupling | Regime | Physics |
|---|---|---|
| $K = 1$ | Critical — all oscillators locked | **General relativity** (Lovelock uniqueness) |
| $0 < K < 1$ | Subcritical — partial locking | **Quantum mechanics** (Madelung / Nelson) |
| $K \\to 0$ | No coupling | Free particles — no structure |

The transition between regimes is controlled by the **same** self-consistency
equation on the Stern-Brocot tree (Derivation 11). There is no
quantization postulate.
"""
    dest = BOOK_DIR / "04_schrodinger" / "04_schrodinger_intro.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text)
    print("  04_schrodinger/04_schrodinger_intro.md")


def generate_toc():
    lines = [
        "format: jb-book",
        "root: intro",
        "parts:",
    ]
    for section_id in sorted(SECTIONS.keys()):
        section = SECTIONS[section_id]
        lines.append(f'  - caption: "{section["title"]}"')
        lines.append("    chapters:")

        # Collect all files for this section
        all_files = []
        for gen_name in section.get("generated", []):
            all_files.append(f"{section_id}/{Path(gen_name).stem}")
        for repo_name, path in section.get("files", []):
            all_files.append(f"{section_id}/{Path(path).stem}")
        for local_name in section.get("local", []):
            all_files.append(f"{section_id}/{Path(local_name).stem}")

        if not all_files:
            continue

        # First file is the visible entry; rest nest as collapsed sections
        lines.append(f"      - file: {all_files[0]}")
        if len(all_files) > 1:
            lines.append("        sections:")
            for f in all_files[1:]:
                lines.append(f"          - file: {f}")

    # Reference: graph, equations, visuals, glossary — all adjacent
    lines.append('  - caption: "Reference"')
    lines.append("    chapters:")
    lines.append('      - file: graph')
    lines.append('        title: "Derivation Graph"')
    lines.append('      - file: equations')
    lines.append('        title: "Key Equations"')
    lines.append('      - file: visuals')
    lines.append('        title: "Visual Assets"')
    lines.append("      - file: glossary")

    toc_path = BOOK_DIR / "_toc.yml"
    toc_path.write_text("\n".join(lines) + "\n")
    print(f"  _toc.yml")


def generate_config():
    config = """\
title: "Submediant"
author: "N. Joven"
copyright: "2026"
logo: ""

execute:
  execute_notebooks: cache
  timeout: 300
  allow_errors: false

repository:
  url: https://github.com/nickjoven/harmonics
  path_to_docs: ""

html:
  use_issues_button: false
  use_repository_button: true
  use_edit_page_button: false
  favicon: ""
  extra_css:
    - _static/custom.css
    - _static/glossary.css
    - _static/mobius-theme.css

sphinx:
  config:
    mathjax3_config:
      tex:
        macros:
          "RR": "\\\\mathbb{R}"
          "NN": "\\\\mathbb{N}"
    html_js_files:
      - glossary.js
      - mobius-theme.js
    html_theme_options:
      navigation_with_keys: false
      collapse_navigation: true
      show_nav_level: 1
      navigation_depth: 2
      icon_links:
        - name: GitHub
          url: https://github.com/nickjoven
          icon: fa-brands fa-github
"""
    (BOOK_DIR / "_config.yml").write_text(config)

    static_dir = BOOK_DIR / "_static"
    static_dir.mkdir(exist_ok=True)
    (static_dir / "custom.css").write_text("""\
:root {
  --pst-color-primary: #58a6ff;
  --pst-color-secondary: #7ee787;
}
""")
    # Copy canonical Mobius theme files from repo root
    for fname in ["mobius-theme.css", "mobius-theme.js", "diagram-controls.js"]:
        src = SITE_DIR / "static" / fname
        if src.exists():
            shutil.copy2(src, static_dir / fname)
            print(f"  _static/{fname}")

    # Copy reference pages — .md to book root, .html to _static for direct serving
    ref_dir = SITE_DIR / "reference"
    if ref_dir.exists():
        for f in ref_dir.iterdir():
            if f.suffix == ".html":
                shutil.copy2(f, static_dir / f.name)
                print(f"  _static/{f.name}")
            elif f.suffix == ".md":
                shutil.copy2(f, BOOK_DIR / f.name)
                print(f"  {f.name}")
    print("  _config.yml")


def generate_intro(manifest):
    d_count = manifest.get("derivation_count", 29)
    d_range = manifest.get("derivation_range", "1–29")

    intro = f"""\
# Submediant

N. Joven — 2026 — [ORCID 0009-0008-0679-0812](https://orcid.org/0009-0008-0679-0812) — CC0 1.0

Source: [harmonics](https://github.com/nickjoven/harmonics)

---

You know this pattern.

Take two numbers. Add them. Use the last two to make the next.
1, 1, 2, 3, 5, 8, 13, 21 ...

The ratio between consecutive terms settles to $\\phi = (1 + \\sqrt{{5}})/2$.
This is the golden ratio — the number that appears in sunflower spirals,
nautilus shells, and the branching of trees.

It also appears in the cosmic microwave background.

The polynomial behind the Fibonacci sequence, $x^2 - x - 1 = 0$,
has two roots. Three properties of these roots correspond to three
physical measurements:

| What the roots do | What we observe | Residual |
|---|---|---|
| Their product is $\\pm 1$ | Born rule: $P = \\lvert\\psi\\rvert^2$ | exact |
| $\\phi^2 = \\phi + 1$ (self-similarity) | CMB spectral tilt $n_s \\approx 0.965$ | 0.2% |
| $\\phi - \\psi = \\sqrt{{5}}$ (gap width) | Inflation lasted $\\sim 61$ e-folds | CMB-S4, ~2030 |

The same polynomial also determines that space has **three dimensions**
(because fractions have two parts: $\\dim \\mathrm{{SL}}(2) = 2^2 - 1 = 3$)
and that the MOND acceleration scale is $a_0 = 1.25 \\times 10^{{-10}}$ m/s$^2$
(observed: $1.2 \\times 10^{{-10}}$, residual: 4%).

The frequency distribution $g(\\omega)$ is fixed by self-consistency:
the distribution that produces dynamics reproducing that distribution
is unique. The dimensionless predictions follow from the recurrence;
setting absolute scales requires two dimensionful anchors — the
cosmological scale $H_0$ and the electroweak scale $v_{{\\text{{EW}}}} = 246$ GeV.

This site walks through the derivation chain, starting from the polynomial
and arriving at known physics:

**Counting** $\\to$ **fractions** $\\to$ **the golden ratio** $\\to$
**mode-locking** $\\to$ **the devil's staircase** $\\to$ **a self-consistency
equation** $\\to$ **general relativity and quantum mechanics**

Each step is a composition of the previous ones. The
[derivation chain](https://github.com/nickjoven/harmonics) is {d_count} steps.
The [engine](https://github.com/nickjoven/rfe) solves the equation
numerically and produces all predictions from a single run.

## Where to start

- **Curious about the math?** Start with [The Alphabet](01_alphabet/minimum_alphabet.html) —
  four primitives that generate all the structure
- **Curious about the physics?** Start with [Predictions](05_predictions/born_rule.html) —
  what the framework says and how it compares to measurement
- **Want the punchline?** [K = 1: Einstein](03_einstein/einstein_from_kuramoto.html) —
  how one equation produces general relativity, uniquely
- **Want to run it?** [rfe](https://github.com/nickjoven/rfe) —
  `python -m rfe --observables`
- **From scratch?** [First Principles](https://nickjoven.github.io/submediant-site/first-principles.html) —
  sin(ωt) to Einstein in 10 steps
- **Where are we?** [Our Address](https://nickjoven.github.io/submediant-site/our_address.html) —
  the universe's computational clock on the Stern-Brocot tree

## Source

- [harmonics](https://github.com/nickjoven/harmonics) — the derivation chain (Derivations {d_range})
- [rfe](https://github.com/nickjoven/rfe) — the engine (one equation, all observables)
- [proslambenomenos](https://github.com/nickjoven/proslambenomenos) — Λ → a₀: one frequency, structural
- [201](https://github.com/nickjoven/201) — gravity as synchronization in a frictional medium
- [intersections](https://github.com/nickjoven/intersections) — stick-slip dynamics and dark matter
"""
    (BOOK_DIR / "intro.md").write_text(intro)
    print("  intro.md")


def generate_derivation_graph():
    """Generate machine-readable derivation graph as JSON and JSON-LD."""
    static_dir = BOOK_DIR / "_static"
    static_dir.mkdir(exist_ok=True)

    # Plain JSON graph for programmatic consumption
    graph = {
        "title": "Submediant Derivation Chain",
        "description": "47 derivations from x^2 - x - 1 = 0 to general relativity, quantum mechanics, and the Standard Model",
        "author": "N. Joven",
        "license": "CC0 1.0",
        "derivation_count": len(DERIVATIONS),
        "dimensionful_anchors": 2,
        "derivations": {},
        "edges": [],
    }
    for num, d in sorted(DERIVATIONS.items()):
        node = {
            "number": num,
            "title": d["title"],
            "status": d["status"],
            "claim": d["claim"],
            "section": d["section"],
            "depends_on": d["depends"],
        }
        if "note" in d:
            node["note"] = d["note"]
        graph["derivations"][str(num)] = node
        for dep in d["depends"]:
            graph["edges"].append({"from": dep, "to": num})

    (static_dir / "derivation-graph.json").write_text(
        json.dumps(graph, indent=2))
    print("  _static/derivation-graph.json")

    # JSON-LD for search engines and LLMs
    jsonld = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "name": "Submediant",
        "author": {"@type": "Person", "name": "N. Joven",
                    "identifier": "https://orcid.org/0009-0008-0679-0812"},
        "license": "https://creativecommons.org/publicdomain/zero/1.0/",
        "description": (
            "A derivation chain showing how x^2 - x - 1 = 0 leads to "
            "general relativity (K=1), quantum mechanics (K<1), and the "
            "Standard Model gauge group."
        ),
        "hasPart": [
            {"@type": "Chapter", "name": f"Derivation {n}: {d['title']}",
             "position": n, "description": d["claim"]}
            for n, d in sorted(DERIVATIONS.items())
        ],
    }
    (static_dir / "jsonld.json").write_text(json.dumps(jsonld, indent=2))
    print("  _static/jsonld.json")


def generate_glossary():
    """Generate glossary data file and tooltip JS/CSS (off by default)."""
    static_dir = BOOK_DIR / "_static"
    static_dir.mkdir(exist_ok=True)

    # Glossary JSON for machine consumption and JS tooltips
    glossary_data = {}
    for term, entry in GLOSSARY.items():
        glossary_data[term] = {
            "definition": entry["definition"],
        }
        if "symbol" in entry:
            glossary_data[term]["symbol"] = entry["symbol"]
        if "derivation" in entry:
            glossary_data[term]["derivation"] = entry["derivation"]
        if "aka" in entry:
            glossary_data[term]["aka"] = entry["aka"]
    (static_dir / "glossary.json").write_text(
        json.dumps(glossary_data, indent=2))
    print("  _static/glossary.json")

    # Tooltip CSS
    tooltip_css = """\
/* Glossary tooltip styles — active only when [data-glossary="on"] is set on <html> */
html[data-glossary="on"] .glossary-term {
  border-bottom: 1px dotted var(--pst-color-secondary, #7ee787);
  cursor: help;
  position: relative;
}
html:not([data-glossary="on"]) .glossary-term {
  /* No visual change when glossary is off */
}
.glossary-tooltip {
  display: none;
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: var(--pst-color-surface, #1e1e2e);
  color: var(--pst-color-text-base, #cdd6f4);
  border: 1px solid var(--pst-color-border, #45475a);
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 0.85rem;
  line-height: 1.4;
  max-width: 360px;
  min-width: 200px;
  z-index: 1000;
  white-space: normal;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  pointer-events: none;
}
html[data-glossary="on"] .glossary-term:hover .glossary-tooltip,
html[data-glossary="on"] .glossary-term:focus .glossary-tooltip {
  display: block;
}
.glossary-tooltip .glossary-ref {
  display: block;
  margin-top: 4px;
  font-size: 0.8em;
  opacity: 0.7;
}
#glossary-toggle {
  position: fixed;
  bottom: 16px;
  right: 16px;
  z-index: 999;
  background: var(--pst-color-surface, #1e1e2e);
  color: var(--pst-color-text-base, #cdd6f4);
  border: 1px solid var(--pst-color-border, #45475a);
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 0.8rem;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
}
#glossary-toggle:hover {
  opacity: 1;
}
"""
    (static_dir / "glossary.css").write_text(tooltip_css)
    print("  _static/glossary.css")

    # Tooltip JS — scans text nodes and wraps glossary terms
    tooltip_js = """\
(function() {
  "use strict";

  var GLOSSARY = null;
  var ACTIVE = localStorage.getItem("glossary") === "on";

  function applyState() {
    document.documentElement.setAttribute("data-glossary", ACTIVE ? "on" : "off");
    var btn = document.getElementById("glossary-toggle");
    if (btn) btn.textContent = ACTIVE ? "Glossary: ON" : "Glossary: OFF";
  }

  function createToggle() {
    var btn = document.createElement("button");
    btn.id = "glossary-toggle";
    btn.type = "button";
    btn.addEventListener("click", function() {
      ACTIVE = !ACTIVE;
      localStorage.setItem("glossary", ACTIVE ? "on" : "off");
      applyState();
    });
    document.body.appendChild(btn);
  }

  function escapeRegex(s) {
    return s.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&");
  }

  function annotateNode(textNode) {
    var text = textNode.nodeValue;
    if (!text || !text.trim()) return;
    // Skip nodes inside tooltips, code blocks, math, headings
    var parent = textNode.parentElement;
    if (!parent) return;
    var tag = parent.tagName;
    if (tag === "CODE" || tag === "PRE" || tag === "SCRIPT" || tag === "STYLE") return;
    if (parent.closest(".glossary-term, .glossary-tooltip, .MathJax, mjx-container, h1, h2, h3")) return;

    var terms = Object.keys(GLOSSARY).sort(function(a, b) { return b.length - a.length; });
    // Collect all terms and their aliases
    var allPatterns = [];
    terms.forEach(function(term) {
      allPatterns.push({ pattern: term, key: term });
      var entry = GLOSSARY[term];
      if (entry.aka) {
        entry.aka.forEach(function(a) { allPatterns.push({ pattern: a, key: term }); });
      }
    });
    allPatterns.sort(function(a, b) { return b.pattern.length - a.pattern.length; });

    var parts = allPatterns.map(function(p) { return escapeRegex(p.pattern); });
    if (!parts.length) return;
    var regex = new RegExp("\\\\b(" + parts.join("|") + ")\\\\b", "gi");
    if (!regex.test(text)) return;

    // Build a lookup from lowercase pattern to key
    var lookup = {};
    allPatterns.forEach(function(p) { lookup[p.pattern.toLowerCase()] = p.key; });

    var fragment = document.createDocumentFragment();
    var lastIndex = 0;
    regex.lastIndex = 0;
    var match;
    var replaced = false;
    while ((match = regex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        fragment.appendChild(document.createTextNode(text.slice(lastIndex, match.index)));
      }
      var matched = match[0];
      var key = lookup[matched.toLowerCase()];
      var entry = GLOSSARY[key];
      var span = document.createElement("span");
      span.className = "glossary-term";
      span.tabIndex = 0;
      span.textContent = matched;
      var tip = document.createElement("span");
      tip.className = "glossary-tooltip";
      tip.setAttribute("role", "tooltip");
      tip.textContent = entry.definition;
      if (entry.derivation) {
        var ref = document.createElement("span");
        ref.className = "glossary-ref";
        ref.textContent = "See Derivation " + entry.derivation;
        tip.appendChild(ref);
      }
      span.appendChild(tip);
      fragment.appendChild(span);
      lastIndex = regex.lastIndex;
      replaced = true;
    }
    if (replaced) {
      if (lastIndex < text.length) {
        fragment.appendChild(document.createTextNode(text.slice(lastIndex)));
      }
      parent.replaceChild(fragment, textNode);
    }
  }

  function annotate() {
    // Only annotate main content area
    var main = document.querySelector("main, .bd-content, article, #main-content");
    if (!main) main = document.body;
    var walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT, null, false);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    // Process in reverse to avoid invalidating walker
    for (var i = nodes.length - 1; i >= 0; i--) {
      annotateNode(nodes[i]);
    }
  }

  function init() {
    fetch("_static/glossary.json")
      .then(function(r) { return r.json(); })
      .then(function(data) {
        GLOSSARY = data;
        createToggle();
        applyState();
        annotate();
      })
      .catch(function() {
        // Glossary unavailable — degrade silently
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
"""
    (static_dir / "glossary.js").write_text(tooltip_js)
    print("  _static/glossary.js")


def build_book():
    # jupyter-book <2 exposes CLI via jupyter_book.cli.main
    # jupyter-book >=2 uses myst and has a different CLI
    # We require <2 (see requirements.txt); use the entry point directly.
    cmd = [shutil.which("jupyter-book") or "jupyter-book", "build", str(BOOK_DIR)]
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        return False

    # Copy standalone HTML pages to build output root (served as pages, not downloads)
    build_html = BOOK_DIR / "_build" / "html"
    if build_html.exists():
        ref_dir = SITE_DIR / "reference"
        if ref_dir.exists():
            for f in ref_dir.iterdir():
                if f.suffix == ".html":
                    shutil.copy2(f, build_html / f.name)
                    print(f"  → {f.name} (served as page)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Build the submediant site")
    parser.add_argument("--local", type=str, default=None,
                        help="Path to parent directory containing sibling repos")
    parser.add_argument("--fetch-only", action="store_true",
                        help="Fetch sources and generate book structure, skip build")
    args = parser.parse_args()

    local_root = Path(args.local).resolve() if args.local else None

    print("Loading manifest...")
    framework_manifest = load_manifest(local_root)
    print(f"  derivation_count: {framework_manifest.get('derivation_count', '?')}")

    print("\nFetching sources...")
    sources = fetch_sources(local_root)

    print("\nFetching scripts and data files...")
    extra_files = fetch_script_and_data_files(local_root)

    print("\nFetching static assets...")
    static_sources = fetch_static_assets(local_root)

    print("\nWriting book sources...")
    write_book_sources(sources, extra_files)

    print("\nCopying static assets...")
    copy_static_assets(static_sources)

    print("\nResolving script references and cross-links...")
    resolve_script_references()

    print("\nGenerating Jupyter Book config...")
    generate_config()
    generate_schrodinger_intro()
    generate_toc()
    generate_intro(framework_manifest)

    print("\nGenerating machine-readable metadata...")
    generate_derivation_graph()
    generate_glossary()

    content_manifest = {k: hashlib.sha256(v[3]).hexdigest()[:16]
                        for k, v in sources.items()}
    (BOOK_DIR / "manifest.json").write_text(json.dumps(content_manifest, indent=2))

    if args.fetch_only:
        print(f"\nFetch complete. Book sources at {BOOK_DIR}")
        return 0

    print("\nBuilding Jupyter Book...")
    if not build_book():
        return 1

    print(f"\nBuild complete: {BOOK_DIR / '_build' / 'html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
