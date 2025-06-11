import './App.css'
import React, { useEffect, useState } from "react";
import { getVideos, createVideo, deleteVideo, updateVideo } from "./api";

function App() {
  const [videos, setVideos] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [url, setUrl] = useState("");

  // ✅ Переименовали prompt → aiPrompt
  const [aiPrompt, setAiPrompt] = useState("");
  const [reply, setReply] = useState("");

  useEffect(() => {
    fetchVideos();
  }, []);

  const fetchVideos = async () => {
    const data = await getVideos();
    setVideos(data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newVideo = {
      title: title.trim(),
      description: description.trim(),
      url: url.trim(),
    };
    await createVideo(newVideo);
    setTitle("");
    setDescription("");
    setUrl("");
    fetchVideos();
  };

  const handleDelete = async (id) => {
    await deleteVideo(id);
    fetchVideos();
  };

  const handleUpdate = async (video) => {
    // ✅ Используем window.prompt
    const updated = {
      title: window.prompt("Новое название:", video.title) || video.title,
      description: window.prompt("Новое описание:", video.description) || video.description,
      url: window.prompt("Новый URL:", video.url) || video.url,
    };
    await updateVideo(video.id, updated);
    fetchVideos();
  };

  const sendPrompt = async () => {
    if (!aiPrompt.trim()) return;

    try {
      const res = await fetch("http://localhost:8000/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: aiPrompt }),
      });
      const data = await res.json();
      setReply(data.response);
    } catch (error) {
      console.error("Ошибка при отправке промпта:", error);
      setReply("Произошла ошибка при запросе.");
    }
  };

  return (
    <>
      <h1 className="main-title">🎥 TikTok Video Manager</h1>
      <form className="video-form" onSubmit={handleSubmit}>
        <input className="input" type="text" placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
        <input className="input" type="text" placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} required />
        <input className="input" type="text" placeholder="URL" value={url} onChange={(e) => setUrl(e.target.value)} required />
        <button className="add-btn" type="submit">Add Video</button>
      </form>

      <h2 className="list-title">📋 Videos List</h2>
      <div className="videos-list">
        {videos.map((video) => (
          <div className="video-card" key={video.id}>
            <div className="video-header">
              <strong className="video-title">{video.title}</strong>
            </div>
            <div className="video-desc">{video.description}</div>
            <div className="video-url">🌐 <a href={video.url} target="_blank" rel="noopener noreferrer">{video.url}</a></div>
            <div className="video-actions">
              <button className="delete-btn" onClick={() => handleDelete(video.id)}>Удалить</button>
              <button className="update-btn" onClick={() => handleUpdate(video)}>Обновить</button>
            </div>
          </div>
        ))}
      </div>

      <h2 className="list-title">🤖 Gemini Assistant</h2>
      <div className="assistant-block">
        <textarea
          className="input"
          placeholder="Задай вопрос ИИ..."
          value={aiPrompt}
          onChange={(e) => setAiPrompt(e.target.value)}
        />
        <button className="add-btn" onClick={sendPrompt}>Отправить</button>
        {reply && (
          <div className="reply-box">
            <strong>Ответ:</strong>
            <p>{reply}</p>
          </div>
        )}
      </div>
    </>
  );
}

export default App;
