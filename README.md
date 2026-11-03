
<div align="center">

# 🖐️ Hand Gesture Mouse & Media Controller

### Touch-Free Computer Interaction Using Hand Gestures

Control your mouse, scrolling, volume, media playback, and zoom operations using real-time hand gestures captured through a webcam.

<br/>

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand_Tracking-00A67E?style=for-the-badge)

<br/>

**Computer Vision | Gesture Recognition | Desktop Automation**

</div>

---

## 📌 Overview

Hand Gesture Mouse & Media Controller is a Python-based computer vision project that enables touch-free interaction with a computer using hand gestures.

The application uses a webcam to capture hand movements and translates recognized gestures into computer actions such as mouse movement, clicking, dragging, scrolling, volume adjustment, media playback, and zoom control.

The project explores an alternative approach to traditional mouse and keyboard interaction by using natural hand movements.

## 🎯 Problem Statement

Traditional computer interaction primarily depends on physical input devices such as a mouse and keyboard.

This project explores how hand gesture recognition can provide an alternative interaction method, allowing users to perform common computer operations without directly touching these devices.

By combining webcam-based hand tracking and gesture-based controls, the application demonstrates the potential of computer vision in human-computer interaction.

---

## ✨ Key Features

### 🖱️ 1. Mouse Cursor Control

- Control the mouse cursor using the right-hand index finger.
- Translate hand movements into cursor movements.
- Enable touch-free mouse navigation.

### 👆 2. Left and Right Click

- Thumb and index finger pinch for left-click.
- Quick pinch gesture for clicking.
- Holding the pinch gesture enables drag-and-drop.
- Thumb and middle finger pinch for right-click.

### 📜 3. Scroll Control

- Use left-hand vertical movement to scroll.
- Navigate through content without touching the mouse wheel.

### 🔊 4. Volume Control

- Use left-hand horizontal movement in the upper screen area.
- Adjust system volume through gestures.

### 🎵 5. Media Playback Control

- Thumb and ring finger pinch for next track.
- Thumb and pinky finger pinch for play/pause.

### 🔍 6. Zoom Control

- Use a two-hand pinch gesture.
- Control zoom-in and zoom-out operations.
- Simulate keyboard shortcuts for zoom control.

### ⚙️ 7. Air Mode

- Press `E` to toggle Air Mode on or off.
- Press `Q` to quit the application.

---

## 🎮 Gesture Controls

| Hand Gesture | Computer Action |
|---|---|
| Right-hand index finger movement | Mouse movement |
| Left thumb + index pinch | Left click |
| Hold thumb + index pinch | Drag and drop |
| Left thumb + middle pinch | Right click |
| Left-hand vertical movement | Scrolling |
| Left-hand horizontal movement in upper area | Volume control |
| Left thumb + ring pinch in middle area | Next track |
| Left thumb + pinky pinch in middle area | Play / Pause |
| Two-hand pinch in middle area | Zoom in / out |

### Keyboard Shortcuts

| Key | Action |
|---|---|
| `E` | Toggle Air Mode |
| `Q` | Quit application |

---


## 🛠️ Technology Stack

- **Python** – Core programming language
- **OpenCV** – Webcam access and image processing
- **MediaPipe** – Real-time hand landmark detection
- **PyAutoGUI** – Mouse and keyboard automation

## 🏗️ System Architecture

The application follows a webcam-based gesture recognition workflow.

```text
          Webcam Input
               |
               v
       Capture Video Frames
               |
               v
        Hand Detection
               |
               v
       Hand Landmark Tracking
               |
               v
       Gesture Recognition
               |
               v
       Gesture Interpretation
               |
       +-------+---------+
       |       |         |
       v       v         v
     Mouse   Media     System
    Actions  Controls  Controls
       |       |         |
       v       v         v
    Cursor   Play /    Volume /
    Click    Pause     Zoom
    Scroll   Next      Control
       |
       v
  Computer Interaction
```

---

## 📂 Project Structure

```text
Hand-tracking-mouse-controller/
│
├── webcam_basic.py       # Main Python application
│
├── requirements.txt      # Python dependencies
│
├── README.md             # Project documentation
│
├── LICENSE               # MIT License
│
└── .gitignore            # Git ignored files
```

---

## ⚙️ Installation & Setup

### Prerequisites

Make sure you have:

- Python 3.10
- A working webcam
- pip package manager
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Jay-Samayamanthula/Hand-tracking-mouse-controller.git
```

### 2. Navigate to the project directory

```bash
cd Hand-tracking-mouse-controller
```

### 3. Create a virtual environment

```bash
python -m venv handenv
```

### 4. Activate the virtual environment

**Windows:**

```bash
handenv\Scripts\activate
```

**Linux / macOS:**

```bash
source handenv/bin/activate
```

### 5. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Run the application

```bash
python webcam_basic.py
```

Make sure your webcam is connected and accessible before starting the application.

---


## 🖼️ Project Preview

<p align="center">
  <img src="Hand Gesture Mouse Controller Demo.png"
       alt="Illustrative preview of webcam-based hand gesture recognition"
       width="850">
</p>

<p align="center">
  <i>Illustrative representation of webcam-based hand gesture recognition and computer control.</i>
</p>


## 💡 Applications

This project demonstrates potential applications in:

- Touch-free computer interaction.
- Human-computer interaction (HCI).
- Gesture-based accessibility interfaces.
- Computer vision applications.
- Desktop automation.
- Interactive control systems.

---

## 🔮 Future Enhancements

Potential improvements for the project include:

- Improved gesture recognition accuracy.
- Customizable gesture configurations.
- Support for additional hand gestures.
- Better gesture detection in different lighting conditions.
- Gesture-based keyboard controls.
- Multi-application gesture customization.
- Improved gesture response time.
- User-configurable sensitivity settings.

---

## 📜 License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Jay Samayamanthula**

Computer Science Graduate | Software Developer | AI & Technology Enthusiast

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Jay-Samayamanthula)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jay-samayamanthula/)

---

<div align="center">

### 🖐️ Turning Hand Gestures Into Digital Actions.

**Built with Python and Computer Vision.**

</div>
