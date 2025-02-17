# Nexus-Stellaron-FlatSat

Nexus-Stellaron FlatSat Team

[https://courses.bwsix.edly.io/assets/courseware/v1/325030de0e6636afe656d5cd7a6ed3a4/asset-v1:bwsix+BWSI1170+2024-2025+type@asset+block/Raspberry_Pi_Setup_2024_V2.pdf](https://courses.bwsix.edly.io/assets/courseware/v1/8dadbae3dfec5287cbe82c6a0671caa6/asset-v1:bwsix+BWSI1170+2024-2025+type@asset+block/Flat_Sat_Challenge_Instructions_2024.pdf)


Changes made to ColorCodeCubeSat.py:

Replaced capture_continuous with camera.capture_array() for capturing frames.

Configured the camera using camera.create_video_configuration.

Removed rawCapture as it's not needed with the updated method.

This should work smoothly for your color detection system! Let me know if there’s anything else you need help with.
