# Motor L

Author: Tobias Reich
Related: [Cycloidal Drive](../docs/cycloidal-drive.md)

## Dimensions

### Cycloidal drive

See [Cycloidal Drive](../docs/cycloidal-drive.md) for the full explanation of all calculations. [`scripts/cycloidal_disk_analysis.py`](../scripts/cycloidal_disk_analysis.py) does most of the calculations for you — it's currently set up with this motor's 19:1 parameters (the run behind the Derived Parameters table below).

#### Validation list

> Unchecked pending re-validation against the recomputed 19:1 loads below — the previous checkmarks were for the 20:1 geometry and no longer apply as-is.

- [ ] Disk material must hold up to $p_{p,max}$ and $p_{out,max}$ — **currently fails for every candidate polymer disk material, see note below**
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
| $R_{out}$   | Output shaft pin radius               | 30.0         | mm   |                  |
| $R_r$       | Pin radius                            | 4.0          | mm   | Roller radius — resolves a pre-existing inconsistency where the table said 5.0mm but the profile formula below had 4 hardcoded; treating the formula as authoritative |
| $e$         | Eccentricity                          | 2.25         | mm   |                  |
| $h_{disk}$  | Disk height                           | 20.0         | mm   |                  |

Cycloidal disk profile (parametric, $t$ in radians):

```
((50.0)*cos(t))-(4*cos(t+arctan(sin((1-20)*t)/(((50.0)/(2.25*20))-cos((1-20)*t)))))-(2.25*cos(20*t))

(-(50.0)*sin(t))+(4*sin(t+arctan(sin((1-20)*t)/(((50.0)/(2.25*20))-cos((1-20)*t)))))+(2.25*sin(20*t))
```

#### Materials

| Part         | Material              |
| ------------ | ---------------------- |
| Disk         | PA6                     |
| Input shaft  | Nylon 12 Tough (SLS)    |
| Output shaft | Nylon 12 Tough (SLS)    |
| Housing      | Nylon 12 Tough (SLS)    |

#### Derived parameters

Recomputed via `scripts/cycloidal_disk_analysis.py` for the new $19:1$ geometry ($N_l=19$, $N_p=20$, $R_p=50.0$mm, $R_r=4.0$mm, $e=2.25$mm, $N_{out}=8$, $R_{out}=30.0$mm, $T_{out}=60$Nm, $\mu=0.1$, bearing safety factor $K=2$).

> **Assumptions carried into this run — verify before treating any status below as final:**
> - $\alpha_{min}$ and $\alpha_{avrg}$ are **carried forward unchanged from the old $20:1$ geometry**, not re-measured. The mevirtuoso.com pressure-angle simulator linked in the original docs turned out to be a paid "Premium" membership feature, not a free tool, so it wasn't used. Pressure angle is governed by $K_1 = e \cdot N_p / R_p$, which only shifts from $0.945$ (old) to $0.900$ (new, ~5%), so carrying the old values forward is a reasonable approximation — but get a real reading (simulator or FEA) before signing off.
> - $b_{contact}$ (axial pin contact length) is assumed equal to disk height $h_{disk}=20$mm — this isn't separately documented anywhere.
> - $R_{eff}$ for $F_{p,max}$ dropped slightly (5.25 → 5.0) because one fewer pin pitch is in the load-bearing region, which alone increases contact force ~5% independent of the pressure-angle assumption above.

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
| $p_{p,max}$       | Max ring pin Hertz pressure (disk ↔ pin, Cast PA6 dry)  | 71.0 | 84.2    | MPa  | $R_r=4$mm; allowable (1.0×σ_y) = 65 MPa → **FAIL**       |
| $p_{out,max}$     | Max output shaft pin Hertz pressure (disk ↔ pin)    | 39.6    | 50.5    | MPa  |                                                           |
| $p_{p,mount}$     | Ring pin pressure on housing and lid                | 4.5     | *not recomputed* | MPa |                                                     |
| $p_{out,mount}$   | Output shaft pin pressure on output shaft           | 14.1    | *not recomputed* | MPa |                                                     |

**Headline result: the disk material check now fails.** At $R_r=4$mm, every candidate polymer disk material (Nylon 12 Tough, Cast PA6 dry/humid, POM, PLA) comes back FAIL or MARGINAL against the script's generic allowables — Cast PA6 (dry) at 84.2 MPa vs. a 65 MPa allowable, for example. Re-running with $R_r=5$mm (the table's original value, before resolving the formula/table inconsistency above) gives a less severe but still marginal 75.3 MPa. Either way, dropping one lobe (20→19) raises $F_{p,max}$ ~5% from having one fewer pin pitch to spread load across, and that alone pushes an already-tight PA6 disk margin into fail/marginal territory. **Before building this**, either re-verify the pressure angle for real, reconsider $R_r$, increase $b_{contact}$, or re-check whether "PA6" in the materials table is a higher-strength grade than this script's generic "Cast PA6" placeholder — the original 20:1 numbers were already close to the edge (71.0 vs 65 MPa) using these same generic material constants.

## BOM

See [`bom/Motor_L_BOM.csv`](bom/Motor_L_BOM.csv).

## CAD

STEP/3MF source files are under [`cad/`](cad).
