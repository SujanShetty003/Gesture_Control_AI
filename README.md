##**Gesture Control Game Interaction**#

This project allows you to control the popular game Subway Surfers using real-time hand gestures detected through your webcam. It leverages the MediaPipe library for hand and pose tracking and PyAutoGUI to simulate keyboard inputs.

**Features**
Shoulder Position Detection: Move the character left or right based on shoulder alignment.

**Hand Gestures:**

Raise two fingers on both hands to start the game.

Use gestures to trigger in-game actions like jump (up) and slide (down).

Real-Time Processing: Smooth and responsive gesture recognition using a webcam.

**Prerequisites:**

**Libraries:**
Ensure the following Python libraries are installed:

OpenCV,

MediaPipe,

PyAutoGUI

**You can install them with:** 
    Command:
        pip install opencv-python mediapipe pyautogui


**Hardware Requirements:**
A webcam (internal or external).

A computer capable of running Python and the above libraries.

**How to Run:**
  python your_script.py

**This will start the webcam and launch the hand gesture detection interface.**

**Control the Game:**

Open the Subway Surfers game.

Position yourself in front of the webcam.

Perform gestures as follows:

Raise both index and middle fingers to start.

Lean shoulders left/right to move the character.

Raise hands up to jump.

Lower hands down to slide.



**Gesture Mapping:**

  Gesture	Actions:
    
Two fingers raised on both hands => Start the game

Lean shoulders left =>	Move left
    
Lean shoulders right	=> Move right
    
Mid-point above initial position (up)	=> Jump
    
Mid-point below initial position (down)	=> Slide


**Notes**
    Ensure proper lighting for accurate detection.
    Position yourself so your shoulders and hands are clearly visible in the webcam frame.
    If gestures are not recognized, adjust your position or improve lighting conditions.


**Troubleshooting:**

Issue: The game does not respond to gestures.

Solution: Ensure that the game window is focused and accepts keyboard inputs.

Issue: Gesture detection is inaccurate.
  
Solution: Verify that the webcam view shows all relevant body parts clearly.


**Acknowledgments**

MediaPipe: For providing efficient hand and pose tracking.

PyAutoGUI: For simulating keyboard inputs to control the game.


