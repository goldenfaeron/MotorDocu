# Motor S

Author: Tobias Reich
Related: [Cycloidal Drive](../docs/cycloidal-drive.md)

## Dimensions

### Cycloidal drive

See [Cycloidal Drive](../docs/cycloidal-drive.md) for the full explanation of all calculations. [`scripts/cycloidal_disk_analysis.py`](../scripts/cycloidal_disk_analysis.py) does most of the calculations for you (edit its input parameters for this motor's geometry before running).

#### Validation list

- [x] Disk material must hold up to $p_{p,max}$ and $p_{out,max}$
- [x] Input shaft must hold up to $F_{bearing,max}$ (Fusion 360 study)
- [x] Bearing must hold up to $F_{bearing,max}$
- [x] Output shaft pin contacts must hold up to $F_{out,max}$
- [x] Housing pin contacts must hold up to $F_{p,max}$

#### Requirements

- **Target ratio (i):** $15:1$
- **Nominal output torque:** $9\,Nm$

#### Core geometry

| Symbol      | Param                                | Value        | Unit | Notes            |
| ----------- | ------------------------------------- | ------------ | ---- | ---------------- |
| $N_l$       | Number of lobes (cycloid disc teeth)  | 15           | -    |                  |
| $N_p$       | Number of ring pins                   | $N_l + 1$    | -    | Always lobes + 1 |
| $N_{out}$   | Number of output shaft pins           | 6            | -    |                  |
| $R_p$       | Ring pin circle radius                | 27.5         | mm   |                  |
| $R_{out}$   | Output shaft pin radius               | 15.9         | mm   |                  |
| $R_r$       | Pin radius                            | 4; 3         | mm   | ring; output     |
| $e$         | Eccentricity                          | 1.15         | mm   | Typ. 0.5–2 mm    |
| $h_{disk}$  | Disk height                           | 10           | mm   |                  |

#### Materials

| Part         | Material         |
| ------------ | ------------------ |
| Disk         | Cast PA6           |
| Input shaft  | Nylon 12 Tough     |
| Output shaft | Nylon 12 Tough     |
| Housing      | Nylon 12 Tough     |

#### Derived parameters

| Symbol            | Param                                              | Value   | Unit | Notes                                                   |
| ----------------- | --------------------------------------------------- | ------- | ---- | -------------------------------------------------------- |
| $\alpha_{min}$    | Minimum pressure angle                              | 43.5    | °    |                                                           |
| $\alpha_{avrg}$   | Average pressure angle                              | 61.9    | °    |                                                           |
| $\eta_{fwd}$      | Forward efficiency                                  | 84.2    | %    | For $\mu = 0.1$                                          |
| $\eta_{back}$     | Backdrive efficiency                                | 94.9    | %    | For $\mu = 0.1$                                          |
| $N_{eff}$         | Number of engaged ring pins                         | 4       | -    |                                                           |
| $F_{p,max}$       | Maximum ring pin normal force                       | 225.6   | N    |                                                           |
| $F_{out,max}$     | Maximum output shaft pin force                      | 377.4   | N    |                                                           |
| $F_{bearing}$     | Eccentric bearing load                              | 1043.5  | N    | Safety factor: 2                                         |
| $E^*$             | Effective elastic modulus                           | 1173    | MPa  | Humid PA6 with steel pin                                 |
| $p_{p,max}$       | Max ring pin Hertz pressure (disk ↔ pin)            | 45.9    | MPa  | Assuming 1/4 of pins are engaged and safety factor: 2    |
| $p_{out,max}$     | Max output shaft pin Hertz pressure (disk ↔ pin)    | 27.9    | MPa  |                                                           |
| $p_{p,mount}$     | Ring pin pressure on housing and lid                | 3.41    | MPa  |                                                           |
| $p_{out,mount}$   | Output shaft pin pressure on output shaft           | 13.47   | MPa  |                                                           |

## BOM

See [`bom/Motor_S_BOM.csv`](bom/Motor_S_BOM.csv).

## CAD

- [`cad/step/`](cad/step) — parametric STEP export from Fusion 360 (full assembly, BLDC and drive components, purchased parts).
- [`cad/BLDC/`](cad/BLDC), [`cad/drive/`](cad/drive), [`cad/springContactBracket.3mf`](cad/springContactBracket.3mf) — existing 3MF print-ready meshes (unchanged by this refresh).

> **Unresolved variants, not deduplicated — don't assume which is current:**
> - `cad/step/drive/` has two cycloidal disk exports: `cycloidalDisk.step` and `cycloidalDisk_S_6und4mmPins.step` (the latter name suggests a 6mm/4mm mixed pin-radius variant — matches this doc's $R_r = 4; 3$mm note, but not confirmed as the as-built version).
> - `cad/step/` has two spring contact bracket exports: `springContactBracket.step` and `springContactBracketFDM.step`.
