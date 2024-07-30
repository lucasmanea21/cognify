import axios from 'axios';
import { API_URL } from '../shared/config';


export const startFocusSession = async () => {
    try {
      const response = await axios.post(`${API_URL}/start_focus`);
      return response.data.session_id;
    } catch (error) {
      console.error('Error starting focus session:', error);
      throw new Error('Failed to start focus session');
    }
  };
  
  export const stopFocusSession = async () => {
    try {
      await axios.post(`${API_URL}/stop_focus`);
    } catch (error) {
      console.error('Error stopping focus session:', error);
      throw new Error('Failed to stop focus session');
    }
  };

  export const startMindControl = async (): Promise<void> => {
    await axios.post(`${API_URL}/start_stream`);
  };
  
  export const stopMindControl = async (): Promise<void> => {
    await axios.post(`${API_URL}/stop_stream`);
  };
  
export const getData = async () => {
    try {
      const response = await axios.get(`${API_URL}/get_data`);
      return response.data;
    } catch (error) {
      console.error('Error getting data:', error);
      throw error;
    }
  };