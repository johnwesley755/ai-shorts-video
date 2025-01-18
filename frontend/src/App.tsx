import React, { useState, useEffect } from "react";
import axios from "axios";

const VideoGeneratorApp = () => {
  const savedPrompt = localStorage.getItem("prompt");
  const [prompt, setPrompt] = useState<string>(savedPrompt || "");
  const [videoUrl, setVideoUrl] = useState<string>(""); // Video URL resets on refresh
  const [downloadUrl, setDownloadUrl] = useState<string>(""); // Download URL for the generated video
  const [loading, setLoading] = useState<boolean>(false);

  // Save prompt to localStorage whenever it changes
  useEffect(() => {
    if (prompt) {
      localStorage.setItem("prompt", prompt);
    } else {
      localStorage.removeItem("prompt");
    }
  }, [prompt]);

  // Handle video generation
  const handleGenerateVideo = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/generate", {
        prompt,
      });
      console.log("Backend Response:", response.data);

      if (response.data.videoUrl && response.data.downloadUrl) {
        setVideoUrl(response.data.videoUrl);
        setDownloadUrl(response.data.downloadUrl);
      } else {
        console.error("Video or download URL not found in response.");
      }
    } catch (error) {
      console.error("Error generating video:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-200 via-purple-200 to-blue-200 p-8 font-sans relative overflow-hidden">
      {/* Gradient Shapes */}
      <div className="absolute top-10 left-20 w-40 h-40 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full animate-bounce" />
      <div className="absolute bottom-20 right-20 w-32 h-32 bg-gradient-to-br from-blue-500 to-green-500 rounded-full animate-pulse" />
      <div className="absolute top-1/3 right-1/4 w-48 h-48 bg-gradient-to-br from-yellow-500 to-red-500 rounded-lg transform rotate-45 opacity-70 animate-spin-slow" />

      <div className="max-w-5xl mx-auto text-center mb-10 relative z-10">
        <h1 className="text-6xl font-extrabold leading-tight text-purple-900 drop-shadow-md lg:mt-20">
          🎥 AI Shorts Video Generator
        </h1>
        <p className="text-2xl mt-4 text-purple-700">
          Generate creative short videos instantly by entering a simple prompt.
        </p>
      </div>

      <div className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 relative z-10">
        <div className="bg-gradient-to-br from-white to-gray-100 p-8 rounded-2xl shadow-2xl relative border">
          <h2 className="text-4xl font-extrabold text-center tracking-normal text-purple-900 mb-6">
            Enter Your Prompt
          </h2>
          <form onSubmit={handleGenerateVideo} className="space-y-4">
            <textarea
              className="w-full p-5 border bg-white text-gray-800 rounded-lg focus:outline-none focus:ring-4 focus:ring-purple-400 transition-all shadow-lg"
              rows={6}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe your video idea here..."
            />
            <button
              type="submit"
              className={`w-full py-4 font-bold text-lg rounded-full transition duration-300 transform hover:scale-105 shadow-lg ${
                loading
                  ? "bg-purple-300 text-purple-800 cursor-not-allowed"
                  : "bg-gradient-to-br from-purple-600 to-indigo-600 text-white hover:from-indigo-700 hover:to-purple-700"
              }`}
              disabled={loading}
            >
              {loading ? "Generating..." : "Generate Video"}
            </button>
          </form>
        </div>

        <div className="bg-gradient-to-br from-white to-gray-100 p-8 rounded-2xl shadow-2xl relative border">
          <h2 className="text-4xl font-extrabold tracking-normal text-center text-purple-900 mb-6">
            Generated Video Preview
          </h2>
          <div
            className={`p-6 border-4 rounded-lg shadow-lg transition-all relative overflow-hidden ${
              videoUrl
                ? "border-green-500 bg-white"
                : "border-gray-300 bg-gray-200 text-gray-500"
            }`}
          >
            {videoUrl ? (
              <div className="relative flex flex-col justify-center items-center space-y-4">
                <video
                  controls
                  className="w-full md:w-3/4 lg:w-2/3 mx-auto rounded-lg shadow-lg border-2 border-purple-400"
                >
                  <source src={videoUrl} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
                <a
                  href={downloadUrl}
                  download
                  className="mt-4 inline-block bg-gradient-to-br from-green-500 to-teal-500 text-white py-3 px-6 rounded-lg font-bold shadow-lg transform transition duration-300 hover:scale-105"
                >
                  Download Video
                </a>
              </div>
            ) : (
              <p className="text-center text-xl">No video available yet.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoGeneratorApp;
