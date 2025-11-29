import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    test: {
        environment: 'jsdom',
        globals: true
    },
    define: {
        API_BASE_URL: JSON.stringify('http://localhost:8000')
    }
})
