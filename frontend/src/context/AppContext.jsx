import React, { createContext, useContext, useState } from 'react'

const AppContext = createContext()

export const AppProvider = ({ children }) => {
  const [questions, setQuestions] = useState([])
  const [uploadedFile, setUploadedFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState({
    total: 0,
    byDifficulty: {},
    bySubject: {}
  })

  return (
    <AppContext.Provider
      value={{
        questions,
        setQuestions,
        uploadedFile,
        setUploadedFile,
        loading,
        setLoading,
        stats,
        setStats
      }}
    >
      {children}
    </AppContext.Provider>
  )
}

export const useAppContext = () => {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useAppContext must be used within AppProvider')
  }
  return context
}
