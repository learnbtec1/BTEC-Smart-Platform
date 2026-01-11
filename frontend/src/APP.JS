import React from 'react';
import ChatInterface from './components/ChatComponent'; // استدعاء المكون
import 'antd/dist/reset.css'; // استدعاء تنسيقات Ant Design (مهم جداً)

function App() {
  return (
    <div className="App">
      <ChatInterface />
    </div>
  );
}

export default App;