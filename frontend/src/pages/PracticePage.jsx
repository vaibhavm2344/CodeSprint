import React from "react";
import { useLocation } from "react-router-dom";
import { useTypingSnippet } from "../hooks/useTypingSnippet";
import { TypingSnippetEditor } from "../components/TypingSnippetEditor";

const PracticePage = () => {
  const { state } = useLocation();
  const initialTimeLimit = state?.timeLimit || 30;
  const language = state?.language || "python";

  const {
    snippet,
    typed,
    wpm,
    accuracy,
    correctCount,
    totalTyped,
    handleKeyDown,
    isFinished,
    elapsedMs,
    timeLeftMs,
  } = useTypingSnippet(initialTimeLimit, language);

  const handlePrevent = (event) => {
    event.preventDefault();
  };

  const formatTime = (ms) => {
    if (ms < 0) ms = 0;
    const totalSeconds = Math.ceil(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-4">
      <div className="w-full max-w-4xl space-y-6">
        <header className="flex items-center justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-slate-400">
              CodeSprint · Typing Practice
            </p>
            <p className="text-sm text-slate-400">
              Practice with real code-style snippets.
            </p>
          </div>
          <div className="flex gap-4 text-xs text-slate-300">
            <div>
              <p className="uppercase tracking-[0.2em] text-slate-500">
                {isFinished ? "Time" : "Remaining"}
              </p>
              <p className="text-lg font-semibold text-slate-100">
                {formatTime(isFinished ? elapsedMs : timeLeftMs)}
              </p>
            </div>
            <div>
              <p className="uppercase tracking-[0.2em] text-slate-500">WPM</p>
              <p className="text-lg font-semibold text-slate-100">{wpm}</p>
            </div>
            <div>
              <p className="uppercase tracking-[0.2em] text-slate-500">
                Accuracy
              </p>
              <p className="text-lg font-semibold text-slate-100">
                {accuracy}%
              </p>
            </div>
          </div>
        </header>

        <TypingSnippetEditor
          snippet={snippet}
          typed={typed}
          onKeyDown={handleKeyDown}
          onPrevent={handlePrevent}
        />

        <div className="flex justify-between text-xs text-slate-500">
          <span>
            Typed: <span className="font-medium">{totalTyped}</span>
          </span>
          <span>
            Correct: <span className="font-medium">{correctCount}</span>
          </span>
        </div>

        {isFinished && (
          <div className="mt-4 p-4 rounded-lg bg-slate-900 border border-slate-800 text-center animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h3 className="text-xl font-bold text-slate-100 mb-2">Practice Complete!</h3>
            <div className="flex justify-center gap-8">
              <div>
                <p className="text-sm text-slate-400 uppercase tracking-wider">WPM</p>
                <p className="text-3xl font-bold text-emerald-400">{wpm}</p>
              </div>
              <div>
                <p className="text-sm text-slate-400 uppercase tracking-wider">Accuracy</p>
                <p className="text-3xl font-bold text-emerald-400">{accuracy}%</p>
              </div>
              <div>
                <p className="text-sm text-slate-400 uppercase tracking-wider">Time</p>
                <p className="text-3xl font-bold text-slate-200">{formatTime(elapsedMs)}</p>
              </div>
            </div>
            <button
              onClick={() => window.location.reload()}
              className="mt-6 px-6 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-md font-medium transition-colors"
            >
              Try Another
            </button>
          </div>
        )}

      </div>
    </div>
  );
};

export default PracticePage;

