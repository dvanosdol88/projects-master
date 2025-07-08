import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [msg, setMsg] = useState('');

  useEffect(() => {
    axios.get('http://localhost:5000/')
      .then(res => setMsg(res.data))
      .catch(err => console.error(err));
  }, []);

  return <div>{msg}</div>;
}

export default App;
