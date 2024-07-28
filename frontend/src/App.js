import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [flights, setFlights] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/flights')
      .then(response => response.json())
      .then(data => {
        console.log('Fetched data:', data);  
        setFlights(data);
      })
      .catch(error => {
        console.error('Error fetching flight data:', error);
        setError(error);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Flight Status Updates</h1>
      </header>
      <main>
        {error && <p>Error fetching data: {error.message}</p>}
        {flights.length > 0 ? (
          <ul>
            {flights.map((flight, index) => (
              <li key={index}>
                <strong>Flight Number:</strong> {flight.flightNumber} <br />
                <strong>Airline:</strong> {flight.airline || "N/A"} <br />
                <strong>Status:</strong> {flight.status} <br />
                <strong>Gate:</strong> {flight.gate} <br />
                <strong>Departure:</strong> {flight.departure} <br />
                <strong>Time:</strong> {flight.Time} <br />
              </li>
            ))}
          </ul>
        ) : (
          <p>No flight data available.</p>
        )}
      </main>
    </div>
  );
}

export default App;
