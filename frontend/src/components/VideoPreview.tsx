const VideoPreview = ({ videoUrl }: { videoUrl: string }) => {
  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold mb-4">Generated Video:</h2>
      {videoUrl ? (
        <video controls className="w-full max-w-4xl mx-auto border rounded-lg">
          <source src={videoUrl} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      ) : (
        <p>No video generated yet.</p>
      )}
    </div>
  );
};

export default VideoPreview;
