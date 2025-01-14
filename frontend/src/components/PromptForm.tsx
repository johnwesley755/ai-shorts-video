import React, { useState, useEffect } from "react";
import axios from "axios";

const PromptForm = ({
  setVideoUrl,
}: {
  setVideoUrl: React.Dispatch<React.SetStateAction<string>>;
}) => {
  // Retrieve saved prompt from localStorage, if it exists
  const savedPrompt = localStorage.getItem("prompt") || "";
  const [prompt, setPrompt] = useState<string>(savedPrompt);
  const [loading, setLoading] = useState(false);

  // Save prompt to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem("prompt", prompt);
  }, [prompt]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:5000/generate", {
        prompt,
      });
      setVideoUrl(response.data.video_url);
    } catch (error: any) {
  console.error("Error generating video:", error);
  alert(`Error: ${error.response?.data?.error || "An unknown error occurred."}`);
}
 {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-10">
      <h1 className="text-3xl font-semibold text-center">
        AI Shorts Video Generator
      </h1>
      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <textarea
          className="w-full p-4 border border-gray-300 rounded-lg"
          rows={5}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter a prompt to generate a video"
        />
        <button
          type="submit"
          className="w-full py-2 bg-blue-600 text-white font-semibold rounded-lg"
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate Video"}
        </button>
      </form>
    </div>
  );
};

export default PromptForm;
