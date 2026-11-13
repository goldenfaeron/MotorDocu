# Motors

CAD and documentation for the three cycloidal-drive BLDC actuators that can be used across a whole robot: **L**, **M**, and **S**. Each actuator pairs a frameless BLDC stator/rotor with a single-stage cycloidal reduction.
Each actuator has a gear reduction of less that 20:10 which makes them backdrivable. This property can be used to sense external loads by measuring rising motor currents. Also it reduces the reflected inertia which makes the actuators safer to use for HRI (human robot interaction) than Actuators that achieve the same output torques by using higher gear ratios.

| Motor | Target ratio | Nominal output torque |
| ----- | ------------- | ----------------------- |
| [Motor L](motor_L/README.md) | 19:1 | 60 Nm |
| [Motor M](motor_M/README.md) | 20:1 | 20 Nm |
| [Motor S](motor_S/README.md) | 15:1 | 9 Nm |

Shared background on the cycloidal reduction stage (transmission ratio, pressure angle, efficiency, force/Hertz-pressure calculations) lives in [`docs/cycloidal-drive.md`](docs/cycloidal-drive.md).

## Repository layout

```
motors/
├── docs/                 shared theory (cycloidal drive math)
├── assembly/
│   └── Actuators.step    combined STEP assembly of all three actuators
├── motor_L/
│   ├── README.md         dimensions, requirements, materials, derived parameters
│   ├── bom/              bill of materials (CSV)
│   └── cad/
│       ├── step/         parametric STEP export (assembly, BLDC, drive)
│       ├── BLDC/         3MF print-ready meshes
│       ├── drive/        3MF print-ready meshes
│       └── springContactBracket.3mf
├── motor_M/              same structure as motor_L
├── motor_S/              same structure as motor_L
└── scripts/
    ├── cycloidal_disk_analysis.py  pin/disk Hertz-contact and force analysis
    └── MassExportProject.py        Fusion 360 script: batch-export a whole
                                     project's designs to STEP + 3MF
```

## License

Everything in this repository (CAD, BOMs, and documentation) is licensed under [CC BY-NC-SA 4.0](LICENSE) ([summary](https://creativecommons.org/licenses/by-nc-sa/4.0/)).
