# Legacy URDF Inventory

This directory stores preserved Thunder URDF references that are useful for comparison but are not the primary simulation asset.

## `thunder_0131copy.urdf`

Version label: `legacy-0131copy`

Source:

```text
robot_lab/source/robot_lab/data/Robots/thunder/urdf/thunder_0131copy.urdf
```

Status:

- archived for reference and regression comparison
- not the active RobotLab/Isaac Lab training URDF
- wheel joint axes match the current primary URDF

Wheel axes:

```text
FR_foot_joint: 0 1 0
FL_foot_joint: 0 -1 0
RR_foot_joint: 0 1 0
RL_foot_joint: 0 -1 0
```

Important differences from `../thunder_v3.urdf`:

- Four wheel/foot links use `1.78294 kg` mass each; current `thunder_v3.urdf` uses about `0.32377 kg`.
- Rear calf limits are wider than the current primary URDF.
- `RR_hip` has an asymmetric diagonal inertia compared with the other hip links:

```text
FR_hip diag: 0.00688, 0.01259, 0.01604
FL_hip diag: 0.00690, 0.01253, 0.01596
RL_hip diag: 0.00691, 0.01254, 0.01597
RR_hip diag: 0.00344, 0.00353, 0.00350
```

Do not use this file as a drop-in replacement for the primary asset unless those dynamics are intentional.
