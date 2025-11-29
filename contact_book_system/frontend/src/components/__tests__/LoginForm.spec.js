import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import LoginForm from '../LoginForm.vue'

describe('LoginForm', () => {
    it('renders properly', () => {
        const wrapper = mount(LoginForm)
        expect(wrapper.text()).toContain('連絡帳システム ログイン')
    })
})
