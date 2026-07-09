# V86 Recovery MuJoCo Showcase

`v86_success_sequence_1080p_black.mp4` is a 24-second, 1920x1080, 30 FPS
MuJoCo sim-to-sim rollout assembled from three successful V86 recovery cases:

1. Side-left fall.
2. Side-right fall.
3. Inverted roll by 180 degrees (the legacy evaluation name is `supine`).

The policy checkpoint is `V86 model_27000`.  The control cadence is 50 Hz and
the MuJoCo integration timestep is 5 ms.  The visual robot meshes are rendered
black and collision-only geoms are transparent; this changes rendering only,
not collision physics.

This is a selected qualitative showcase, not an all-pose success benchmark.
In particular, the corresponding inverted-pitch 180-degree case (legacy name
`prone`) remains a failure and is intentionally not included in this video.
