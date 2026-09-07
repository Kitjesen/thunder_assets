# Thunder V4 — current robot version

V4 is the current Thunder small-wheel robot. V3 remains available for previous
policies and historical comparisons.

## Definition and ownership

| Item | Current V4 value / source |
| --- | --- |
| Physical geometry, inertia, axes, joint limits | `urdf/thunder_v4.urdf` |
| Visual geometry | `meshes/*.STL` |
| MuJoCo contact materials and scene | `mjcf/thunder_v4_mujoco.xml` |
| Modeled mass | `45.8086 kg` |
| Wheel collision radius | `0.095 m` (95 mm) |
| Wheel collision width | `0.05117 m` |
| Actuated joints | 12 leg joints + 4 continuous wheel joints |
| Leg torque / velocity limits | `120 Nm` / `17.48 rad/s` |
| Wheel torque / velocity limits | `17 Nm` / `44 rad/s` |

The MuJoCo model adds a free floating base and retains the fixed sensor masses.
URDF leg prefixes `fr/fl/rr/rl` become `FR/FL/RR/RL` in the MJCF. Actuator order
is hip, thigh, calf for FR, FL, RR, RL, followed by the four wheel actuators
in the same leg order. `v4_nominal_stand` provides a joint-limit-valid reference
pose; a controller is still required to hold or move the robot.

MuJoCo motor torque limits are enforced by the model. The custom numeric
`hardware_joint_velocity_limit_rad_s` records velocity limits in actuator
order; a controller must consume them to enforce a speed envelope. They are
not an automatic MuJoCo joint-speed clamp.

## MuJoCo friction

The supplied MJCF actually applies these values to all four wheel collision
geoms and the included ground:

```xml
<geom friction="1.0 0.005 0.0001" condim="4" />
```

| Coefficient | Value | Meaning with `condim=4` |
| --- | --- | --- |
| Sliding | `1.0` (dimensionless) | Active |
| Torsional | `0.005 m` | Active |
| Rolling | `0.0001 m` | Declared; only active with `condim=6` |

`thunder_v4_rubber_wheel` owns the wheel material. Wheel geoms deliberately
have no inline `friction` attribute, so generic collision annotations cannot
shadow the wheel class. The supplied ground and robot subtree select the
named `thunder_v4` defaults; these are not global world defaults.

Non-wheel leg collision primitives retain their existing separate material
`0.9 0.2 0.2`. Those values do not apply to the tires or the ground. An external
world owns its own material: equal-priority contacts combine friction using
the maximum of each component, so changing the world requires checking the
resulting contacts too.

These values are a MuJoCo simulation baseline, not measured tire/ground
calibration. Standard URDF does not carry this MuJoCo contact contract.
Isaac Lab and Gazebo integrations must configure their own physics materials
using their respective parameter definitions.

References: MuJoCo [geom friction](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-geom-friction),
[default inheritance](https://mujoco.readthedocs.io/en/stable/modeling.html#default-settings),
and [contact combination](https://mujoco.readthedocs.io/en/stable/modeling.html#contact-parameters).

## Load and verify

From the repository root, in a Python environment with MuJoCo and NumPy:

```python
import mujoco

model = mujoco.MjModel.from_xml_path("thunder_v4/mjcf/thunder_v4_mujoco.xml")
data = mujoco.MjData(model)
mujoco.mj_resetDataKeyframe(model, data, model.key("v4_nominal_stand").id)
mujoco.mj_forward(model, data)
print(model.geom("FR_wheel").friction)  # [1.0, 0.005, 0.0001]
```

```sh
python -m unittest discover -s tests -p "test_thunder_v4_mujoco.py" -v
```

The checks compile the actual mesh-backed asset, compare its mass, wheel
geometry, actuator order, axes and limits with the URDF, create all four
wheel/ground contacts, and verify that V4 material defaults do not replace an
external world's material.

Physics timestep, inference rate, observation construction, action scaling,
PD gains and speed limiting belong to the selected controller. The MJCF does
not choose a policy timestep; loading it alone uses MuJoCo's default timestep.

## Provenance and downstream compatibility

The kinematic tree was converted from the V4 URDF at
[`8b535d0`](https://github.com/Kitjesen/thunder_assets/commit/8b535d0f885371cc303f7a08056a7c6650cfa9d7)
using LingTu's
[V4 converter](https://github.com/Kitjesen/MapPilot/blob/0de010148654e52dca3abbae141fd4785f34da1c/sim/packages/robots/doso/thunder_v4/tools/generate_thunderv4_mjcf.py).
This checked-in MJCF is a maintained asset: its contact defaults are scoped to
V4 and its supplied ground explicitly selects that scope. When updating the
URDF, reconcile the converted geometry with this MJCF, preserve the scoped
material definitions, and run the checks above. No LingTu checkout is needed
to load or test the supplied asset.

LingTu [PR #22](https://github.com/Kitjesen/MapPilot/pull/22) fixes wheel friction
inheritance and policy timing in the navigation simulator. Its existing
qualified MJCF and the local 4998 training asset use a `0.093 m` wheel radius.
This repository retains the current URDF's `0.095 m` radius; do not silently
substitute it into those policy rollouts or transfer their speed/yaw results
to this geometry.

Validation here covers native MuJoCo 3.10.0 model import and contact behavior.
It does not establish policy performance, Isaac Lab / Gazebo behavior, or
physical-robot deployment readiness.
