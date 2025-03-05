import { useState } from "react";

export default function SearchBar() {
  const [query, setQuery] = useState<String>('');
  const SERVER = "http://127.0.0.1:5000"

  async function makeQuery() {
    const currentQuery = query.replace(/ /g, '+')
    const promise = await fetch(`${SERVER}/most-relevant?query=${currentQuery}`)
    const response = await promise.json()
    console.log(response)
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
