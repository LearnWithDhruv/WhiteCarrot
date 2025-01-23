import axios from 'axios';

const API = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL,
});

export const loginWithGoogle = async (token) => {
    return await axios.post(`${process.env.REACT_APP_BACKEND_URL}/auth/login/`, { token });
  };
  

export const fetchCalendarEvents = async () => {
    return API.get('/calendar/events/');
  };

export const postCalendarEvent = async (eventData) => {
    return API.post('/calendar/events/', eventData);
  };