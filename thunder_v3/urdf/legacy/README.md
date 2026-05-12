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

## `thunder_v3_cad_2026-05-02.urdf`

Version label: `cad-2026-05-02-symmetric-wheel-raw`

Source:

```text
D:\Tencent\wechat\xwechat_files\wxid_gyuafybcd6u311_9e10\msg\file\2026-05\轮足狗机器人v3.urdf
```

Status:

- archived as the raw CAD export behind the current primary asset update
- not a direct RobotLab training file
- inertial values were copied into `../thunder_v3.urdf` after mapping lowercase CAD names to the canonical RobotLab names

Important adaptation notes:

- The primary URDF keeps canonical names such as `FR_hip`, `FR_foot`, and `FR_hip_joint`.
- The primary URDF keeps wheel joints continuous and without CAD-exported zero limit tags.
- The primary URDF keeps leg joint effort `120` and velocity `17.48`; the raw CAD export has `0` for those metadata fields.
- The primary URDF keeps the existing rear calf limits rather than the wider raw CAD export limits.
