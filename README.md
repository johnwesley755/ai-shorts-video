# 🎥 AI Shorts Video Generator

Welcome to the **AI Shorts Video Generator**! This project allows users to generate creative short videos instantly by simply providing a prompt. It leverages AI technology to bring your ideas to life with video content!

## 🚀 Features

- **Simple Prompt Input**: Just describe your video idea, and our AI will do the rest!
- **Instant Video Generation**: Get a video preview in no time, ready to share.
- **Responsive UI**: Optimized for both desktop and mobile views.
- **Smooth User Experience**: Clean design with easy navigation.

## ⚙️ Technology Stack

- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: Flask (Python)
- **Video Generation**: AI-based model hosted on Flask API
- **State Management**: React's `useState` and `useEffect`
- **Video Playback**: HTML5 `<video>` tag

## 📦 Prerequisites

Before running this project, ensure you have the following installed:

- Node.js (v14 or higher)
- npm (v6 or higher)
- Python (v3.7 or higher)
- Flask (Python package)

## 🏁 Getting Started

Follow these steps to get this project up and running locally.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-shorts-video-generator.git
cd ai-shorts-video-generator
```

### 2. Install dependencies

- **Frontend**:
    1. Navigate to the `frontend` folder:
    ```bash
    cd frontend
    ```
    2. Install the required packages:
    ```bash
    npm install
    ```

- **Backend**:
    1. Navigate to the `backend` folder:
    ```bash
    cd ../backend
    ```
    2. Install Flask and any necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Run the application

- **Frontend**:
    1. Navigate back to the `frontend` folder:
    ```bash
    cd frontend
    ```
    2. Start the frontend React app:
    ```bash
    npm start
    ```

- **Backend**:
    1. Navigate to the `backend` folder:
    ```bash
    cd backend
    ```
    2. Start the Flask server:
    ```bash
    python app.py
    ```

Now you can visit the frontend app in your browser at `http://localhost:5173` and interact with the video generator!

## 🌟 Project Demo

Check out the video generator in action! You can enter a prompt, generate a video, and view the results instantly.

## 📸 Screenshots

![Video Generator App Screenshot](./screenshots/video-generator.png)

## 📄 How it Works

1. **User Input**: The user enters a prompt describing their desired video idea.
2. **AI Model**: The backend processes the prompt and uses an AI model to generate a video.
3. **Preview**: The video is sent back to the frontend, where it is displayed for the user to view and download.

## 🔧 Backend Setup

To ensure that the backend API works seamlessly, the Flask server is set up to receive a `POST` request with a prompt and return a generated video URL. The backend uses a Python-based AI model (you can use any AI-based video generation model you prefer).

### Example request:
```json
{
  "prompt": "A futuristic city with flying cars"
}
```

### Example response:
```json
{
  "videoUrl": "http://example.com/generated-video.mp4"
}
```

## 📝 LocalStorage Persistence

- The user prompt is saved in the browser's `localStorage`, ensuring that your previous input is preserved even after refreshing the page.

## 📣 Contributing

We welcome contributions to improve the AI Shorts Video Generator! Feel free to fork this repository, submit issues, and create pull requests.

### How to contribute:

1. Fork this repo
2. Create a new branch (`git checkout -b feature-name`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to your branch (`git push origin feature-name`)
6. Create a new pull request

---

This should now be more concise and focused on the setup and usage. Let me know if you need any further modifications!
