import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

const ResultsPage = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const { wpm, accuracy, timeTakenInSeconds } = location.state || {};

  if (wpm == null || accuracy == null || timeTakenInSeconds == null) {
    navigate("/");
    return null;
  }

  let accuracyColor = "text-red-600";
  if (accuracy >= 90) {
    accuracyColor = "text-green-600";
  } else if (accuracy >= 70) {
    accuracyColor = "text-yellow-600";
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-xl shadow-lg p-8 space-y-6 text-center">
          <h1 className="text-xl font-semibold text-gray-900">
            Session Results
          </h1>

          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-500">Words Per Minute</p>
              <p className="mt-1 text-4xl font-bold text-gray-900">
                {Math.round(wpm)}
              </p>
            </div>

            <div>
              <p className="text-sm text-gray-500">Accuracy</p>
              <p className={`mt-1 text-2xl font-semibold ${accuracyColor}`}>
                {accuracy.toFixed(2)}%
              </p>
            </div>

            <div>
              <p className="text-sm text-gray-500">Time Taken</p>
              <p className="mt-1 text-lg font-medium text-gray-800">
                {timeTakenInSeconds}s
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={() => navigate("/")}
            className="mt-4 w-full rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 focus-visible:ring-offset-white"
          >
            Restart
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
