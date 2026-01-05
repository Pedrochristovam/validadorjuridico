import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { existsSync } from 'fs'

const candidatePaths = [
  path.resolve(__dirname, 'src'),
  path.resolve(__dirname, '..', 'src'),
  path.resolve(process.cwd(), 'src'),
]

const srcPath = candidatePaths.find((candidate) => existsSync(candidate)) || path.resolve(__dirname, 'src')

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': srcPath,
    },
  },
})
