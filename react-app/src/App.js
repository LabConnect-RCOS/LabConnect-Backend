import logo from "./logo.svg";
import { Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Home from "./shared/pages/Home";
import PageNotFound from "./shared/pages/404";
import MainNavigation from "./shared/components/Navigation/MainNavigation";
import Jobs from "./opportunities/pages/Jobs";
import Browse from "./staff/pages/Browse";
import Profile from "./staff/pages/Profile";
import Center from "./staff/pages/Center";

function App() {
  return (
    <>
      <MainNavigation />

      <main className="container-xl">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/staff" element={<Browse />} />
          <Route path="/center/:centerName" element={<Center />} />
          <Route path="/staff/:staffId" element={<Profile />} />

          <Route path="/*" element={<PageNotFound />} />
        </Routes>
      </main>
    </>
  );
}

export default App;
