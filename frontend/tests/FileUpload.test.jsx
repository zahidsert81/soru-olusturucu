import { describe, it, expect, beforeEach } from 'vitest'
import React from 'react'
import { render, screen } from '@testing-library/react'
import FileUpload from '../src/components/FileUpload'

describe('FileUpload Component', () => {
  it('should render upload component', () => {
    render(<FileUpload />)
    expect(screen.getByText(/PDF Dosyası Yükleyin/i)).toBeInTheDocument()
  })

  it('should have file input', () => {
    render(<FileUpload />)
    const input = screen.getByRole('textbox', { hidden: true })
    expect(input).toBeInTheDocument()
  })
})
