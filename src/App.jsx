import React, { useState } from 'react'
import CareConnectLogin from './CareConnectLogin.jsx'
import PatientDashboard from './nextpage.jsx'

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [currentUser, setCurrentUser] = useState(null)

  const handleLogin = (user) => {
    setCurrentUser(user)
    setIsLoggedIn(true)
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setCurrentUser(null)
  }

  return (
    <>
      {!isLoggedIn ? (
        <CareConnectLogin onLogin={handleLogin} />
      ) : (
        <PatientDashboard user={currentUser} onLogout={handleLogout} />
      )}
    </>
  )
}
