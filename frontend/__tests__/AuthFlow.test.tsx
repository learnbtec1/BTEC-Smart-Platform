import React, { useEffect } from 'react'
import { render } from '@testing-library/react'
import { useRouter } from 'next/router'

jest.mock('next/router', () => ({
  useRouter: jest.fn(),
}))

describe('Auth middleware simulation', () => {
  it('redirects to /login if no token present', () => {
    const push = jest.fn()
    ;(useRouter as jest.Mock).mockReturnValue({ push })

    // Minimal protected component that redirects when no token
    function Protected() {
      useEffect(() => {
        const t = globalThis.localStorage?.getItem('token')
        if (!t) push('/login')
      }, [])
      return <div>Protected</div>
    }

    // Ensure localStorage is empty
    globalThis.localStorage?.removeItem('token')
    render(<Protected />)
    expect(push).toHaveBeenCalledWith('/login')
  })
})
