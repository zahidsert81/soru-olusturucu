import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Upload API
export const uploadPDF = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await apiClient.post('/upload/pdf', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return response.data
}

// Questions API
export const getQuestions = async (difficulty = null, subject = null, limit = 100) => {
  const params = new URLSearchParams()
  if (difficulty) params.append('difficulty', difficulty)
  if (subject) params.append('subject', subject)
  params.append('limit', limit)
  
  const response = await apiClient.get(`/questions/?${params}`)
  return response.data
}

export const getQuestion = async (questionId) => {
  const response = await apiClient.get(`/questions/${questionId}`)
  return response.data
}

export const createQuestion = async (questionData) => {
  const response = await apiClient.post('/questions/create', questionData)
  return response.data
}

export const getStats = async () => {
  const response = await apiClient.get('/questions/stats/summary')
  return response.data
}

// PDF API
export const generatePDF = async () => {
  const response = await apiClient.post('/pdf/generate')
  return response.data
}

export const downloadPDF = (filename) => {
  window.open(`${API_BASE}/pdf/download/${filename}`, '_blank')
}

export default apiClient
