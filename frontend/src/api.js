import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // адрес твоего backend

export const getVideos = async () => {
  const response = await axios.get(`${API_BASE_URL}/videos/`);
  return response.data;
};

export const createVideo = async (videoData) => {
  console.log("Sending video:", videoData); // <--- добавь
  const response = await axios.post(`${API_BASE_URL}/videos/`, videoData);
  return response.data;
};


export const deleteVideo = async (id) => {
  await axios.delete(`${API_BASE_URL}/videos/${id}`);
};

export const updateVideo = async (id, data) => {
  const response = await axios.put(`${API_BASE_URL}/videos/${id}`, data);
  return response.data;
};

