// Example: src/App.js
import { useEffect, useState } from 'react'

function App() {
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetch('/hello')
      .then(res => res.json())
      .then(data => setMessage(data.message))
  }, [])

  return <h1>{message}</h1>
}

export default App