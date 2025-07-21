import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

export const generateSql = async ({ prompt, model, user_id }) => {
  const response = await axios.post(`${API_BASE_URL}/generate-sql`, {
    prompt,
    model,
    user_id: user_id || 1
  });
  return response.data;
};

export const createDashboard = async ({ prompt, model, user_id }) => {
  const response = await axios.post(`${API_BASE_URL}/generate_dashboard/`, {
    prompt,
    model,
    user_id: user_id || 1
  });
  return response.data;
};

export const explainData = async ({ question, data, model }) => {
  const response = await axios.post(`${API_BASE_URL}/explain-data/`, {
    question,
    data,
    model
  });
  return response.data;
};

export const getQueryHistory = async () => {
  const response = await axios.get(`${API_BASE_URL}/query-history/`);
  return response.data;
};

export const updateLLMPreference = async (modelId) => {
  const response = await axios.post(`${API_BASE_URL}/update-preference/`, {
    model: modelId
  });
  return response.data;
};