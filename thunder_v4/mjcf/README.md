# Thunder V4 MuJoCo MJCF

This directory contains a MuJoCo representation of the real Thunder V4
small-wheel hardware. The files reference the adjacent V4 mesh directory, so
keep this layout intact:

```text
thunder_v4/
  meshes/
  mjcf/
    thunder_v4_mujoco.xml
    thunder_v4_mujoco_stairs.xml
```

## Models

- `thunder_v4_mujoco.xml`: flat-ground V4 scene.
- `thunder_v4_mujoco_stairs.xml`: the same robot model plus three fixed stairs.

Both files expose the same floating-base state and 16 policy actuators in this
order: the twelve leg joints (FR, FL, RR, RL; hip/thigh/calf) followed by the
four wheel joints (FR, FL, RR, RL).

## Hardware Contract

| Item | Value |
|---|---:|
| Total modeled mass | `45.8086 kg` |
| Leg torque limit | `120 Nm` |
| Wheel torque limit | `17 Nm` |
| Leg speed limit | `17.48 rad/s` |
| Wheel speed limit | `44 rad/s` |
| Wheel collision radius | `0.093 m` |
| Nominal keyframe | `v4_nominal_stand` |

The numerical speed limits are available in the MJCF numeric named
`hardware_joint_velocity_limit_rad_s`. They document the V4 hardware contract;
a controller should implement its own speed-torque behavior rather than clip
MuJoCo state velocity directly.

Collision primitives remain enabled for physics but are render-transparent by
default. The opaque CAD meshes are the intended visible robot. This avoids
showing collision boxes and cylinders during normal playback without changing
contact behavior.

## Smoke Test

```python
import mujoco

model = mujoco.MjModel.from_xml_path("thunder_v4/mjcf/thunder_v4_mujoco.xml")
data = mujoco.MjData(model)
key = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_KEY, "v4_nominal_stand")
data.qpos[:] = model.key_qpos[key]
mujoco.mj_forward(model, data)
```
