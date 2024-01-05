import logo from "./logo.svg";
import { Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Home from "./shared/pages/Home";
import PageNotFound from "./shared/pages/404";
import MainNavigation from "./shared/components/Navigation/MainNavigation";
import Jobs from "./opportunities/pages/Jobs";

function App() {
  return (
    <>
      <MainNavigation />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/jobs" element={<Jobs />} />

        <Route path="/*" element={<PageNotFound />} />
      </Routes>
    </>
  );
}

export default App;
