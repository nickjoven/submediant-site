# Derivation Graph

Interactive force-directed visualization of the framework's derivation chain and repository structure.

```{raw} html
<div id="graph-container" style="
  width: 100%;
  height: 90vh;
  min-height: 700px;
  background: #0d1117;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
">
  <!-- Title overlay -->
  <div style="
    position: absolute;
    top: 24px;
    left: 32px;
    z-index: 10;
    pointer-events: none;
  ">
    <div style="
      font-size: 22px;
      font-weight: 700;
      color: #e6edf3;
      letter-spacing: 0.02em;
    ">Derivation Substrate</div>
    <div style="
      font-size: 13px;
      color: #8b949e;
      margin-top: 4px;
      font-weight: 400;
    ">Force-directed graph of the synchronization framework</div>
  </div>

  <!-- Legend -->
  <div id="graph-legend" style="
    position: absolute;
    top: 24px;
    right: 32px;
    z-index: 10;
    background: rgba(13, 17, 23, 0.85);
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 12px;
    color: #c9d1d9;
    backdrop-filter: blur(8px);
  ">
    <div style="margin-bottom: 8px; font-weight: 600; color: #e6edf3; font-size: 13px;">Legend</div>
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
      <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#ffd75c;margin-right:8px;"></span>Foundation
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
      <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#58a6ff;margin-right:8px;"></span>Field Equation
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
      <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#7ee787;margin-right:8px;"></span>Spacetime (K=1)
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
      <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#d2a8ff;margin-right:8px;"></span>Topology
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
      <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#ffa657;margin-right:8px;"></span>Cosmology
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
      <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#f5a9b8;margin-right:8px;"></span>Extended
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
      <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#ff7b72;margin-right:8px;"></span>Gauge Sector
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
      <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#79c0ff;margin-right:8px;"></span>Predictions
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
      <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#8b949e;margin-right:8px;"></span>Prior Work
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
      <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#0d1117;border:2px solid #e6edf3;margin-right:8px;"></span>Repository
    </div>
    <div style="display: flex; align-items: center;">
      <span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#484f58;margin-right:8px;"></span>Media Asset
    </div>
  </div>

  <!-- Attribution -->
  <div style="
    position: absolute;
    bottom: 16px;
    right: 32px;
    z-index: 10;
    font-size: 11px;
    color: #484f58;
    pointer-events: none;
  ">N. Joven — github.com/nickjoven</div>

  <!-- Tooltip -->
  <div id="graph-tooltip" style="
    position: absolute;
    display: none;
    background: rgba(22, 27, 34, 0.95);
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: #c9d1d9;
    pointer-events: none;
    z-index: 20;
    max-width: 280px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
  ">
    <div id="tooltip-title" style="font-weight: 600; color: #e6edf3; margin-bottom: 4px;"></div>
    <div id="tooltip-claim" style="font-size: 11px; color: #8b949e; line-height: 1.4;"></div>
  </div>

  <svg id="graph-svg" style="width:100%;height:100%;"></svg>
</div>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
(function() {

// ─── Data ────────────────────────────────────────────────────────────────────

const derivations = [
  // Foundation (gold)
  { id: "D29", label: "D29", title: "Mediant Derivation", claim: "The mediant operation (a+c)/(b+d) is the unique binary operation preserving Farey adjacency.", color: "#ffd75c", group: "foundation", r: 12 },
  { id: "D10", label: "D10", title: "Minimum Alphabet", claim: "Three coupled oscillators and the mediant generate the minimum structure for physics.", color: "#ffd75c", group: "foundation", r: 12, url: "first-principles.html" },
  { id: "D0",  label: "D0",  title: "Recurrence Survival", claim: "Only recurrent configurations survive indefinite iteration.", color: "#ffd75c", group: "foundation", r: 12 },

  // Field Equation (blue)
  { id: "D11", label: "D11", title: "Rational Field Equation", claim: "Synchronization cost C(p/q) = 1/(q²·sin²(πp/q)) governs all coupling.", color: "#58a6ff", group: "field_eq", r: 11, url: "oscillations.html" },
  { id: "D14", label: "D14", title: "Three Dimensions", claim: "Three spatial dimensions emerge as the minimum for non-degenerate mediant geometry.", color: "#58a6ff", group: "field_eq", r: 11, url: "three-body.html" },
  { id: "D15", label: "D15", title: "Lie Group Characterization", claim: "The symmetry group of the rational field equation is SL(2,Z).", color: "#58a6ff", group: "field_eq", r: 11 },

  // Spacetime K=1 (green)
  { id: "D12", label: "D12", title: "Two Continuum Limits", claim: "The field equation has two limits: K→1 (gravity) and K<1 (quantum).", color: "#7ee787", group: "spacetime", r: 11 },
  { id: "D13", label: "D13", title: "Einstein from Kuramoto", claim: "The Einstein field equations emerge from Kuramoto synchronization at K=1.", color: "#7ee787", group: "spacetime", r: 11, url: "first-principles.html" },
  { id: "D16", label: "D16", title: "Variable Denominator", claim: "Variable denominator q(x) encodes local curvature as rational approximation depth.", color: "#7ee787", group: "spacetime", r: 10 },
  { id: "D17", label: "D17", title: "Rank-1 Temporal Causation", claim: "Time emerges as rank-1 causal ordering of synchronization updates.", color: "#7ee787", group: "spacetime", r: 10 },

  // Topology (purple)
  { id: "D18", label: "D18", title: "Möbius Container", claim: "The mediant's half-twist identifies p/q with (q−p)/q on a Möbius strip.", color: "#d2a8ff", group: "topology", r: 10 },
  { id: "D19", label: "D19", title: "Klein Bottle", claim: "Doubling the Möbius container produces the Klein bottle as the natural topology.", color: "#d2a8ff", group: "topology", r: 11 },
  { id: "D20", label: "D20", title: "XOR Continuum Limit", claim: "The discrete XOR gate has a continuum limit that reproduces quantum interference.", color: "#d2a8ff", group: "topology", r: 10 },
  { id: "D21", label: "D21", title: "Discrete Gauge", claim: "Gauge symmetry arises from the discrete ambiguity in Farey labeling.", color: "#d2a8ff", group: "topology", r: 10 },
  { id: "D23", label: "D23", title: "Three Zeros", claim: "The field equation has exactly three zeros, corresponding to three generations.", color: "#d2a8ff", group: "topology", r: 10 },

  // Cosmology (orange)
  { id: "D24", label: "D24", title: "Vacuum Energy", claim: "Klein bottle has exactly 4 surviving modes; cosmological constant problem dissolves.", color: "#ffa657", group: "cosmology", r: 10 },
  { id: "D25", label: "D25", title: "Farey Partition (Ω_Λ = 13/19)", claim: "Ω_Λ = |F_6|/(|F_6|+6) = 13/19 ≈ 0.6842 (observed 0.6847 ± 0.0073).", color: "#ffa657", group: "cosmology", r: 11 },
  { id: "D26", label: "D26", title: "Hierarchy", claim: "Planck/Hubble ratio R = 6 × 13^54 (residual 0.48%).", color: "#ffa657", group: "cosmology", r: 10 },
  { id: "D27", label: "D27", title: "Exponent", claim: "Exponent 54 = q₂ × q₃^d derived from spatial dimension and Klein bottle.", color: "#ffa657", group: "cosmology", r: 10 },
  { id: "D28", label: "D28", title: "Farey Proof", claim: "SO(2) structure at locked/unlocked boundary forces Farey counting.", color: "#ffa657", group: "cosmology", r: 10 },
  { id: "D47", label: "D47", title: "Baryon Fraction", claim: "Ω_b = 13/264, Ω_DM = 35/132 from two-component closure.", color: "#ffa657", group: "cosmology", r: 11 },

  // Extended Derivations (pink)
  { id: "D30", label: "D30", title: "Denomination Boundary", claim: "Devil's staircase in K-space is a brachistochrone; three open questions unified.", color: "#f5a9b8", group: "extended", r: 10 },
  { id: "D31", label: "D31", title: "Speed of Light", claim: "c as gate propagation speed of the coherent medium at K=1.", color: "#f5a9b8", group: "extended", r: 10 },
  { id: "D32", label: "D32", title: "Minkowski Signature", claim: "(3,1) signature from phase-state observability: 3 observable + 1 dark.", color: "#f5a9b8", group: "extended", r: 10 },
  { id: "D33", label: "D33", title: "Duty Cycle Dictionary", claim: "Coupling constants from Klein bottle duty cycles: sin²θ_W = 8/35.", color: "#f5a9b8", group: "extended", r: 10 },
  { id: "D34", label: "D34", title: "Generation Mechanism", claim: "Three generations from phase-state observability at Stern-Brocot depth.", color: "#f5a9b8", group: "extended", r: 10 },
  { id: "D35", label: "D35", title: "Cosmological Cycle", claim: "Two-voice round in 13/19: gap-twin at 18.7% spacetime duty.", color: "#f5a9b8", group: "extended", r: 10 },
  { id: "D36", label: "D36", title: "Conservation as Computability", claim: "S^1 compact → |r| ≤ 1 → K_eff ≤ 1 → circle map invertible → information conserved.", color: "#f5a9b8", group: "extended", r: 10 },
  { id: "D37", label: "D37", title: "Figure-Eight Topology", claim: "Klein bottle self-intersection = lemniscate; sin²θ_W = 8/35 is crossing probability.", color: "#f5a9b8", group: "extended", r: 10 },
  { id: "D38", label: "D38", title: "Boundary Weight", claim: "Ω_Λ(w) = (11+2w)/(16+3w); w* = 0.83 at K* = 0.862.", color: "#f5a9b8", group: "extended", r: 10 },
  { id: "D39", label: "D39", title: "Half-Möbius Boundary", claim: "Z_4 boundary condition from half-Möbius strip.", color: "#d2a8ff", group: "topology", r: 10 },
  { id: "D40", label: "D40", title: "Stribeck Vortex", claim: "Vortex regime map: overcritical core (K>1) + subcritical annulus (K<1).", color: "#f5a9b8", group: "extended", r: 10 },

  // Gauge Sector (coral)
  { id: "D41", label: "D41", title: "Discrete Gauge Resolution", claim: "Gauge structure is discrete: charges, center Z_6, confinement from XOR.", color: "#ff7b72", group: "gauge", r: 11 },
  { id: "D42", label: "D42", title: "Gauge-Sector Lovelock", claim: "SU(3) × SU(2) × U(1) → Yang-Mills uniquely via Utiyama + Cartan.", color: "#ff7b72", group: "gauge", r: 11 },
  { id: "D43", label: "D43", title: "Gell-Mann–Nishijima", claim: "Q = T_3 + Y/2 derived from Klein bottle identification geometry.", color: "#ff7b72", group: "gauge", r: 10 },
  { id: "D44", label: "D44", title: "Higgs from Tongue Boundary", claim: "Higgs doublet is tongue boundary mode of open q=2 fiber.", color: "#ff7b72", group: "gauge", r: 11 },
  { id: "D45", label: "D45", title: "Coupling Scales", claim: "D_0 = 1/2 from tree geometry; all dimensionless ratios determined; θ = 0.", color: "#ff7b72", group: "gauge", r: 10 },

  // ADM dictionary (spacetime)
  { id: "D46", label: "D46", title: "ADM Dictionary", claim: "Each ADM entry uniquely identified by K=1 Kuramoto symmetries.", color: "#7ee787", group: "spacetime", r: 10 },

  // Predictions (cyan)
  { id: "D1", label: "D1",  title: "Born Rule", claim: "Born's probability rule |ψ|² emerges as basin measure of synchronization.", color: "#79c0ff", group: "predictions", r: 11, url: "constants.html" },
  { id: "D4", label: "D4",  title: "Spectral Tilt", claim: "CMB spectral tilt nₛ from mode-locking statistics on the Stern-Brocot tree.", color: "#79c0ff", group: "predictions", r: 10, url: "constants.html" },
  { id: "D5", label: "D5",  title: "Two Forces", claim: "Only two long-range forces (gravity + EM) survive the synchronization filter.", color: "#79c0ff", group: "predictions", r: 10 },
  { id: "D6", label: "D6",  title: "Planck Scale", claim: "Planck length as the self-sustaining synchronization threshold.", color: "#79c0ff", group: "predictions", r: 10 },
  { id: "D7", label: "D7",  title: "Measurement Collapse", claim: "Wavefunction collapse as tongue traversal in the Arnold tongue diagram.", color: "#79c0ff", group: "predictions", r: 10 },
  { id: "D8", label: "D8",  title: "High-z MOND", claim: "MOND acceleration a₀ varies with redshift: a₀(z) = a₀(0)·(1+z)^β.", color: "#79c0ff", group: "predictions", r: 10, url: "our_address.html" },
  { id: "D9", label: "D9",  title: "Fidelity Bound", claim: "Self-referential bound: the framework must predict its own derivability.", color: "#79c0ff", group: "predictions", r: 11 },

  // Prior Work (dim white)
  { id: "D3",  label: "D3",  title: "a₀ Threshold", claim: "MOND acceleration a₀ derived from the synchronization cost threshold.", color: "#8b949e", group: "prior", r: 10, url: "our_address.html" },
  { id: "D22", label: "D22", title: "Engineering Targets", claim: "Experimental targets and engineering implications of the framework.", color: "#8b949e", group: "prior", r: 10 },

  // Repositories (larger, white border)
  { id: "proslambenomenos", label: "proslambenomenos", title: "proslambenomenos", claim: "Original derivation monograph — the added tone.", url: "https://nickjoven.github.io/proslambenomenos/", color: "#e6edf3", group: "repo", r: 18, isRepo: true },
  { id: "201", label: "201", title: "201", claim: "Einstein field equation reading and companion material.", url: "https://nickjoven.github.io/201/", color: "#e6edf3", group: "repo", r: 16, isRepo: true },
  { id: "intersections", label: "intersections", title: "intersections", claim: "Born rule substrate and stick-slip dynamics.", url: "https://nickjoven.github.io/intersections/", color: "#e6edf3", group: "repo", r: 16, isRepo: true },
  { id: "harmonics", label: "harmonics", title: "harmonics", claim: "Contains all derivations, GIF animations, and interactive HTML apps.", url: "https://github.com/nickjoven/harmonics", color: "#e6edf3", group: "repo", r: 20, isRepo: true },
  { id: "rfe", label: "rfe", title: "rfe", claim: "Rational field equation solver and numerical tools.", url: "https://github.com/nickjoven/rfe", color: "#e6edf3", group: "repo", r: 14, isRepo: true },
  { id: "stribeck-optics", label: "stribeck-optics", title: "stribeck-optics", claim: "Physical analogue — Stribeck curve optics experiments.", url: "https://github.com/nickjoven/stribeck-optics", color: "#e6edf3", group: "repo", r: 14, isRepo: true },
  { id: "product", label: "product", title: "product", claim: "Product-facing repository.", url: "https://github.com/nickjoven/product", color: "#e6edf3", group: "repo", r: 14, isRepo: true },

  // Media assets (small dots)
  { id: "gif_stairs",     label: "stairs",     title: "stairs.gif", claim: "Staircase animation of Farey mediant convergence.", color: "#484f58", group: "media", r: 4, parent: "harmonics" },
  { id: "gif_triangles",  label: "triangles",  title: "triangles.gif", claim: "Triangle animation of three-oscillator coupling.", color: "#484f58", group: "media", r: 4, parent: "harmonics" },
  { id: "gif_orbit",      label: "orbit",      title: "orbit.gif", claim: "Orbital animation of synchronization dynamics.", color: "#484f58", group: "media", r: 4, parent: "harmonics" },
  { id: "gif_spiral",     label: "spiral",     title: "spiral.gif", claim: "Spiral animation of Stern-Brocot descent.", color: "#484f58", group: "media", r: 4, parent: "harmonics" },
  { id: "gif_rose",       label: "rose",       title: "rose.gif", claim: "Rose curve animation of mode-locked harmonics.", color: "#484f58", group: "media", r: 4, parent: "harmonics" },
  { id: "app_sb_walk",    label: "stern_brocot_walk", title: "Stern-Brocot Walk", claim: "Interactive walk on the Stern-Brocot tree.", color: "#484f58", group: "media", r: 5, parent: "harmonics" },
  { id: "app_ontology",   label: "ontology",   title: "Ontology Viewer", claim: "Interactive ontology of the derivation chain.", color: "#484f58", group: "media", r: 5, parent: "harmonics" },
  { id: "app_mobius",     label: "mobius_views", title: "Möbius Views", claim: "Interactive Möbius strip visualizations.", color: "#484f58", group: "media", r: 5, parent: "harmonics" },
  { id: "app_projector",  label: "mobius_projector", title: "Möbius Projector", claim: "Möbius strip projection tool.", color: "#484f58", group: "media", r: 5, parent: "harmonics" },
  { id: "app_address",    label: "our_address", title: "Our Address", claim: "Interactive Farey address locator.", color: "#484f58", group: "media", r: 5, parent: "harmonics" },
  { id: "nb_quantum_stribeck", label: "quantum_stribeck", title: "quantum_stribeck.ipynb", claim: "Quantum Stribeck curve notebook.", color: "#484f58", group: "media", r: 5, parent: "201" },
  { id: "nb_stick_slip",  label: "stick_slip_lagrangian", title: "stick_slip_lagrangian.ipynb", claim: "Stick-slip Lagrangian mechanics notebook.", color: "#484f58", group: "media", r: 5, parent: "intersections" },
  { id: "nb_phase",       label: "phase_portrait", title: "phase_portrait.ipynb", claim: "Phase portrait analysis notebook.", color: "#484f58", group: "media", r: 5, parent: "proslambenomenos" },
];

// Dependency edges (derivation chain)
const depEdges = [
  ["D0",  "D29"], ["D1",  "D10"], ["D3",  "D9"],  ["D3",  "D11"],
  ["D4",  "D10"], ["D5",  "D10"], ["D6",  "D10"], ["D6",  "D14"],
  ["D7",  "D1"],  ["D7",  "D10"], ["D8",  "D3"],  ["D8",  "D9"],
  ["D9",  "D0"],  ["D9",  "D1"],  ["D9",  "D7"],  ["D9",  "D10"],
  ["D9",  "D11"], ["D10", "D29"], ["D11", "D10"], ["D12", "D11"],
  ["D12", "D14"], ["D13", "D11"], ["D13", "D12"], ["D14", "D10"],
  ["D14", "D11"], ["D15", "D14"], ["D16", "D11"], ["D17", "D16"],
  ["D18", "D14"], ["D19", "D18"], ["D20", "D19"], ["D21", "D20"],
  ["D22", "D3"],  ["D22", "D6"],  ["D22", "D8"],  ["D23", "D19"],
  ["D24", "D19"], ["D25", "D19"], ["D25", "D28"], ["D26", "D25"],
  ["D26", "D27"], ["D27", "D14"], ["D27", "D19"], ["D28", "D19"],
  ["D28", "D11"],
  // Extended derivations (D30–D40)
  ["D30", "D19"], ["D30", "D11"],
  ["D31", "D11"], ["D31", "D14"], ["D31", "D17"],
  ["D32", "D14"], ["D32", "D19"],
  ["D33", "D19"],
  ["D34", "D10"], ["D34", "D14"], ["D34", "D19"],
  ["D35", "D19"], ["D35", "D25"],
  ["D36", "D10"], ["D36", "D11"],
  ["D37", "D19"], ["D37", "D32"],
  ["D38", "D25"], ["D38", "D19"],
  ["D39", "D18"],
  ["D40", "D11"], ["D40", "D36"],
  // Gauge sector (D41–D45)
  ["D41", "D20"], ["D41", "D21"],
  ["D42", "D41"], ["D42", "D14"], ["D42", "D13"],
  ["D43", "D42"], ["D43", "D19"],
  ["D44", "D1"],  ["D44", "D43"], ["D44", "D19"],
  ["D45", "D44"], ["D45", "D33"],
  // ADM dictionary (D46)
  ["D46", "D12"], ["D46", "D13"],
  // Baryon fraction (D47)
  ["D47", "D25"], ["D47", "D19"],
];

// Cross-repo edges (dashed)
const crossEdges = [
  ["proslambenomenos", "D3"],  ["proslambenomenos", "D9"],
  ["201", "D13"], ["201", "intersections"],
  ["intersections", "D1"], ["rfe", "D11"],
  ["stribeck-optics", "intersections"],
  ["harmonics", "D29"], ["harmonics", "D10"], ["harmonics", "D11"],
  ["harmonics", "D14"], ["harmonics", "D19"],
];

// Media parent edges
const mediaEdges = derivations
  .filter(d => d.parent)
  .map(d => [d.id, d.parent]);

// Build links array
const links = [
  ...depEdges.map(([s, t]) => ({ source: s, target: t, type: "dep" })),
  ...crossEdges.map(([s, t]) => ({ source: s, target: t, type: "cross" })),
  ...mediaEdges.map(([s, t]) => ({ source: s, target: t, type: "media" })),
];

// ─── Render ──────────────────────────────────────────────────────────────────

const container = document.getElementById("graph-container");
const svg = d3.select("#graph-svg");
const tooltip = document.getElementById("graph-tooltip");
const tooltipTitle = document.getElementById("tooltip-title");
const tooltipClaim = document.getElementById("tooltip-claim");

const width = container.clientWidth;
const height = container.clientHeight;

// Glow filter
const defs = svg.append("defs");

// Radial gradient for background ambiance
const bgGrad = defs.append("radialGradient")
  .attr("id", "bg-glow")
  .attr("cx", "50%").attr("cy", "50%").attr("r", "50%");
bgGrad.append("stop").attr("offset", "0%").attr("stop-color", "#161b22");
bgGrad.append("stop").attr("offset", "100%").attr("stop-color", "#0d1117");

svg.append("rect")
  .attr("width", width)
  .attr("height", height)
  .attr("fill", "url(#bg-glow)");

// Glow filters per group color
const glowColors = {
  foundation: "#ffd75c",
  field_eq: "#58a6ff",
  spacetime: "#7ee787",
  topology: "#d2a8ff",
  cosmology: "#ffa657",
  extended: "#f5a9b8",
  gauge: "#ff7b72",
  predictions: "#79c0ff",
  prior: "#8b949e",
  repo: "#e6edf3",
  media: "#484f58"
};

Object.entries(glowColors).forEach(([group, color]) => {
  const filter = defs.append("filter")
    .attr("id", `glow-${group}`)
    .attr("x", "-50%").attr("y", "-50%")
    .attr("width", "200%").attr("height", "200%");
  filter.append("feGaussianBlur")
    .attr("in", "SourceGraphic")
    .attr("stdDeviation", group === "media" ? 1 : 3)
    .attr("result", "blur");
  filter.append("feColorMatrix")
    .attr("in", "blur")
    .attr("type", "matrix")
    .attr("values", `0 0 0 0 ${parseInt(color.slice(1,3),16)/255} 0 0 0 0 ${parseInt(color.slice(3,5),16)/255} 0 0 0 0 ${parseInt(color.slice(5,7),16)/255} 0 0 0 0.4 0`);
  const merge = filter.append("feMerge");
  merge.append("feMergeNode");
  merge.append("feMergeNode").attr("in", "SourceGraphic");
});

// Zoom behavior
const g = svg.append("g");
const zoom = d3.zoom()
  .scaleExtent([0.2, 4])
  .on("zoom", (event) => g.attr("transform", event.transform));
svg.call(zoom);

// Center initial view
svg.call(zoom.transform, d3.zoomIdentity.translate(width / 2, height / 2).scale(0.85).translate(-width / 2, -height / 2));

// Simulation
const simulation = d3.forceSimulation(derivations)
  .force("link", d3.forceLink(links).id(d => d.id).distance(d => {
    if (d.type === "media") return 40;
    if (d.type === "cross") return 180;
    return 100;
  }).strength(d => {
    if (d.type === "media") return 0.8;
    if (d.type === "cross") return 0.15;
    return 0.3;
  }))
  .force("charge", d3.forceManyBody()
    .strength(d => {
      if (d.group === "media") return -30;
      if (d.isRepo) return -400;
      return -200;
    })
  )
  .force("center", d3.forceCenter(width / 2, height / 2).strength(0.05))
  .force("collision", d3.forceCollide().radius(d => d.r + 8))
  .force("x", d3.forceX(width / 2).strength(0.02))
  .force("y", d3.forceY(height / 2).strength(0.02))
  .alphaDecay(0.01)
  .velocityDecay(0.3);

// Draw links
const link = g.append("g")
  .selectAll("line")
  .data(links)
  .join("line")
  .attr("stroke", d => {
    if (d.type === "media") return "#21262d";
    if (d.type === "cross") return "#30363d";
    return "#30363d";
  })
  .attr("stroke-width", d => {
    if (d.type === "media") return 0.5;
    if (d.type === "cross") return 1;
    return 1.2;
  })
  .attr("stroke-dasharray", d => d.type === "cross" ? "4,4" : d.type === "media" ? "2,3" : "none")
  .attr("stroke-opacity", d => {
    if (d.type === "media") return 0.3;
    if (d.type === "cross") return 0.4;
    return 0.5;
  });

// Arrow markers for dependency edges
defs.append("marker")
  .attr("id", "arrowhead")
  .attr("viewBox", "0 -3 6 6")
  .attr("refX", 12)
  .attr("refY", 0)
  .attr("markerWidth", 5)
  .attr("markerHeight", 5)
  .attr("orient", "auto")
  .append("path")
  .attr("d", "M0,-3L6,0L0,3")
  .attr("fill", "#30363d")
  .attr("fill-opacity", 0.5);

link.filter(d => d.type === "dep")
  .attr("marker-end", "url(#arrowhead)");

// Draw nodes
const node = g.append("g")
  .selectAll("g")
  .data(derivations)
  .join("g")
  .attr("cursor", "pointer")
  .call(d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended)
  );

// Node circles
node.append("circle")
  .attr("r", d => d.r)
  .attr("fill", d => {
    if (d.isRepo) return "#0d1117";
    if (d.group === "media") return d.color;
    return d.color;
  })
  .attr("fill-opacity", d => {
    if (d.group === "media") return 0.5;
    return 0.85;
  })
  .attr("stroke", d => {
    if (d.isRepo) return "#e6edf3";
    return d.color;
  })
  .attr("stroke-width", d => {
    if (d.isRepo) return 2.5;
    if (d.group === "media") return 0;
    return 1;
  })
  .attr("stroke-opacity", d => d.isRepo ? 0.8 : 0.3)
  .attr("filter", d => `url(#glow-${d.group})`);

// Repo icon circles — inner ring
node.filter(d => d.isRepo)
  .append("circle")
  .attr("r", d => d.r - 5)
  .attr("fill", "none")
  .attr("stroke", "#e6edf3")
  .attr("stroke-width", 0.5)
  .attr("stroke-opacity", 0.3);

// Labels
node.filter(d => d.group !== "media")
  .append("text")
  .text(d => d.label)
  .attr("text-anchor", "middle")
  .attr("dy", d => d.r + 14)
  .attr("fill", d => d.color)
  .attr("fill-opacity", 0.7)
  .attr("font-size", d => d.isRepo ? "11px" : "9px")
  .attr("font-weight", d => d.isRepo ? 600 : 400)
  .attr("font-family", "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif")
  .attr("pointer-events", "none");

// Hover and click
node.on("mouseover", function(event, d) {
    tooltipTitle.textContent = d.title;
    tooltipClaim.textContent = d.claim;
    tooltip.style.display = "block";

    d3.select(this).select("circle")
      .transition().duration(200)
      .attr("fill-opacity", 1)
      .attr("stroke-opacity", 1)
      .attr("r", d.r * 1.2);

    // Highlight connected links
    link.transition().duration(200)
      .attr("stroke-opacity", l => {
        if (l.source.id === d.id || l.target.id === d.id) return 0.9;
        return 0.1;
      })
      .attr("stroke", l => {
        if (l.source.id === d.id || l.target.id === d.id) return d.color;
        return l.type === "media" ? "#21262d" : "#30363d";
      });
  })
  .on("mousemove", function(event) {
    const rect = container.getBoundingClientRect();
    tooltip.style.left = (event.clientX - rect.left + 16) + "px";
    tooltip.style.top = (event.clientY - rect.top - 10) + "px";
  })
  .on("mouseout", function(event, d) {
    tooltip.style.display = "none";

    d3.select(this).select("circle")
      .transition().duration(300)
      .attr("fill-opacity", d.group === "media" ? 0.5 : 0.85)
      .attr("stroke-opacity", d.isRepo ? 0.8 : 0.3)
      .attr("r", d.r);

    link.transition().duration(300)
      .attr("stroke-opacity", l => {
        if (l.type === "media") return 0.3;
        if (l.type === "cross") return 0.4;
        return 0.5;
      })
      .attr("stroke", l => {
        if (l.type === "media") return "#21262d";
        return "#30363d";
      });
  })
  .on("click", function(event, d) {
    if (d.url) {
      window.open(d.url, "_blank");
    }
  });

// Simulation tick
simulation.on("tick", () => {
  link
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y);

  node.attr("transform", d => `translate(${d.x},${d.y})`);
});

// Drag functions
function dragstarted(event, d) {
  if (!event.active) simulation.alphaTarget(0.1).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(event, d) {
  d.fx = event.x;
  d.fy = event.y;
}

function dragended(event, d) {
  if (!event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

// Gentle initial warmup — let it settle slowly
simulation.alpha(1).restart();

// Responsive resize
window.addEventListener("resize", () => {
  const w = container.clientWidth;
  const h = container.clientHeight;
  svg.select("rect").attr("width", w).attr("height", h);
  simulation.force("center", d3.forceCenter(w / 2, h / 2).strength(0.05));
  simulation.force("x", d3.forceX(w / 2).strength(0.02));
  simulation.force("y", d3.forceY(h / 2).strength(0.02));
  simulation.alpha(0.3).restart();
});

})();
</script>
```
