"""Verify the current V4 asset against its URDF and compiled MuJoCo contacts."""

from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import mujoco
import numpy as np


V4 = Path(__file__).resolve().parents[1] / "thunder_v4"
MJCF = V4 / "mjcf" / "thunder_v4_mujoco.xml"
LEGS = ("FR", "FL", "RR", "RL")
ACTUATORS = tuple(f"{leg}_{part}_joint" for leg in LEGS for part in ("hip", "thigh", "calf")) + tuple(
    f"{leg}_foot_joint" for leg in LEGS
)
FRICTION = (1.0, 0.005, 0.0001)


class ThunderV4MuJoCoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = mujoco.MjModel.from_xml_path(str(MJCF))
        cls.urdf = ET.parse(V4 / "urdf" / "thunder_v4.urdf").getroot()

    def test_current_v4_geometry_and_actuators_match_urdf(self):
        model = self.model
        links = {link.get("name"): link for link in self.urdf.findall("link")}
        joints = {joint.get("name"): joint for joint in self.urdf.findall("joint")}
        mass = sum(float(link.find("inertial/mass").get("value")) for link in links.values())
        self.assertAlmostEqual(model.body_mass.sum(), mass, places=5)
        self.assertAlmostEqual(mass, 45.8086, places=5)
        self.assertEqual(model.joint("floating_base_joint").type[0], mujoco.mjtJoint.mjJNT_FREE)
        self.assertEqual((model.nq, model.nv, model.nu), (23, 22, 16))
        self.assertEqual(tuple(model.actuator(i).name for i in range(model.nu)), ACTUATORS)

        velocity_limits = []
        for name in ACTUATORS:
            source = joints[name.lower()]
            limit = source.find("limit")
            effort = float(limit.get("effort"))
            np.testing.assert_allclose(model.actuator(name).ctrlrange, (-effort, effort))
            np.testing.assert_allclose(model.jnt_actfrcrange[model.joint(name).id], (-effort, effort))
            np.testing.assert_allclose(model.joint(name).axis, np.fromstring(source.find("axis").get("xyz"), sep=" "))
            velocity_limits.append(float(limit.get("velocity")))
            if source.get("type") == "continuous":
                self.assertFalse(model.joint(name).limited[0])
            else:
                np.testing.assert_allclose(model.joint(name).range, [float(limit.get(k)) for k in ("lower", "upper")])
                stand = model.key("v4_nominal_stand").qpos[model.joint(name).qposadr[0]]
                self.assertGreaterEqual(stand, float(limit.get("lower")))
                self.assertLessEqual(stand, float(limit.get("upper")))
        np.testing.assert_allclose(model.numeric("hardware_joint_velocity_limit_rad_s").data, velocity_limits)

        for leg in LEGS:
            source_link = links[f"{leg.lower()}_foot_Link"]
            cylinder = source_link.find("collision/geometry/cylinder")
            wheel = model.geom(f"{leg}_wheel")
            self.assertEqual(wheel.type[0], mujoco.mjtGeom.mjGEOM_CYLINDER)
            np.testing.assert_allclose(wheel.size[:2], [float(cylinder.get("radius")), float(cylinder.get("length")) / 2])
            self.assertAlmostEqual(wheel.size[0], 0.095)
            np.testing.assert_allclose(wheel.pos, np.fromstring(source_link.find("collision/origin").get("xyz"), sep=" "))

    def test_actual_wheel_ground_contacts_use_v4_material(self):
        model = self.model
        wheels = {model.geom(f"{leg}_wheel").id for leg in LEGS}
        ground = model.geom("ground").id
        for geom_id in wheels | {ground}:
            np.testing.assert_allclose(model.geom_friction[geom_id], FRICTION)
            self.assertEqual(model.geom_condim[geom_id], 4)

        data = mujoco.MjData(model)
        mujoco.mj_resetDataKeyframe(model, data, model.key("v4_nominal_stand").id)
        mujoco.mj_forward(model, data)
        # Lower the standing pose until all four tires touch the flat ground.
        highest_tire_bottom = max(data.geom_xpos[i, 2] - model.geom_size[i, 0] for i in wheels)
        data.qpos[2] -= highest_tire_bottom + 0.001
        mujoco.mj_forward(model, data)
        touched = set()
        for contact in data.contact:
            pair = {contact.geom1, contact.geom2}
            if ground in pair and pair & wheels:
                touched.update(pair & wheels)
                self.assertEqual(contact.dim, 4)
                np.testing.assert_allclose(contact.friction, [1.0, 1.0, 0.005, 0.0001, 0.0001])
        self.assertEqual(touched, wheels)

    def test_v4_defaults_do_not_replace_external_world_material(self):
        tree = ET.parse(MJCF)
        root = tree.getroot()
        root.find("compiler").set("meshdir", str(V4 / "meshes"))
        ET.SubElement(root.find("default"), "geom", friction="0.7 0.002 0.0002", condim="3")
        ET.SubElement(root.find("worldbody"), "geom", name="external_floor", type="plane", size="0 0 1", pos="0 0 -2")
        model = mujoco.MjModel.from_xml_string(ET.tostring(root, encoding="unicode"))
        np.testing.assert_allclose(model.geom("external_floor").friction, [0.7, 0.002, 0.0002])
        self.assertEqual(model.geom("external_floor").condim[0], 3)
        for name in ["ground", *(f"{leg}_wheel" for leg in LEGS)]:
            np.testing.assert_allclose(model.geom(name).friction, FRICTION)


if __name__ == "__main__":
    unittest.main()
