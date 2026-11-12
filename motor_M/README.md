# Motor M

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

- **Target ratio (i):** $20:1$
- **Nominal output torque:** $20\,Nm$

#### Core geometry

| Symbol      | Param                                | Value        | Unit | Notes            |
| ----------- | ------------------------------------- | ------------ | ---- | ---------------- |
| $N_l$       | Number of lobes (cycloid disc teeth)  | 19           | -    |                  |
| $N_p$       | Number of ring pins                   | $N_l + 1$    | -    | Always lobes + 1 |
| $N_{out}$   | Number of output shaft pins           | 6            | -    |                  |
| $R_p$       | Ring pin circle radius                | 42.5         | mm   |                  |
| $R_{out}$   | Output shaft pin radius               | 29.5         | mm   |                  |
| $R_r$       | Pin radius                            | 8            | mm   | Roller radius    |
| $e$         | Eccentricity                          | 1.5          | mm   | Typ. 0.5–2 mm    |
| $h_{disk}$  | Disk height                           | 10           | mm   |                  |

Cycloidal disk profile (parametric, $t$ in radians):

```
((42.5)*cos(t))-(4*cos(t+arctan(sin((1-21)*t)/(((42.5)/(1.4*21))-cos((1-21)*t)))))-(1.4*cos(21*t))

(-(42.5)*sin(t))+(4*sin(t+arctan(sin((1-21)*t)/(((42.5)/(1.4*21))-cos((1-21)*t)))))+(1.4*sin(21*t))
```

#### Materials

| Part         | Material              |
| ------------ | ---------------------- |
| Disk         | Cast PA6                |
| Input shaft  | Nylon 12 Tough (SLS)    |
| Output shaft | Nylon 12 Tough (SLS)    |
| Housing      | Nylon 12 Tough (SLS)    |

#### Derived parameters

| Symbol            | Param                                              | Value   | Unit | Notes                                                   |
| ----------------- | --------------------------------------------------- | ------- | ---- | -------------------------------------------------------- |
| $\alpha_{min}$    | Minimum pressure angle                              | 42.5    | °    |                                                           |
| $\alpha_{avrg}$   | Average pressure angle                              | 61.3    | °    |                                                           |
| $\eta_{fwd}$      | Forward efficiency                                  | 84.6    | %    | For $\mu = 0.1$                                          |
| $\eta_{back}$     | Backdrive efficiency                                | 94.8    | %    | For $\mu = 0.1$                                          |
| $N_{eff}$         | Number of engaged ring pins                         | 5.2     | -    |                                                           |
| $F_{p,max}$       | Maximum ring pin normal force                       | 243.2   | N    |                                                           |
| $F_{out,max}$     | Maximum output shaft pin force                      | 452.0   | N    |                                                           |
| $F_{bearing}$     | Eccentric bearing load                              | 1333.3  | N    | Safety factor: 2                                         |
| $E^*$             | Effective elastic modulus                           | 3256    | MPa  | PA6 with steel pin                                       |
| $p_{p,max}$       | Max ring pin Hertz pressure (disk ↔ pin)            | 83.7    | MPa  | Assuming 1/4 of pins are engaged and safety factor: 2    |
| $p_{out,max}$     | Max output shaft pin Hertz pressure (disk ↔ pin)    | 59.6    | MPa  |                                                           |
| $p_{p,mount}$     | Ring pin pressure on housing and lid                | 5.1     | MPa  | $l = 8\,mm$                                              |
| $p_{out,mount}$   | Output shaft pin pressure on output shaft           | 10.7    | MPa  | $l = 7\,mm$                                              |

## BOM

See [`bom/Motor_M_BOM.csv`](bom/Motor_M_BOM.csv).

## CAD

STEP/3MF source files are under [`cad/`](cad).
