import React from 'react'
import { render, screen } from '@testing-library/react'

// Mock small components used on the Home page
jest.mock('../src/components/ChatWidget', () => () => <div>ChatWidget</div>)
jest.mock('../src/components/Onboarding', () => () => <div>Onboarding</div>)

import Home from '../src/pages/index'

describe('Dashboard rendering', () => {
  it('renders onboarding, chat widget and header', () => {
    render(<Home />)
    expect(screen.getByText('Onboarding')).toBeInTheDocument()
    expect(screen.getByText('ChatWidget')).toBeInTheDocument()
    expect(screen.getByText(/Welcome to the Platform/i)).toBeInTheDocument()
  })
})
