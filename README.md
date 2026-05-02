# Thunder v3 Assets

Current version: `cad-2026-05-02-symmetric-wheel`

Primary asset: `urdf/thunder_v3.urdf`

This repository contains the standalone Thunder v3 wheeled-leg robot asset used
by RobotLab and Isaac Lab.

## What Changed

This version updates the robot dynamics data in the primary URDF:

- Total modeled mass changed from `44.47163 kg` to `48.79163 kg`.
- All four wheel/foot assemblies now use `1.40377 kg` mass instead of the old
  `0.32377 kg` placeholder-style mass.
- All four wheel/foot inertials are symmetric:
  - right side COM: `0.00000 -0.01385 0.00000`
  - left side COM: `0.00000 0.01385 0.00000`
  - tensor: `ixx=0.00092`, `iyy=0.00121`, `izz=0.00092`, off-diagonal terms `0`
- `FR_calf`, `RR_calf`, and `RR_thigh` COM and inertia tensors were corrected
  from the May 2 CAD-derived values.
- `xml/thunder_v3.xml` was synchronized with `urdf/thunder_v3.urdf`.
- The raw CAD export was saved at
  `urdf/legacy/thunder_v3_cad_2026-05-02.urdf` for traceability.

The primary URDF intentionally keeps the RobotLab-compatible interface:

- canonical link names such as `FR_hip`, `FL_foot`, and `base_link`
- canonical joint names such as `FR_hip_joint` and `RR_foot_joint`
- relative mesh paths under `meshes/`
- continuous wheel joints without position limits
- leg joint effort `120` and velocity `17.48`

## Files

- `urdf/thunder_v3.urdf`: current RobotLab/Isaac Lab URDF
- `xml/thunder_v3.xml`: byte-synchronized copy for tools that expect `.xml`
- `meshes/`: STL visual and collision meshes
- `urdf/legacy/`: historical references only, not the active training asset

Do not use the raw CAD export directly for RobotLab training. It has lowercase
`_Link` names, package mesh paths, zero joint effort/velocity metadata, and
wheel limit tags that can break rolling-wheel behavior.

## Validation

Validated for this version:

- parsed the primary URDF, XML copy, and raw CAD archive as XML
- verified `21` links and `20` joints
- verified total mass `48.79163 kg`
- verified `urdf/thunder_v3.urdf` and `xml/thunder_v3.xml` are synchronized
- verified wheel joints stay continuous
- verified wheel axes and leg joint effort/velocity metadata

Not validated:

- Isaac Lab runtime import after the GitHub push
- policy rollout with the updated dynamics
