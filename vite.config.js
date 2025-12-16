import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'
import { existsSync } from 'fs'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// Tenta encontrar o diretório src de forma inteligente
let srcPath = path.resolve(__dirname, 'src')

// Se o caminho não existir ou já contiver 'src/src', tenta alternativas
if (!existsSync(srcPath) || srcPath.includes('src/src')) {
  // Tenta usar process.cwd() como base
  const cwd = process.cwd()
  const altPath = path.resolve(cwd, 'src')
  if (existsSync(altPath) && !altPath.includes('src/src')) {
    srcPath = altPath
  } else {
    // Fallback: usa __dirname mas remove duplicações
    const normalized = path.normalize(path.resolve(__dirname, 'src'))
    srcPath = normalized.replace(/src\/src/g, 'src')
  }
}

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': srcPath,
    },
  },
})
