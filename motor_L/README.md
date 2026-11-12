# Motor L

Author: Tobias Reich
Related: [Cycloidal Drive](../docs/cycloidal-drive.md)

## Dimensions

### Cycloidal drive

See [Cycloidal Drive](../docs/cycloidal-drive.md) for the full explanation of all calculations. [`scripts/cycloidal_disk_analysis.py`](../scripts/cycloidal_disk_analysis.py) does most of the calculations for you — it's currently set up with this motor's 19:1 parameters, $R_r=5$mm (ring) and $R_{r,out}=4$mm (output), the run behind the Derived Parameters table below.

#### Validation list

> Unchecked pending re-validation against the recomputed 19:1 loads below — the previous checkmarks were for the 20:1 geometry and no longer apply as-is.

- [ ] Disk material must hold up to $p_{p,max}$ and $p_{output}$ — **PA6 (dry) is marginal, see note below**
- [ ] Input shaft must hold up to $F_{bearing,max}$ (Fusion 360 study)
- [ ] Bearing must hold up to $F_{bearing,max}$
- [ ] Output shaft pin contacts must hold up to $F_{out,max}$
- [ ] Housing pin contacts must hold up to $F_{p,max}$

#### Requirements

- **Target ratio (i):** $19:1$
- **Nominal output torque:** $60\,Nm$

#### Core geometry

| Symbol      | Param                                | Value        | Unit | Notes            |
| ----------- | ------------------------------------- | ------------ | ---- | ---------------- |
| $N_l$       | Number of lobes (cycloid disc teeth)  | 19           | -    |                  |
| $N_p$       | Number of ring pins                   | $N_l + 1$    | -    | Always lobes + 1 |
| $N_{out}$   | Number of output shaft pins           | 8            | -    |                  |
| $R_p$       | Ring pin circle radius                | 50.0         | mm   |                  |
| $R_{out}$   | Output shaft pin circle radius        | 30.0         | mm   | Lever arm, used in $F_{out,max}$ |
| $R_r$       | Ring pin radius                        | 5.0          | mm   | Roller radius (table value)     |
| $R_{r,out}$ | Output shaft pin radius (physical)    | 4.0          | mm   | Distinct from $R_{out}$ above — see Derived Parameters |
| $e$         | Eccentricity                          | 2.25         | mm   |                  |
| $h_{disk}$  | Disk height                           | 20.0         | mm   |                  |

Cycloidal disk profile (parametric, $t$ in radians):

```
((50.0)*cos(t))-(4*cos(t+arctan(sin((1-20)*t)/(((50.0)/(2.25*20))-cos((1-20)*t)))))-(2.25*cos(20*t))

(-(50.0)*sin(t))+(4*sin(t+arctan(sin((1-20)*t)/(((50.0)/(2.25*20))-cos((1-20)*t)))))+(2.25*sin(20*t))
```

> Note: this formula's roller-offset term is hardcoded to `4`, not $R_r=5.0$mm — a pre-existing inconsistency in the source docs that's still unresolved (it doesn't appear to be $R_{r,out}$ either, since this curve is the ring-pin lobe profile, not the output coupling). Flagging rather than guessing again.

#### Materials

| Part         | Material              |
| ------------ | ---------------------- |
| Disk         | PA6                     |
| Input shaft  | Nylon 12 Tough (SLS)    |
| Output shaft | Nylon 12 Tough (SLS)    |
| Housing      | Nylon 12 Tough (SLS)    |

#### Derived parameters

Recomputed via `scripts/cycloidal_disk_analysis.py` for the new $19:1$ geometry ($N_l=19$, $N_p=20$, $R_p=50.0$mm, $R_r=5.0$mm, $R_{r,out}=4.0$mm, $e=2.25$mm, $N_{out}=8$, $R_{out}=30.0$mm, $T_{out}=60$Nm, $\mu=0.1$, bearing safety factor $K=2$).

The script now models **two genuinely separate Hertz contacts** instead of one: the ring pin against its disk hole ($p_{p,max}$, using $F_{p,max}$ and $R_r$), and the output pin against *its own* disk hole ($p_{output}$, using $F_{out,max}$ and $R_{r,out}$) — both the same convex-concave pin-in-oversized-hole mechanism, with the output hole's oversize likewise tied to $e$. Earlier drafts of this table conflated the two (reusing the ring pin's force for a formula that only changed the radius), which overstated or understated the output pin check depending on the radius chosen — this version keeps them independent.

> **Assumptions carried into this run — verify before treating any status below as final:**
> - $\alpha_{min}$ and $\alpha_{avrg}$ are **carried forward unchanged from the old $20:1$ geometry**, not re-measured. The mevirtuoso.com pressure-angle simulator linked in the original docs turned out to be a paid "Premium" membership feature, not a free tool, so it wasn't used. Pressure angle is governed by $K_1 = e \cdot N_p / R_p$, which only shifts from $0.945$ (old) to $0.900$ (new, ~5%), so carrying the old values forward is a reasonable approximation — but get a real reading (simulator or FEA) before signing off.
> - $b_{contact}$ (axial pin contact length) is assumed equal to disk height $h_{disk}=20$mm — this isn't separately documented anywhere.
> - $N_{eff}$ for $F_{p,max}$ dropped slightly (5.25 → 5.0) because one fewer pin pitch is in the load-bearing region, which alone increases ring contact force ~5% independent of the pressure-angle assumption above.

| Symbol            | Param                                              | Old (20:1) | New (19:1) | Unit | Notes                                                   |
| ----------------- | --------------------------------------------------- | ------- | ------- | ---- | -------------------------------------------------------- |
| $\alpha_{min}$    | Minimum pressure angle                              | 20.0    | 20.0 *(carried forward)* | °    |                                           |
| $\alpha_{avrg}$   | Average pressure angle                              | 51.0    | 51.0 *(carried forward)* | °    |                                           |
| $\eta_{fwd}$      | Forward efficiency                                  | 89.0    | 89.0    | %    | For $\mu = 0.1$                                          |
| $\eta_{back}$     | Backdrive efficiency                                | 92.5    | 92.5    | %    | For $\mu = 0.1$                                          |
| $N_{eff}$         | Number of engaged ring pins                         | 5.25    | 5.0     | -    |                                                           |
| $F_{p,max}$       | Maximum ring pin normal force                       | 486.5   | 510.8   | N    |                                                           |
| $F_{out,max}$     | Maximum output shaft pin force                      | 1016.9  | 1000.0  | N    |                                                           |
| $F_{bearing}$     | Eccentric bearing load                              | 2666.7  | 2807.0  | N    | Safety factor: 2                                         |
| $E^*$             | Effective elastic modulus (vs. Cast PA6 dry, steel pin) | 3256 | 3485    | MPa  |                                                           |
| $p_{p,max}$       | Max ring pin Hertz pressure (disk ↔ ring pin, Cast PA6 dry) | 71.0 | 75.3 | MPa  | $R_r=5$mm; allowable (1.0×σ_y) = 65 MPa → **MARGINAL**   |
| $p_{output}$      | Max output pin Hertz pressure (disk ↔ output pin, Cast PA6 dry) | *n/a (not separately modeled before)* | 70.7 | MPa | $R_{r,out}=4$mm; allowable = 65 MPa → MARGINAL, but below $p_{p,max}$ |
| $p_{p,mount}$     | Ring pin pressure on housing and lid                | 4.5     | *not recomputed* | MPa |                                                     |
| $p_{out,mount}$   | Output shaft pin pressure on output shaft           | 14.1    | *not recomputed* | MPa |                                                     |

**Headline result: PA6 (dry) is marginal, same ballpark as before.** With the ring pin correctly governing (75.3 MPa vs. 65 MPa allowable, a ~16% overage — "MARGINAL" by the script's own ≤1.25× rule, not an outright "FAIL"), this isn't materially worse than where the original 20:1 design already sat (71.0 MPa against the same 65 MPa allowable). The 20→19 lobe change costs a real but modest ~6% increase in ring contact pressure (71.0→75.3 MPa) from one fewer pin pitch sharing the load. Cast PA6 (humid) still passes outright (43.7 vs. 45 MPa). A full material/geometry sweep at these final radii:

| Disk material | $p_{p,max}$ (ring) | $p_{output}$ (output) | $p_{max}$ | Allowable | Status |
| --- | --- | --- | --- | --- | --- |
| Steel (hardened, σ_y≈1000) | 433.1 | 406.5 | 433.1 | 1000 | OK |
| 42CrMo4 Q&T (σ_y≈900) | 433.1 | 406.5 | 433.1 | 900 | OK |
| Mild steel S235JR (σ_y=235) | 433.1 | 406.5 | 433.1 | 235 | FAIL |
| Cast PA6 (dry) | 75.3 | 70.7 | 75.3 | 65 | MARGINAL |
| Cast PA6 (humid) | 43.7 | 41.0 | 43.7 | 45 | OK |
| POM | 71.5 | 67.1 | 71.5 | 66 | MARGINAL |
| PLA | 76.7 | 72.0 | 76.7 | 70 | MARGINAL |
| Nylon 12 Tough (SLS) | 52.8 | 49.5 | 52.8 | 42 | FAIL |

**Before building this**, still get a real pressure-angle reading (simulator membership or FEA) rather than the carried-forward approximation, and confirm whether the actual "PA6" disk material is specifically dry- or humid-conditioned (the difference between MARGINAL and a clean pass).

## BOM

See [`bom/Motor_L_BOM.csv`](bom/Motor_L_BOM.csv).

## CAD

STEP/3MF source files are under [`cad/`](cad).
