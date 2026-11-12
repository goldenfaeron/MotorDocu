# Motor L

Author: Tobias Reich
Related: [Cycloidal Drive](../docs/cycloidal-drive.md)

## Dimensions

### Cycloidal drive

See [Cycloidal Drive](../docs/cycloidal-drive.md) for the full explanation of all calculations. The `scripts` folder in the main workspace contains a Python script that does most of the calculations for you.

#### Validation list

- [x] Disk material must hold up to $p_{p,max}$ and $p_{out,max}$
- [x] Input shaft must hold up to $F_{bearing,max}$ (Fusion 360 study)
- [x] Bearing must hold up to $F_{bearing,max}$
- [x] Output shaft pin contacts must hold up to $F_{out,max}$
- [x] Housing pin contacts must hold up to $F_{p,max}$

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
| $R_r$       | Pin radius                            | 5.0          | mm   | Roller radius    |
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

> **Note:** these values were calculated for the previous $20:1$ ratio ($N_l = 20$, $N_p = 21$). They have not been recomputed for the new $19:1$ ratio yet — rerun the cycloidal disk analysis script before relying on them for structural validation.

| Symbol            | Param                                              | Value   | Unit | Notes                                                   |
| ----------------- | --------------------------------------------------- | ------- | ---- | -------------------------------------------------------- |
| $\alpha_{min}$    | Minimum pressure angle                              | 20.0    | °    |                                                           |
| $\alpha_{avrg}$   | Average pressure angle                              | 51.0    | °    |                                                           |
| $\eta_{fwd}$      | Forward efficiency                                  | 89.0    | %    | For $\mu = 0.1$                                          |
| $\eta_{back}$     | Backdrive efficiency                                | 92.5    | %    | For $\mu = 0.1$                                          |
| $N_{eff}$         | Number of engaged ring pins                         | 5.2     | -    |                                                           |
| $F_{p,max}$       | Maximum ring pin normal force                       | 486.5   | N    |                                                           |
| $F_{out,max}$     | Maximum output shaft pin force                      | 1016.9  | N    |                                                           |
| $F_{bearing}$     | Eccentric bearing load                              | 2666.7  | N    | Safety factor: 2                                         |
| $E^*$             | Effective elastic modulus                           | 3256    | MPa  | With steel pin                                           |
| $p_{p,max}$       | Max ring pin Hertz pressure (disk ↔ pin)            | 71.0    | MPa  | Assuming 1/4 of pins are engaged and safety factor: 2    |
| $p_{out,max}$     | Max output shaft pin Hertz pressure (disk ↔ pin)    | 39.6    | MPa  |                                                           |
| $p_{p,mount}$     | Ring pin pressure on housing and lid                | 4.5     | MPa  |                                                           |
| $p_{out,mount}$   | Output shaft pin pressure on output shaft           | 14.1    | MPa  |                                                           |

## BOM

See [`bom/Motor_L_BOM.csv`](bom/Motor_L_BOM.csv).

## CAD

STEP/3MF source files are under [`cad/`](cad).
