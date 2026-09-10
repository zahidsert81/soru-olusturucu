import React, { useState } from 'react'
import { Plus, Edit2, Trash2, AlertCircle } from 'lucide-react'
import { createQuestion } from '../services/api'

const QuestionForm = ({ onQuestionAdded }) => {
  const [formData, setFormData] = useState({
    number: '',
    text: '',
    options: [{ letter: 'A', text: '' }, { letter: 'B', text: '' }, { letter: 'C', text: '' }, { letter: 'D', text: '' }],
    difficulty: 'Orta',
    subject: 'Matematik'
  })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleTextChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleOptionChange = (index, value) => {
    const newOptions = [...formData.options]
    newOptions[index].text = value
    setFormData(prev => ({
      ...prev,
      options: newOptions
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)

    // Validasyon
    if (!formData.text.trim()) {
      setError('Soru metni boş olamaz')
      return
    }

    if (formData.options.some(opt => !opt.text.trim())) {
      setError('Tüm seçenekler doldurulmalıdır')
      return
    }

    try {
      setLoading(true)
      await createQuestion(formData)
      setFormData({
        number: '',
        text: '',
        options: [{ letter: 'A', text: '' }, { letter: 'B', text: '' }, { letter: 'C', text: '' }, { letter: 'D', text: '' }],
        difficulty: 'Orta',
        subject: 'Matematik'
      })
      onQuestionAdded()
    } catch (err) {
      setError(err.response?.data?.detail || 'Soru oluşturma başarısız')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
      <h2 className="text-2xl font-bold mb-4">Yeni Soru Ekle</h2>

      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-red-500" />
          <p className="text-red-700 text-sm">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        <input
          type="number"
          name="number"
          placeholder="Soru No"
          value={formData.number}
          onChange={handleTextChange}
          className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <select
          name="difficulty"
          value={formData.difficulty}
          onChange={handleTextChange}
          className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option>Kolay</option>
          <option>Orta</option>
          <option>Zor</option>
        </select>
      </div>

      <textarea
        name="text"
        placeholder="Soru metni"
        value={formData.text}
        onChange={handleTextChange}
        rows="3"
        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <div className="space-y-2">
        <label className="block font-semibold">Seçenekler</label>
        {formData.options.map((option, index) => (
          <div key={index} className="flex gap-2">
            <span className="px-3 py-2 bg-gray-100 rounded-lg font-bold">{option.letter})</span>
            <input
              type="text"
              placeholder={`Seçenek ${option.letter}`}
              value={option.text}
              onChange={(e) => handleOptionChange(index, e.target.value)}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        ))}
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition disabled:bg-gray-400"
      >
        {loading ? 'Ekleniyor...' : '+ Soru Ekle'}
      </button>
    </form>
  )
}

export default QuestionForm
