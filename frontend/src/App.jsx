import React from 'react'
import FileUpload from './components/FileUpload'
import QuestionForm from './components/QuestionForm'
import Statistics from './components/Statistics'
import PDFGenerator from './components/PDFGenerator'
import { AppProvider } from './context/AppContext'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import './index.css'

function App() {
  const [activeTab, setActiveTab] = React.useState('upload')
  const [refreshStats, setRefreshStats] = React.useState(0)

  const handleQuestionAdded = () => {
    setRefreshStats(prev => prev + 1)
  }

  return (
    <AppProvider>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Header */}
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 py-6">
            <h1 className="text-3xl font-bold text-gray-900">📚 Soru Oluşturucu</h1>
            <p className="text-gray-600 mt-1">PDF'den soruları algılayıp yayın kalitesinde PDF üreten uygulama</p>
          </div>
        </header>

        {/* Navigation Tabs */}
        <div className="bg-white border-b">
          <div className="max-w-7xl mx-auto px-4">
            <nav className="flex gap-8">
              {[
                { id: 'upload', label: '📤 Yükle' },
                { id: 'questions', label: '❓ Sorular' },
                { id: 'stats', label: '📊 İstatistikler' },
                { id: 'pdf', label: '📄 PDF Oluştur' }
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-4 py-4 font-medium border-b-2 transition ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-600 hover:text-gray-900'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 py-8">
          {activeTab === 'upload' && <FileUpload />}
          {activeTab === 'questions' && <QuestionForm onQuestionAdded={handleQuestionAdded} />}
          {activeTab === 'stats' && <Statistics key={refreshStats} />}
          {activeTab === 'pdf' && <PDFGenerator />}
        </main>

        {/* Footer */}
        <footer className="bg-white border-t mt-12">
          <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-600">
            <p>© 2024 Soru Oluşturucu. Tüm hakları saklıdır.</p>
          </div>
        </footer>
      </div>
      <ToastContainer />
    </AppProvider>
  )
}

export default App
