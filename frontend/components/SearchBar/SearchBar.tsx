import { useState } from "react";

export default function SearchBar() {
  const [query, setQuery] = useState<String>();

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
            console.log("User Query:", query)
          }}
        >
          search
        </button>
      </div>
    </div>
  );
}
