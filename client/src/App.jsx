import React from 'react'
import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './pages/login'
import SignUp from './pages/sign-up'
import Home from './pages/home'
import RecipeDashboard from './pages/my-recipes'
import ErrorPage from './pages/error-page'

const App = () => {
  return (
    <div className="App bg-black">
      <BrowserRouter>
        <Routes>
          <Route index element={<Home />} />
          <Route path="my-recipes" element={<RecipeDashboard />} />
          <Route path="login" element={<Login />} />
          <Route path="sign-up" element={<SignUp />} />
          <Route path="*" element={<ErrorPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App
