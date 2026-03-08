import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export function useApi() {
  const startSimulation = async (config) => {
    try {
      const response = await axios.post(`${API_URL}/api/start`, config);
      return response.data;
    } catch (error) {
      throw error;
    }
  };

  const getResults = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/results`);
      return response.data;
    } catch (error) {
      throw error;
    }
  };

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await axios.post(`${API_URL}/api/upload`, formData);
      return response.data;
    } catch (error) {
      throw error;
    }
  };

  return {
    startSimulation,
    getResults,
    uploadFile
  };
}