import { useState } from "react";

export default function SearchBar({setLinks, setTime}) {
  const [query, setQuery] = useState<string>('')
  const SERVER = "https://cs121-a3-zr0a.onrender.com"
  async function makeQuery() {
    try {
      const currentQuery = query.replace(/ /g, '+')
      const promise = await fetch(`${SERVER}/most-relevant?query=${currentQuery}`)
      const response = await promise.json()
      setLinks(response.Results)
      setTime(response.RetrievalTime)

      console.log(response)
    } catch (error) {
      console.log("Encountered Error in MakeQuery:", error)
    }
  }

  return (
    <div>
      <div className="input-group">
        <input
          type="text"
          className="form-control rounded"
          placeholder="Search"
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          type="button"
          className="btn btn-outline-primary"
          data-mdb-ripple-init
          onClick={() => {
            makeQuery()
          }}
        >
          search
        </button> 

      </div>
    </div>
  );
}
