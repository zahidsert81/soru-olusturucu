import { describe, it, expect } from 'vitest'
import * as api from '../src/services/api'

describe('API Service', () => {
  it('should have correct API endpoints', () => {
    // API client'in tanımlı olduğunu kontrol et
    expect(api.uploadPDF).toBeDefined()
    expect(api.getQuestions).toBeDefined()
    expect(api.createQuestion).toBeDefined()
    expect(api.generatePDF).toBeDefined()
  })
})
