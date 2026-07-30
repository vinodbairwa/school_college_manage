export function BackendDown() {
  return (
    <div className="error">
      <strong>Backend API is not reachable on port 8000.</strong>
      <p className="error-text">
        Website alone is not enough. FastAPI backend must also be running.
      </p>
      <ol className="error-list">
        <li>
          From project root run: <code>npm start</code> (starts backend + website + panel)
        </li>
        <li>
          Confirm backend: open <code>http://127.0.0.1:8000/health</code>
        </li>
        <li>
          Then refresh this page. Full help: <code>LOCAL_SETUP.md</code>
        </li>
      </ol>
    </div>
  );
}
