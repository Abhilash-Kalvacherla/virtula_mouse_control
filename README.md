🖱️ Virtual Mouse Controller using AI & Computer Vision
📌 Overview

The Virtual Mouse Controller is an AI-powered application that allows users to control the mouse cursor using hand gestures captured through a webcam.
This project leverages Computer Vision and Machine Learning techniques to detect hand landmarks and translate gestures into mouse actions such as move, click, and scroll.

This system eliminates the need for physical mouse devices and demonstrates a practical application of AI in Human–Computer Interaction (HCI).

🚀 Features

🎥 Real-time hand detection using webcam

✋ Gesture-based mouse movement

🖱️ Left click & right click using finger gestures

🔄 Scroll functionality

⚡ Smooth and responsive cursor control

🧠 AI & Computer Vision based logic

🛠️ Technologies Used

Python

OpenCV

MediaPipe

PyAutoGUI

NumPy

📂 Project Structure
virtual_mouse_controller/
│
├── main.py                 # Main execution file
├── hand_tracking.py        # Hand landmark detection logic
├── requirements.txt        # Required Python libraries
├── README.md               # Project documentation
└── .gitignore              # Ignored files

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/virtual_mouse_controller.git
cd virtual_mouse_controller

2️⃣ Create Virtual Environment (Optional but Recommended)
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

▶️ How to Run
python main.py


📸 Ensure your webcam is connected before running the program.

🧠 How It Works

Webcam captures real-time video frames

MediaPipe detects hand landmarks

Specific finger gestures are identified

Gestures are mapped to mouse actions using PyAutoGUI

Cursor moves and performs actions accordingly

📊 Use Cases

Touchless computer interaction

Assistive technology for physically challenged users

AI-based automation demonstrations

Human–Computer Interaction projects

🔮 Future Enhancements

Multi-hand support

Gesture customization

GUI for calibration

Improved accuracy using deep learning models
