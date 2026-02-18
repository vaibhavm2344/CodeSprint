import React, { useEffect, useLayoutEffect, useRef, useState } from "react";

export function TypingSnippetEditor({ snippet, typed, onKeyDown }) {
  const hiddenInputRef = useRef(null);
  const baseLayerRef = useRef(null);
  const caretMarkerRef = useRef(null);

  const [cursorPos, setCursorPos] = useState({ x: 0, y: 0, height: 20 });
  const caretIndex = typed.length;

  const focusInput = () => {
    hiddenInputRef.current?.focus();
  };

  useEffect(() => {
    if (snippet) {
      focusInput();
    }
  }, [snippet]);

  useLayoutEffect(() => {
    if (!snippet || !baseLayerRef.current || !caretMarkerRef.current) return;

    const caretRect = caretMarkerRef.current.getBoundingClientRect();
    const containerRect = baseLayerRef.current.getBoundingClientRect();

    setCursorPos({
      x: caretRect.left - containerRect.left,
      y: caretRect.top - containerRect.top,
      height: caretRect.height || 20,
    });
  }, [snippet, typed]);

  return (
    <section
      className="relative rounded-xl bg-slate-900 border border-slate-800 shadow-lg shadow-black/40 px-4 py-3 cursor-text"
      onClick={focusInput}
    >
      <input
        ref={hiddenInputRef}
        className="absolute opacity-0 pointer-events-none h-0 w-0"
        onKeyDown={onKeyDown}
      />

      <div className="mb-2 flex items-center justify-between text-[11px] text-slate-400">
        <div className="flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-red-500" />
          <span className="h-2 w-2 rounded-full bg-amber-400" />
          <span className="h-2 w-2 rounded-full bg-emerald-500" />
          <span className="ml-3 font-mono text-xs text-slate-300">
            snippet
          </span>
        </div>
        <span className="font-mono text-[11px] text-slate-500">
          Type to begin · Backspace, Tab and Enter supported
        </span>
      </div>

      <div
        ref={baseLayerRef}
        className="relative max-h-95 overflow-auto rounded-lg bg-slate-950 px-4 py-3 font-mono text-sm leading-relaxed"
      >


        <pre className="m-0 whitespace-pre text-slate-700">
          {snippet}
        </pre>


        <pre className="pointer-events-none absolute inset-0 m-0 px-4 py-3 whitespace-pre font-mono text-sm leading-relaxed">
          {snippet.split("").map((char, index) => {
            const typedChar = typed[index];
            let colorClass = "text-transparent";



            if (typedChar != null) {
              colorClass = typedChar === char ? "text-amber-300" : "text-red-400";
            }

            return (
              <span key={index} className={colorClass}>
                {char}
              </span>
            );
          })}
        </pre>



        <pre className="pointer-events-none absolute inset-0 m-0 px-4 py-3 whitespace-pre font-mono text-sm leading-relaxed text-transparent select-none">
          {snippet.split("").map((char, index) => {
            return (
              <span key={index} className="relative inline">
                {index === caretIndex && (
                  <span
                    ref={caretMarkerRef}
                    className="absolute left-0 top-0 w-0 h-[1.2em]"
                  />
                )}
                {char}
              </span>
            );
          })}
          {caretIndex === snippet.length && (
            <span
              ref={caretMarkerRef}
              className="relative inline-block w-0 h-[1.2em]"
            />
          )}
        </pre>

        {snippet && (
          <div
            className="pointer-events-none absolute z-20 w-0.5 bg-amber-300 transition-all duration-75 animate-cursor-blink"
            style={{
              left: cursorPos.x,
              top: cursorPos.y,
              height: cursorPos.height,
            }}
          />
        )}
      </div>
    </section>
  );
}
