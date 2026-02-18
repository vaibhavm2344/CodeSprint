import { useEffect, useRef, useState } from "react";
import { api } from "../api/client";

const MOCK_SNIPPET = `function greet(name) {
  if (!name) {
    return "Hello, world!";
  }

  return \`Hello, \${name}\`;
}

console.log(greet("Developer"));`;

export function useTypingSnippet(initialTimeLimit = 60, language = "python") {
  const [snippet, setSnippet] = useState("");
  const [typed, setTyped] = useState("");
  const [isFinished, setIsFinished] = useState(false);
  const [elapsedMs, setElapsedMs] = useState(0);
  const [timeLeftMs, setTimeLeftMs] = useState(initialTimeLimit * 1000);

  const [correctCount, setCorrectCount] = useState(0);
  const [totalTyped, setTotalTyped] = useState(0);

  const indexRef = useRef(0);
  const startTimeRef = useRef(null);
  const timerIdRef = useRef(null);

  useEffect(() => {
    // Reset state when language or time limit changes
    setTyped("");
    setIsFinished(false);
    setElapsedMs(0);
    setTimeLeftMs(initialTimeLimit * 1000);
    setCorrectCount(0);
    setTotalTyped(0);
    startTimeRef.current = null;
    if (timerIdRef.current) {
      clearInterval(timerIdRef.current);
      timerIdRef.current = null;
    }

    const fetchSnippet = async () => {
      try {
        // Append language query param if supported, otherwise just fetch
        const res = await api.get(`/code/snippets`, { params: { language } });
        if (res.status === 200) {
          const data = res.data;
          setSnippet(data?.code || MOCK_SNIPPET);
          return;
        }
      } catch (err) {
        console.error("Failed to fetch snippet from API, using mock.", err);
      }
      setSnippet(MOCK_SNIPPET);
    };

    fetchSnippet();
  }, [language, initialTimeLimit]);

  useEffect(() => {
    if (!snippet) return;

    let correct = 0;
    // Calculate correct chars by comparing typed vs snippet up to typed length
    const limit = Math.min(typed.length, snippet.length);
    for (let i = 0; i < limit; i += 1) {
      if (typed[i] === snippet[i]) {
        correct += 1;
      }
    }

    setCorrectCount(correct);
    setTotalTyped(typed.length);
    indexRef.current = typed.length;

    // Check for completion by typing
    if (typed.length >= snippet.length && snippet.length > 0 && !isFinished) {
      setIsFinished(true);
    }
  }, [snippet, typed, isFinished]);

  useEffect(() => {
    // Timer Logic
    if (typed.length === 0 || isFinished || !startTimeRef.current) {
      if (timerIdRef.current) {
        clearInterval(timerIdRef.current);
        timerIdRef.current = null;
      }
      return;
    }

    if (!timerIdRef.current) {
      timerIdRef.current = setInterval(() => {
        const now = Date.now();
        const diff = now - startTimeRef.current;
        setElapsedMs(diff);

        // Calculate countdown
        const remaining = (initialTimeLimit * 1000) - diff;
        if (remaining <= 0) {
          setTimeLeftMs(0);
          setElapsedMs(initialTimeLimit * 1000);
          setIsFinished(true);
          // Stop timer
          if (timerIdRef.current) {
            clearInterval(timerIdRef.current);
            timerIdRef.current = null;
          }
        } else {
          setTimeLeftMs(remaining);
        }
      }, 100);
    }

    return () => {
      if (timerIdRef.current) {
        clearInterval(timerIdRef.current);
        timerIdRef.current = null;
      }
    };
  }, [typed.length, isFinished, initialTimeLimit]);

  const handleKeyDown = (event) => {
    if (!snippet || isFinished) return;

    const { key } = event;
    event.preventDefault();

    // Start timer on first valid key press
    if (!startTimeRef.current && (key.length === 1 || key === "Enter")) {
      startTimeRef.current = Date.now();
      setElapsedMs(0);
    }

    if (key === "Backspace") {
      setTyped((prev) => prev.slice(0, -1));
      return;
    }

    if (key.length === 1) {
      setTyped((prev) => {
        if (prev.length >= snippet.length) return prev;
        return prev + key;
      });
      return;
    }

    if (key === "Enter") {
      setTyped((prev) => {
        if (prev.length >= snippet.length) return prev;
        return prev + "\n";
      });
      return;
    }
    if (key === "Tab") {
      setTyped((prev) => prev + "  ");
      return;
    }
  };

  const wpm = (() => {
    if (elapsedMs <= 0) return 0;
    const minutes = elapsedMs / 60000;
    
    // Standard WPM: (All typed entries / 5) / Time (min)
    const wpmVal = (correctCount / 5) / minutes;
    return Math.round(wpmVal);
  })();

  const accuracy = (() => {
    if (totalTyped === 0) return 100;
    // Accuracy = (Correct / Total Typed) * 100
    return Math.round((correctCount / totalTyped) * 100);
  })();

  return {
    snippet,
    typed,
    isFinished,
    elapsedMs,
    correctCount,
    totalTyped,
    wpm,
    accuracy,
    indexRef,
    handleKeyDown,
    timeLeftMs,
  };
}
