import React, { useState } from 'react'
import { Upload, AlertCircle } from 'lucide-react'
import { uploadPDF } from '../services/api'
import { useAppContext } from '../context/AppContext'

const FileUpload = () => {
  const [isDragActive, setIsDragActive] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)
  const { setUploadedFile, setLoading } = useAppContext()

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragActive(e.type === 'dragenter' || e.type === 'dragover')
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragActive(false)

    const files = e.dataTransfer.files
    if (files && files[0]) {
      handleFile(files[0])
    }
  }

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = async (file) => {
    setError(null)
    setSuccess(false)

    if (file.type !== 'application/pdf') {
      setError('Lütfen sadece PDF dosyası yükleyin')
      return
    }

    if (file.size > 50 * 1024 * 1024) {
      setError('Dosya çok büyük (max 50MB)')
      return
    }

    try {
      setLoading(true)
      const response = await uploadPDF(file)
      setUploadedFile(response)
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Yükleme başarısız oldu')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 bg-white hover:border-gray-400'
        }`}
      >
        <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
        <h3 className="text-lg font-semibold mb-2">PDF Dosyası Yükleyin</h3>
        <p className="text-gray-600 mb-4">Sürükleyip bırakın veya tıklayın</p>
        <input
          type="file"
          accept=".pdf"
          onChange={handleChange}
          className="hidden"
          id="file-input"
        />
        <label htmlFor="file-input" className="inline-block">
          <button className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
            Dosya Seç
          </button>
        </label>
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2">
          <AlertCircle className="w-5 h-5 text-red-500" />
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {success && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-green-700 font-semibold">✓ Dosya başarıyla yüklendi!</p>
        </div>
      )}
    </div>
  )
}

export default FileUpload
