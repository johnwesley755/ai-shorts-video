import React, { useState } from "react";
import PromptForm from "./components/PromptForm";
import VideoPreview from "./components/VideoPreview";

const App = () => {
  const [videoUrl, setVideoUrl] = useState("");

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-12">
      <PromptForm setVideoUrl={setVideoUrl} />
      <VideoPreview videoUrl={videoUrl} />
    </div>
  );
};

export default App;
