# Motors

CAD and documentation for the three cycloidal-drive BLDC actuators used across the robot: **L**, **M**, and **S**. Each actuator pairs a frameless BLDC stator/rotor with a single-stage cycloidal reduction.

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

CAD was last refreshed from a full-project Fusion 360 export; only the three actuator subtrees were kept (CNC-shop-specific exports, a torque test rig, an unrelated CNC router project, and loose electronics duplicates already covered by the separate `electronics/hall_encoder` repo were all excluded). Each motor's README flags any unresolved part-revision ambiguity found during that sort (e.g. duplicate exports with unclear current-ness) — check there before using CAD for manufacturing.

## License

Hardware (CAD, BOMs) is licensed under [CERN-OHL-S v2](LICENSE). Documentation is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
