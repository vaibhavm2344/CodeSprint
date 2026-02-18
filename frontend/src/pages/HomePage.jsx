import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";

const fallbackLanguages = [
  { value: "javascript", label: "JavaScript" },
  { value: "cpp", label: "C++" },
  { value: "java", label: "Java" },
  { value: "python", label: "Python" },
];

const times = [
  { value: 30, label: "30s" },
  { value: 60, label: "60s" },
  { value: 120, label: "120s" },
];

const HomePage = () => {
  const navigate = useNavigate();
  const [language, setLanguage] = useState("");
  const [time, setTime] = useState(30);
  const [languages, setLanguages] = useState([]);
  const [languagesError, setLanguagesError] = useState("");
  const [loadingLanguages, setLoadingLanguages] = useState(true);

  useEffect(() => {
    let active = true;
    const loadLanguages = async () => {
      try {
        setLoadingLanguages(true);
        setLanguagesError("");
        const res = await api.get("/languages");
        if (!active) return;
        const data = Array.isArray(res.data) ? res.data : [];
        console.log(data)
        if (data.length > 0) {
          setLanguages(data);
          setLanguage(data[0].name);
        } else {
          setLanguages([]);
          setLanguage(fallbackLanguages[0].value);
        }
      } catch (err) {
        console.error(err);
        if (!active) return;
        setLanguages([]);
        setLanguage(fallbackLanguages[0].value);
        setLanguagesError(
          "Using default languages because backend languages could not be loaded.",
        );
      } finally {
        if (active) setLoadingLanguages(false);
      }
    };

    loadLanguages();
    return () => {
      active = false;
    };
  }, []);

  const handleStart = () => {
    if (!language) return;

    navigate("/practice", {
      state: {
        language,
        timeLimit: Number(time),
      },
    });
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        <div className="rounded-xl shadow-lg p-8 space-y-6 bg-slate-900 border border-slate-800">
          <div className="text-center space-y-2">
            <h1 className="text-2xl font-semibold text-white/80">
              CodeSprint Typing Practice
            </h1>
            <p className="text-sm text-gray-500">
              Practice real-world code with focused timed sessions.
            </p>
          </div>

          <div className="space-y-4">
            <div className="space-y-1">
              <label className="block text-sm font-medium text-slate-300">
                Language
              </label>
              <select
                className="block w-full rounded-lg border border-gray-300 bg-slate-300 px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
              >
                {languages.length > 0
                  ? languages.map((lang) => (
                      <option key={lang.id} value={lang.name}>
                        {lang.display_name}
                      </option>
                    ))
                  : fallbackLanguages.map((lang) => (
                      <option key={lang.value} value={lang.value}>
                        {lang.label}
                      </option>
                    ))}
              </select>
              {languagesError && (
                <p className="text-xs text-red-400 mt-1">{languagesError}</p>
              )}
            </div>

            <div className="space-y-1">
              <label className="block text-sm font-medium text-slate-300">
                Time Limit
              </label>
              <select
                className="block w-full rounded-lg border border-gray-300 bg-slate-300 px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                value={time}
                onChange={(e) => setTime(Number(e.target.value))}
              >
                {times.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button
            type="button"
            onClick={handleStart}
            className="w-full rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 focus-visible:ring-offset-white"
            disabled={!language}
          >
            Start Practice
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
