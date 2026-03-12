import axios from 'axios';
const API_URL = '/api';
export const debateApi = {
  startDebate: async (topic, rounds = 3) => {
    const response = await axios.post(`${API_URL}/debate/start`, { topic, rounds });
    return response.data;
  },
  executeRound: async (sessionId) => {
    const response = await axios.post(`${API_URL}/debate/${sessionId}/round`);
    return response.data;
  },
  getJudgment: async (sessionId) => {
    const response = await axios.post(`${API_URL}/debate/${sessionId}/judge`);
    return response.data;
  },
  getDebate: async (sessionId) => {
    const response = await axios.get(`${API_URL}/debate/${sessionId}`);
    return response.data;
  }
};