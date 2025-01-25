import React, { useState, useEffect } from 'react';
import { fetchCalendarEvents, postCalendarEvent } from '../services/api'; // Backend API calls

const Calendar = () => {
    const [events, setEvents] = useState([]);
    const [newEvent, setNewEvent] = useState({
        summary: '',
        date: '',
        time: '',
        location: '',
    });
    const [error, setError] = useState('');

    useEffect(() => {
        loadEvents();
    }, []);

    const loadEvents = async () => {
        try {
            const response = await fetchCalendarEvents();
            setEvents(response.data || []); 
        } catch (error) {
            console.error('Failed to fetch events:', error);
            setError('Failed to load events');
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewEvent(prev => ({ ...prev, [name]: value }));
        setError(''); 
    };

    const resetForm = () => {
        setNewEvent({
            summary: '',
            date: '',
            time: '',
            location: '',
        });
    };

    const validateEvent = () => {
        if (!newEvent.summary.trim()) {
            setError('Event title is required');
            return false;
        }
        if (!newEvent.date) {
            setError('Date is required');
            return false;
        }
        if (!newEvent.time) {
            setError('Time is required');
            return false;
        }
        return true;
    };

    const handleAddEvent = async () => {
        setError('');

        if (!validateEvent()) {
            return;
        }

        try {
            const eventDateTime = new Date(`${newEvent.date}T${newEvent.time}`);
            
            const eventToAdd = {
                summary: newEvent.summary.trim(),
                location: newEvent.location.trim() || null,
                dateTime: eventDateTime.toISOString(),
            };

            const response = await postCalendarEvent(eventToAdd);

            if (response && (response.status === 200 || response.status === 201)) {
                await loadEvents();
                
                // Reset the form
                resetForm();
                
                setError('Event added successfully!');
            } else {
                throw new Error('Unexpected response from server');
            }
        } catch (error) {
            console.error('Error in handleAddEvent:', error);
            setError('Failed to add event. Please try again.');
        }
    };

    return (
        <div>
            <h1>Google Calendar Events</h1>
            
            {/* Error Message Display */}
            {error && (
                <div style={{ 
                    color: error.includes('successfully') ? 'green' : 'red', 
                    marginBottom: '10px' 
                }}>
                    {error}
                </div>
            )}

            <div style={{ marginBottom: '20px' }}>
                <input
                    type="text"
                    name="summary"
                    placeholder="Event Title"
                    value={newEvent.summary}
                    onChange={handleInputChange}
                    style={{ marginRight: '10px', padding: '5px' }}
                />
                <input
                    type="date"
                    name="date"
                    placeholder="Date"
                    value={newEvent.date}
                    onChange={handleInputChange}
                    style={{ marginRight: '10px', padding: '5px' }}
                />
                <input
                    type="time"
                    name="time"
                    placeholder="Time"
                    value={newEvent.time}
                    onChange={handleInputChange}
                    style={{ marginRight: '10px', padding: '5px' }}
                />
                <input
                    type="text"
                    name="location"
                    placeholder="Location"
                    value={newEvent.location}
                    onChange={handleInputChange}
                    style={{ marginRight: '10px', padding: '5px' }}
                />
                <button onClick={handleAddEvent} style={{ padding: '5px 10px' }}>
                    Add Event
                </button>
            </div>

            <table border="1" cellPadding="10" style={{ width: '100%', textAlign: 'left' }}>
                <thead>
                    <tr>
                        <th>Event Title</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Location</th>
                    </tr>
                </thead>
                <tbody>
                    {events.map((event, index) => {
                        const eventDateTime = new Date(event.dateTime || event.date);
                        const formattedDate = eventDateTime.toLocaleDateString();
                        const formattedTime = eventDateTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                        return (
                            <tr key={index}>
                                <td>{event.summary}</td>
                                <td>{formattedDate}</td>
                                <td>{formattedTime}</td>
                                <td>{event.location || 'N/A'}</td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
};

export default Calendar;
