import * as pdfjsLib from 'pdfjs-dist'
pdfjsLib.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs'
import mammoth from 'mammoth'

export async function extractTextFromFile(file) {
  const ext = file.name.split('.').pop().toLowerCase()
  if (ext === 'pdf') {
    // PDF: используем pdfjs-dist
    const arrayBuffer = await file.arrayBuffer()
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise
    let text = ''
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i)
      const content = await page.getTextContent()
      text += content.items.map(item => item.str).join(' ') + '\n'
    }
    return text.trim()
  } else if (ext === 'docx') {
    // DOCX: используем mammoth
    const arrayBuffer = await file.arrayBuffer()
    const { value } = await mammoth.extractRawText({ arrayBuffer })
    return value.trim()
  } else {
    // Для .txt и других — читаем как текст
    return await file.text()
  }
}

export function formatFileSize(size) {
  if (typeof size !== 'number' || isNaN(size)) return '0 B'
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB'
  return (size / 1024 / 1024).toFixed(2) + ' MB'
} 