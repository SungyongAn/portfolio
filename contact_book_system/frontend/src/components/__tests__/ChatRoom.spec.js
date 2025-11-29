import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import ChatRoom from '../ChatRoom.vue'

// Mock vue-router
vi.mock('vue-router', () => ({
    useRoute: () => ({
        params: { roomId: '1' },
        query: { roomName: 'Test Room' }
    }),
    useRouter: () => ({
        push: vi.fn()
    })
}))

// Stub global variable
vi.stubGlobal('API_BASE_URL', 'http://localhost:8000')

// Mock sessionStorage
const sessionStorageMock = {
    getItem: vi.fn((key) => {
        if (key === 'currentUser') return JSON.stringify({ id: 1, name: 'Test User', role: 'teacher' })
        if (key === 'access_token') return 'fake-token'
        return null
    }),
    setItem: vi.fn(),
    clear: vi.fn()
}
vi.stubGlobal('sessionStorage', sessionStorageMock)

// Mock axios
vi.mock('axios', () => ({
    default: {
        get: vi.fn((url) => {
            if (url.includes('/messages')) return Promise.resolve({ data: [] })
            if (url.includes('/rooms/')) return Promise.resolve({ data: { id: 1, name: 'Test Room', participants: [] } })
            return Promise.resolve({ data: {} })
        }),
        post: vi.fn(() => Promise.resolve({ data: {} })),
        defaults: { headers: { common: {} } }
    }
}))

describe('ChatRoom', () => {
    it('emits updateTitle with room name', async () => {
        const wrapper = mount(ChatRoom, {
            global: {
                stubs: ['font-awesome-icon']
            },
            props: {
                roomId: '1',
                currentUser: { id: 1, name: 'Test User' }
            }
        })

        // Wait for mounted and async calls
        await new Promise(resolve => setTimeout(resolve, 100))

        // Check emitted events
        expect(wrapper.emitted()).toHaveProperty('updateTitle')
        const updateTitleEvent = wrapper.emitted('updateTitle')
        expect(updateTitleEvent[0][0].title).toBe('Test Room') // Assuming axios mock returns room with name 'Test Room'
    })
})
