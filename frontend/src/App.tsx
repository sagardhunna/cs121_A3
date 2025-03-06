import './App.css'
import SearchBar from '../components/SearchBar/SearchBar'
import { useState } from 'react'


function App() {

  const [links, setLinks] = useState<string[]>([])
  const [time, setTime] = useState()

  return (
    <>
    <div>
      <h1>Search Engine type shi</h1>
      <SearchBar setLinks={setLinks} setTime={setTime}/>
      <div>
          {links.map((link, index) => {
            return (
              <p key={index}>
                <a href={link} target="_blank" rel="noopener noreferrer">{link}</a>
              </p>
            )
          })}
      </div>
      <p>Total Time: {time}</p>
    </div>
    </>
  )
}

export default App
