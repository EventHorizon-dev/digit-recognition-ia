# 2D Handwritten Digit Recognition IA

This project features a Neural Network trained on the famous MNIST dataset to recognize handwritten digits, combined with a custom graphical user interface (GUI) for live testing.

## Features
* **Neural Network:** Built with Keras (Sequential API) using Dense layers and the Adam optimizer.
* **Live Drawing GUI:** A Tkinter-based interface allowing users to draw digits with their mouse on a digital canvas.
* **Real-time Reinforcement:** Includes a correction system where the user can teach the AI the correct answer if it guesses wrong. The model updates and saves its weights immediately using `train_on_batch`.

## Installation & Usage

### 1. Install Dependencies
Open your terminal or command prompt and install the required Python libraries:
\`\`\`bash
pip install keras numpy pillow matplotlib
\`\`\`

### 2. Train the AI Model
Run the training script first. This will automatically download the MNIST dataset, train the neural network, evaluate its accuracy, and save the trained model:
\`\`\`bash
python "réseau neuronal from scratch.py"
\`\`\`
Once completed, a file named `mon_modele_ia.keras` will be created in your folder.

### 3. Launch the Interface
Once the model file is generated, you can launch the drawing interface to test the AI live:
\`\`\`bash
python "interface IA.py"
\`\`\`

## How it Works
1. **Drawing:** Draw any digit from 0 to 9 on the canvas.
2. **Prediction:** Click **"Deviner"** (Guess) to let the AI process the image (resizing it to 28x28 pixels and inverting colors to match the training data) and output its guess in the terminal.
3. **Correction:** If the AI makes a mistake, click on the correct number button below the canvas. The AI will instantly train on your drawing and update its memory!
