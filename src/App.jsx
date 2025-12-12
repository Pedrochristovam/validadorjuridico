import React from 'react'
import { Routes, Route, useLocation } from 'react-router-dom'
import Layout from './Layout.jsx'
import Home from './Pages/Home.jsx'
import Models from './Pages/Models.jsx'
import History from './Pages/History.jsx'

function App() {
  const location = useLocation()
  
  // Determinar o nome da página atual baseado na rota
  const getCurrentPageName = () => {
    if (location.pathname === '/' || location.pathname === '/home') return 'Home'
    if (location.pathname === '/models') return 'Models'
    if (location.pathname === '/history') return 'History'
    return 'Home'
  }

  return (
    <Layout currentPageName={getCurrentPageName()}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/models" element={<Models />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </Layout>
  )
}

export default App

