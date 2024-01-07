import logo from "./logo.svg";
import { Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Home from "./shared/pages/Home";
import PageNotFound from "./shared/pages/404";
import MainNavigation from "./shared/components/Navigation/MainNavigation";
import Jobs from "./opportunities/pages/Jobs";
import Browse from "./staff/pages/Browse";

function App() {
  return (
    <>
      <MainNavigation />

      <main className="container-xl">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/staff" element={<Browse />} />

          <Route path="/*" element={<PageNotFound />} />
        </Routes>
      </main>
    </>
  );
}

export default App;
