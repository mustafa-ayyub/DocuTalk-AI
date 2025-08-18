import { useEffect, useState } from 'react'
import axios from 'axios'

export default function App() {
  const [status, setStatus] = useState('loading...')

  useEffect(() => {
    axios.get('/api/health').then(r => setStatus(r.data.status)).catch(() => setStatus('error'))
  }, [])

  return (
    <div style={{ maxWidth: 800, margin: '2rem auto', fontFamily: 'system-ui, sans-serif' }}>
      <h1>DocuTalk</h1>
      <p>Backend status: {status}</p>

      <section style={{ marginTop: '2rem' }}>
        <h2>Next steps</h2>
        <ol>
          <li>Implement login/register to get a user_id</li>
          <li>Upload files to /api/files/process (multipart)</li>
          <li>Ask questions with /api/chat/ask</li>
        </ol>
      </section>
    </div>
  )
}

