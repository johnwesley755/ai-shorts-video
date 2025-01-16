import React, { useState, useEffect } from "react";
import axios from "axios";

const VideoGeneratorApp = () => {
  const savedPrompt = localStorage.getItem("prompt");
  const [prompt, setPrompt] = useState<string>(savedPrompt || "");
  const [videoUrl, setVideoUrl] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  // Save prompt to localStorage whenever it changes
  useEffect(() => {
    if (prompt) localStorage.setItem("prompt", prompt);
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

      if (response.data.videoUrl) {
        setVideoUrl(response.data.videoUrl);
      } else {
        console.error("Video URL not found in response.");
      }
    } catch (error) {
      console.error("Error generating video:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-800 to-black p-8 text-white font-sans">
      <div className="max-w-5xl mx-auto text-center mb-10">
        <h1 className="text-5xl font-extrabold leading-tight text-indigo-100 lg:mt-20">
          🎥 AI Shorts Video Generator
        </h1>
        <p className="text-xl mt-4 text-gray-300">
          Generate creative short videos instantly by entering a simple prompt.
        </p>
      </div>

      <div className="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-10">
        <div className="bg-gradient-to-br from-gray-800 to-gray-900 p-8 rounded-2xl shadow-2xl relative border">
          <h2 className="text-3xl font-bold text-center tracking-wide text-indigo-100 mb-6">
            Enter Your Prompt
          </h2>
          <form onSubmit={handleGenerateVideo} className="space-y-2">
            <textarea
              className="w-full p-5 border bg-gray-900 text-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-300 focus:border-none transition-all"
              rows={6}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe your video idea here..."
            />
            <button
              type="submit"
              className={`w-full py-3 font-semibold text-lg rounded-lg transition duration-300 ${
                loading
                  ? "bg-indigo-300 text-indigo-800 cursor-not-allowed"
                  : "bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg hover:shadow-indigo-500/50"
              }`}
              disabled={loading}
            >
              {loading ? "Generating..." : "Generate Video"}
            </button>
          </form>
        </div>

        <div className="bg-gradient-to-br from-gray-800 to-gray-900 p-8 rounded-2xl shadow-2xl relative border">
          <h2 className="text-3xl font-bold tracking-wide text-center text-white mb-6">
            Generated Video Preview
          </h2>
          <div
            className={`p-6 border-4 rounded-lg shadow-lg transition-all ${
              videoUrl
                ? "border-green-500 bg-gray-800"
                : "border-gray-700 bg-gray-700 text-gray-400"
            }`}
          >
            {videoUrl ? (
              <div className="relative flex justify-center">
                <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-10 h-32 bg-indigo-500 rounded-lg animate-pulse"></div>
                <video
                  controls
                  className="w-full md:w-3/4 lg:w-2/3 mx-auto rounded-lg shadow-lg border-2 border-indigo-500"
                >
                  <source src={videoUrl} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
                <div className="absolute right-0 top-1/2 transform -translate-y-1/2 w-10 h-32 bg-indigo-500 rounded-lg animate-pulse"></div>
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
