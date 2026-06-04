import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="screen-center flex-col gap-3">
      <h1 className="text-2xl font-semibold text-ink">Page not found</h1>
      <Link className="btn btn-primary" to="/dashboard">Back to dashboard</Link>
    </div>
  );
}
