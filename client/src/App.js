// Example: src/App.js
import { useEffect, useState } from 'react'

function App() {
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetch('/hello')
      .then(res => res.json())
      .then(data => setMessage(data.message))
  }, [])

  return <h1 className="text-3xl text-red-800 font-bold underline">{message}</h1>
}

export default App