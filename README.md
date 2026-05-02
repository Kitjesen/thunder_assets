# Thunder v3 Assets

This repository contains the standalone Thunder v3 wheeled-leg robot asset used by RobotLab.

## Files

- `meshes/` contains the STL visual and collision mesh files referenced by the robot description.
- `urdf/thunder_v3.urdf` is the primary URDF used by RobotLab and Isaac Lab.
- `urdf/legacy/thunder_0131copy.urdf` is a preserved legacy reference URDF from the January 31 copy line. It is not the primary training asset.
- `urdf/legacy/thunder_v3_cad_2026-05-02.urdf` is the raw May 2 CAD export used to refresh the primary inertial parameters.
- `xml/thunder_v3.xml` is an XML-extension copy of the same robot description for tools that expect `.xml` files. Keep it synchronized with `urdf/thunder_v3.urdf`.

## Current Asset Version

Version label: `cad-2026-05-02-symmetric-wheel`

The primary URDF keeps RobotLab-compatible link and joint names while using the May 2 CAD inertial values:

- all four wheel/foot links use fixed mass `1.40377 kg`
- all four wheel/foot centers of mass and inertia tensors are symmetric
- calf/thigh inertial origins include the knee-alignment correction from the May 2 CAD export
- remaining left/right center-of-mass offsets are expected to come from the motor geometry itself; the remaining offset is within about `1.5 mm`, mainly on the z axis
- y-axis symmetry is preserved for the wheel/foot links

The raw CAD export uses lowercase link names with `_Link` suffixes, package mesh paths, zero effort/velocity metadata, and wheel limit tags. Do not use it directly for RobotLab training unless those fields are adapted first.

## Joint Configuration Notes

Thunder v3 has 12 leg joints and 4 wheel joints:

- Leg joints: `.*_hip_joint`, `.*_thigh_joint`, `.*_calf_joint`
- Wheel joints: `.*_foot_joint`

The wheel joints must stay `type="continuous"` without zero position limits. Do not add a limit like:

```xml
<limit lower="0" upper="0" effort="0" velocity="0" />
```

on any `*_foot_joint`. That locks the imported wheel joints in simulation and makes the robot step instead of roll.

The fixed URDF keeps the wheel joints continuous and gives the leg joints nonzero motor metadata:

- leg joint effort: `120`
- leg joint velocity: `17.48`
- front/right and rear/left calf joints use positive calf ranges
- front/left and rear/right calf joints use negative calf ranges

## Legacy URDF Notes

`urdf/legacy/thunder_0131copy.urdf` is archived for comparison only. Its wheel joint axes match the current primary URDF:

- `FR_foot_joint`: `0 1 0`
- `FL_foot_joint`: `0 -1 0`
- `RR_foot_joint`: `0 1 0`
- `RL_foot_joint`: `0 -1 0`

Known differences from `urdf/thunder_v3.urdf`:

- wheel/foot mass is `1.78294 kg` per link instead of the current `1.40377 kg`
- rear calf limits are wider on the legacy copy
- `RR_hip` diagonal inertia is asymmetric relative to the other hip links, so do not copy its inertial values into the primary asset without checking CAD/source measurements

RobotLab then maps the joints to actuators as follows:

- Legs use `DCMotorCfg`, an explicit DC motor model with effort, saturation effort, velocity limit, stiffness, and damping.
- Wheels use `ImplicitActuatorCfg`, the PhysX/Isaac Sim internal implicit drive, configured as a velocity drive.

Current RobotLab actuator values:

- Leg motors: `effort_limit=120.0`, `saturation_effort=120.0`, `velocity_limit=17.48`, `stiffness=100.0`, `damping=5.0`
- Wheel drive: `effort_limit_sim=60.0`, `velocity_limit_sim=16.956`, `stiffness=0.0`, `damping=1.0`

## Validation

The fixed asset was checked by parsing the URDF as XML and by a direct wheel-drive smoke test in RobotLab. With randomization disabled, commanded wheel velocity reached about `10 rad/s`, and the robot base moved forward at about `1.2 m/s`, matching the `0.12 m` wheel radius.
