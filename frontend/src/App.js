import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [worlds, setWorlds] = useState([]);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost';

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const worldsRes = await fetch(${apiUrl}/example/api/worlds);
      const studentsRes = await fetch(${apiUrl}/example/api/students);
      
      setWorlds(await worldsRes.json());
      setStudents(await studentsRes.json());
      setLoading(false);
    } catch (error) {
      console.error('Error:', error);
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌍 BTEC Virtual World</h1>
        <p>Full-Stack Microservices Platform</p>

        {loading ? (
          <p>Loading...</p>
        ) : (
          <>
            <section className="worlds-section">
              <h2>Virtual Worlds</h2>
              <div className="cards">
                {worlds.worlds && worlds.worlds.map(world => (
                  <div key={world.id} className="card">
                    <h3>{world.name}</h3>
                    <p>👥 {world.students} students</p>
                    <p className="status">{world.status}</p>
                  </div>
                ))}
              </div>
            </section>

            <section className="students-section">
              <h2>Top Students</h2>
              <div className="cards">
                {students.students && students.students.map(student => (
                  <div key={student.id} className="card">
                    <h3>{student.name}</h3>
                    <p>Level {student.level}</p>
                    <p>⭐ {student.points} points</p>
                  </div>
                ))}
              </div>
            </section>
          </>
        )}
      </header>
    </div>
  );
}

export default App;
