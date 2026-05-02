# Changelog

## 2026-05-02 - cad-2026-05-02-symmetric-wheel

- Updated the primary RobotLab/Isaac Lab asset at `urdf/thunder_v3.urdf`
  with corrected CAD-derived inertial parameters while preserving the canonical
  Thunder v3 link names, joint names, wheel joint axes, and leg joint metadata.
- Synchronized `xml/thunder_v3.xml` with the primary URDF for tools that expect
  an `.xml` file.
- Added the raw May 2 CAD export as
  `urdf/legacy/thunder_v3_cad_2026-05-02.urdf` for traceability.
- Documented why the raw CAD export is not used directly for RobotLab training:
  it uses lowercase `_Link` names, package mesh paths, zero joint effort and
  velocity metadata, and wheel limit tags that are unsafe for rolling wheels.
- Preserved `urdf/legacy/thunder_0131copy.urdf` as a historical comparison
  asset instead of replacing it in place.

Validation:

- Parsed the primary URDF, XML copy, and raw CAD archive as XML.
- Checked that the primary URDF and XML copy stay synchronized.
- Verified 21 links, 20 joints, continuous wheel joints, wheel axes, leg joint
  effort/velocity metadata, and total mass `48.79163 kg`.

Not validated:

- Isaac Lab runtime import after the GitHub push.
