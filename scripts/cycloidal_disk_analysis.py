"""
Cycloidal Drive Analysis Script
================================
Enter geometry and load parameters below. The script evaluates all materials
from the table for pin-hole Hertzian contact and eccentric bearing load.
"""

import math

# =============================================================================
# INPUT PARAMETERS — edit these
# =============================================================================

# Transmission
# Motor L, updated 20:1 -> 19:1 reduction
N_l = 19            # number of lobes on cycloidal disk
N_p = N_l + 1       # number of pins in outer ring (usually N_l + 1)

# Geometry [mm]
R_p       = 50.0    # Ring pin circle radius
R_r       = 5.0     # pin radius (ring gear pins) -- table value
b_contact = 20.0    # pin contact length (axial / effective) -- assumed = disk height h_disk, not separately documented
e         = 2.25     # eccentricity [mm]
R_hole    = R_r + e # hole radius in cycloidal disk (must be > R_pin)

# Output shaft pins
# Mechanism: oversized holes in the disk, pins fixed to the output shaft,
# hole oversize tied to eccentricity e -- same convex-concave contact as the
# ring pins, just on the output side.
N_out       = 8       # number of output shaft pins
R_out       = 30.0    # output shaft pin circle radius [mm] (lever arm, used in F_out_max)
R_out_pin   = 4.0     # physical radius of the output shaft pins themselves [mm]
R_hole_out  = R_out_pin + e   # oversized disk hole radius for the output pin

# Load
T_out = 60000.0     # output torque [N·mm]  (60 Nm)

# Pressure angle [deg] — read from simulator for your geometry
# NOT re-measured for the new 19-lobe geometry: the mevirtuoso.com pressure-angle
# simulator is a paid "Premium" feature, not freely accessible. Carrying forward
# the old 20:1 values (K1 = e*N_p/R_p shifts only 0.945 -> 0.900, ~5%) as a rough
# placeholder -- verify against the real simulator/FEA before trusting these.
alpha_min_deg = 20   # minimum pressure angle in load-bearing region
alpha_deg     = 51   # representative / working pressure angle

# Friction coefficient (disk–pin contact)
mu = 0.10

# Eccentric bearing safety factor
K_bearing = 2.0

# Hertzian allowable multipliers (static / repeated)
HERTZ_STATIC_FACTOR   = 1.6   # p_max ≤ factor × σ_y  (static)
HERTZ_REPEATED_FACTOR = 1.0   # p_max ≤ factor × σ_y  (repeated / rolling)
LOAD_TYPE = "repeated"          # "static" or "repeated"

# Safety factor on σ_y for yield check (non-Hertzian)
SF_yield = 2.0

# =============================================================================
# MATERIAL TABLE
# (name, E [MPa], nu, sigma_y [MPa or None], UTS [MPa or None], is_polymer)
# =============================================================================

# Pin material (body 1) — Steel
E_pin  = 210_000.0
nu_pin = 0.30

MATERIALS = [
    # name,                          E [MPa],  nu,   σ_y [MPa], UTS [MPa], polymer?
    ("Steel (pin ref., ~hardened)",  210_000,  0.30,  1000,       None,     False),
    ("Stainless 303/304 (annealed)", 193_000,  0.29,   215,        550,     False),
    ("Mild steel S235JR",            210_000,  0.30,   235,        360,     False),
    ("42CrMo4 Q&T (~900 HB-ish)",     210_000,  0.30,   900,       1100,     False),
    ("Nylon 12 Tough (SLS)",           1_450,  0.40,  None,         42,     True ),
    ("Cast PA6 (dry)",                 3_000,  0.39,    65,       None,     True ),
    ("Cast PA6 (humid)",               1_000,  0.39,    45,       None,     True ),
    ("POM",                            2_700,  0.39,    66,       None,     True ),
    ("PLA",                            3_120,  0.39,    70,       None,     True ),
    ("EN AW-5083 (AlMg4.5Mn0.7)",     70_000,  0.33,   145,        270,     False),
    ("EN AW-6060 T66 (AlMgSi0.5)",    70_000,  0.33,   160,        215,     False),
    ("EN AW-2007 T3 (AlCu4PbMgMn)",   70_000,  0.33,   300,        370,     False),
]

# =============================================================================
# CALCULATIONS
# =============================================================================

def effective_modulus(E1, nu1, E2, nu2):
    """Reduced contact modulus E* for two dissimilar materials."""
    return (E1 * E2) / (E2 * (1 - nu1**2) + E1 * (1 - nu2**2))

def hertz_line_pressure(F, E_star, R_eq, b):
    """Maximum Hertzian contact pressure [MPa] for line contact."""
    return math.sqrt((F * E_star) / (math.pi * b * R_eq))

def forward_efficiency(alpha_rad, mu):
    return 1.0 / (1.0 + mu * math.tan(alpha_rad))

def backdrive_efficiency(alpha_rad, mu):
    tan_a = math.tan(alpha_rad)
    if tan_a == 0:
        return 0.0
    return 1.0 / (1.0 + mu / tan_a)

# --- Transmission ---
i = N_l / (N_p - N_l)

# --- Engaged pins ---
N_eff = N_p / 4.0

# --- Angles ---
alpha_min = math.radians(alpha_min_deg)
alpha     = math.radians(alpha_deg)

# --- Forces ---
F_pin_max  = (2 * T_out) / (N_eff * R_p * math.cos(alpha_min))
F_out_max  = (4 * T_out) / (N_out * R_out)
F_bearing  = K_bearing * T_out / (i * e)

# --- Equivalent radius (convex pin in concave hole) ---
R_eq     = (R_r * R_hole) / (R_hole - R_r)               # ring pin <-> disk hole
R_eq_out = (R_out_pin * R_hole_out) / (R_hole_out - R_out_pin)  # output pin <-> disk hole

# --- Efficiencies ---
eta_fwd  = forward_efficiency(alpha, mu)
eta_back = backdrive_efficiency(alpha, mu)

hertz_factor = HERTZ_STATIC_FACTOR if LOAD_TYPE == "static" else HERTZ_REPEATED_FACTOR

# =============================================================================
# OUTPUT
# =============================================================================

SEP  = "=" * 72
sep  = "-" * 72

print(SEP)
print("  CYCLOIDAL DRIVE — ANALYSIS SUMMARY")
print(SEP)

print(f"\n{'TRANSMISSION':}")
print(f"  Lobes N_l = {N_l},  Pins N_p = {N_p}")
print(f"  Ratio i   = {i:.4f}  ({N_l}:{int(N_p - N_l)})")

print(f"\nEFFICIENCY  (α = {alpha_deg}°, μ = {mu})")
print(f"  Forward   η_fwd  = {eta_fwd*100:.1f}%")
print(f"  Backdrive η_back = {eta_back*100:.1f}%")
if eta_back > 0.5:
    print("  → Backdriveable (η_back > 50%)")
else:
    print("  → Self-locking tendency (η_back ≤ 50%)")

print(f"\n{'FORCE SUMMARY':}")
print(f"  Output torque          T_out      = {T_out:.1f} N·mm")
print(f"  Effective engaged pins N_eff      = {N_eff:.1f}")
print(f"  Max ring pin force     F_pin_max  = {F_pin_max:.1f} N  (α_min={alpha_min_deg}°, peak factor=2)")
print(f"  Max output pin force   F_out_max  = {F_out_max:.1f} N")
print(f"  Eccentric bearing load F_bearing  = {F_bearing:.1f} N  (K={K_bearing})")

print(f"\n{'HERTZIAN GEOMETRY':}")
print(f"  Ring pin:   R_pin = {R_r:.2f} mm,  R_hole = {R_hole:.2f} mm,  R_eq = {R_eq:.3f} mm")
print(f"  Output pin: R_pin = {R_out_pin:.2f} mm,  R_hole = {R_hole_out:.2f} mm,  R_eq = {R_eq_out:.3f} mm  (F_out_max = {F_out_max:.1f} N)")
print(f"  b       = {b_contact:.1f} mm  (contact length)")
print(f"  Load    = {LOAD_TYPE}  → allowable multiplier = {hertz_factor}×σ_y")

print(f"\n{SEP}")
print(f"  MATERIAL EVALUATION  (disk, paired with steel pins)")
print(f"  Ring pin force F_pin_max = {F_pin_max:.1f} N   Output pin force F_out_max = {F_out_max:.1f} N")
print(SEP)

header = (
    f"  {'Material':<30} {'E* [MPa]':>10} {'p_p_max [MPa]':>12} {'p_p_max,eq [MPa]':>14} {'p_output [MPa]':>13} "
    f"{'p_max [MPa]':>12} {'Allow. [MPa]':>14} {'Status':>8}"
)
print(header)
print(f"  {sep}")

for name, E2, nu2, sig_y, UTS, is_polymer in MATERIALS:
    E_star = effective_modulus(E_pin, nu_pin, E2, nu2)
    # Ring pin <-> disk hole, conservative (flat) idealization -- matches the
    # original doc's "p_p,max"
    p_p_max      = hertz_line_pressure(F_pin_max, E_star, R_r, b_contact)
    # Ring pin <-> disk hole, concave-corrected idealization -- this is what the
    # original script/doc actually computed as "p_out,max"; it's still the RING
    # pin, just a more generous estimate crediting the hole's concave curvature.
    p_p_max_eq   = hertz_line_pressure(F_pin_max, E_star, R_eq, b_contact)
    # Genuinely separate output pin <-> disk hole contact (new; wasn't modeled before)
    p_output_pin = hertz_line_pressure(F_out_max, E_star, R_eq_out, b_contact)
    p_max = max(p_p_max, p_output_pin)  # p_p_max_eq is never the worst case (R_eq > R_r always)

    # Determine allowable
    if sig_y is not None and UTS is not None:
        allowable_val  = min(sig_y, UTS) if is_polymer else sig_y
        allowable_base = "min(σ_y,UTS)" if is_polymer else "σ_y"
    elif sig_y is not None:
        allowable_val  = sig_y
        allowable_base = "σ_y"
    elif UTS is not None:
        allowable_val  = UTS
        allowable_base = "UTS"
    else:
        # No strength data (e.g. steel pin reference)
        print(f"  {name:<30} {E_star:>10.0f} {p_max:>12.1f} {'—':>14} {'N/A':>8}")
        continue

    hertz_allow = hertz_factor * allowable_val

    if p_max <= hertz_allow:
        status = "OK"
        flag   = ""
    elif p_max <= hertz_allow * 1.25:
        status = "MARGINAL"
        flag   = " !"
    else:
        status = "FAIL"
        flag   = " !!"

    print(
        f"  {name:<30} {E_star:>10.0f} {p_p_max:>12.1f} {p_p_max_eq:>14.1f} {p_output_pin:>13.1f} "
        f"{p_max:>12.1f} {hertz_allow:>14.1f} {status:>8}{flag}"
    )
    # print(
    #     f"  {'':30} {'':10} {'':12} "
    #     f"  ({hertz_factor}×{allowable_base}={hertz_allow:.1f})"
    # )

print(SEP)
print(f"\nNotes:")
print(f"  • E* computed as E_pin={E_pin/1000:.0f} GPa (steel) paired with disk material.")
print(f"  • Hertz allowable = {hertz_factor} × reference strength ({LOAD_TYPE} load).")
print(f"  • p_p_max (flat) and p_p_max,eq (concave-corrected) are both the RING pin, using F_pin_max; p_p_max,eq matches the original doc's 'p_out,max' label.")
print(f"  • p_output is the genuinely separate OUTPUT pin <-> disk-hole contact, using F_out_max and R_eq_out. p_max is the worse of p_p_max and p_output.")
print(f"  • Polymers: creep and temperature effects NOT captured here.")
print(f"  • Bearing load F_bearing = {F_bearing:.1f} N → check bearing datasheet separately.")
print()