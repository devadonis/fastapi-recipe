import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    'process.env': {
      REACT_APP_MODE: 'dev',
      REACT_APP_API_BASE_PATH: 'http://localhost:8081',
    }
  },
})
