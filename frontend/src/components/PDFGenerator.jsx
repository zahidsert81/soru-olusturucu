import React, { useState, useEffect } from 'react'
import { Download, RefreshCw, AlertCircle } from 'lucide-react'
import { generatePDF, downloadPDF, getQuestions } from '../services/api'

const PDFGenerator = () => {
  const [generating, setGenerating] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)
  const [questionCount, setQuestionCount] = useState(0)

  useEffect(() => {
    const fetchQuestionCount = async () => {
      try {
        const data = await getQuestions(null, null, 1)
        setQuestionCount(data.count)
      } catch (err) {
        console.error('Soru sayısı alma hatası:', err)
      }
    }
    fetchQuestionCount()
  }, [])

  const handleGeneratePDF = async () => {
    setError(null)
    setSuccess(false)

    if (questionCount === 0) {
      setError('Henüz soru eklenmemiş')
      return
    }

    try {
      setGenerating(true)
      const response = await generatePDF()
      setSuccess(true)
      
      // PDF'yi indir
      setTimeout(() => {
        downloadPDF(response.filename)
      }, 500)
    } catch (err) {
      setError(err.response?.data?.detail || 'PDF oluşturma başarısız')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 space-y-4">
      <h2 className="text-2xl font-bold mb-4">PDF Oluştur</h2>

      <div className="bg-blue-50 border border-blue-200 rounded p-4">
        <p className="text-blue-900 font-semibold">
          {questionCount > 0 ? `${questionCount} soru PDF'ye dönüştürülecek` : 'Henüz soru eklenmemiş'}
        </p>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded flex items-center gap-2">
          <AlertCircle className="w-5 h-5 text-red-500" />
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {success && (
        <div className="p-4 bg-green-50 border border-green-200 rounded">
          <p className="text-green-700 font-semibold">✓ PDF başarıyla oluşturuldu ve indirildi!</p>
        </div>
      )}

      <button
        onClick={handleGeneratePDF}
        disabled={generating || questionCount === 0}
        className="w-full py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition disabled:bg-gray-400 flex items-center justify-center gap-2 font-semibold"
      >
        {generating ? (
          <>
            <RefreshCw className="w-5 h-5 animate-spin" />
            Oluşturuluyor...
          </>
        ) : (
          <>
            <Download className="w-5 h-5" />
            PDF Oluştur ve İndir
          </>
        )}
      </button>
    </div>
  )
}

export default PDFGenerator
