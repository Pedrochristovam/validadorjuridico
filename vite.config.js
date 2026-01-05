import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { existsSync } from 'fs'

const candidatePaths = [
  path.resolve(process.cwd(), 'src'),
  path.resolve(process.cwd(), '..', 'src'),
  path.resolve(process.cwd(), '..', '..', 'src'),
  path.resolve(__dirname, 'src'),
  path.resolve(__dirname, '..', 'src'),
  path.resolve(__dirname, '..', '..', 'src'),
]

const resolveSrcPath = () => {
  for (const candidate of candidatePaths) {
    const utilsPath = path.join(candidate, 'lib', 'utils.js')
    if (existsSync(candidate) && existsSync(utilsPath)) {
      return candidate
    }
  }

  return path.resolve(__dirname, 'src')
}

const srcPath = resolveSrcPath()

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': srcPath,
    },
  },
})
