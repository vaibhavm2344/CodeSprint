import React from 'react'
import { Route, Routes } from 'react-router-dom'
import HomePage from './pages/HomePage'
import PracticePage from './pages/PracticePage'
import ResultsPage from './pages/ResultsPage'

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/practice" element={<PracticePage />} />
      <Route path="/result" element={<ResultsPage />} />
    </Routes>
  )
}

export default App
