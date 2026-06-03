import { ref, watch } from 'vue'

const THEME_KEY = 'blog-theme'

const themes = {
  light: {
    name: 'light',
    primary: '#ea6f5a',
    secondary: '#dd5a3e',
    accent: '#00AAEE',
    background: '#f0f0f0',
    surface: '#ffffff',
    text: '#333333',
    textSecondary: '#666666',
    textMuted: '#999999',
    border: '#e8e8e8',
    shadow: 'rgba(0, 0, 0, 0.06)',
    headerBg: '#ffffff',
    footerBg: '#1c1f21',
    footerText: '#99979c',
    tagBg: '#f5f5f5',
    cardRadius: '8px',
  },
  dark: {
    name: 'dark',
    primary: '#ea6f5a',
    secondary: '#dd5a3e',
    accent: '#00AAEE',
    background: '#22303f',
    surface: '#18222d',
    text: '#9caec7',
    textSecondary: '#7a8ba3',
    textMuted: '#5a6b83',
    border: '#2a3a4a',
    shadow: 'rgba(0, 0, 0, 0.3)',
    headerBg: '#18222d',
    footerBg: '#0f151c',
    footerText: '#5a6b83',
    tagBg: '#2a3a4a',
    cardRadius: '8px',
  }
}

const currentTheme = ref(localStorage.getItem(THEME_KEY) || 'light')

const applyTheme = (themeName) => {
  const theme = themes[themeName]
  const root = document.documentElement
  
  root.style.setProperty('--primary-color', theme.primary)
  root.style.setProperty('--secondary-color', theme.secondary)
  root.style.setProperty('--accent-color', theme.accent)
  root.style.setProperty('--background-color', theme.background)
  root.style.setProperty('--surface-color', theme.surface)
  root.style.setProperty('--text-color', theme.text)
  root.style.setProperty('--text-secondary-color', theme.textSecondary)
  root.style.setProperty('--text-muted-color', theme.textMuted)
  root.style.setProperty('--border-color', theme.border)
  root.style.setProperty('--shadow-color', theme.shadow)
  root.style.setProperty('--header-bg', theme.headerBg)
  root.style.setProperty('--footer-bg', theme.footerBg)
  root.style.setProperty('--footer-text', theme.footerText)
  root.style.setProperty('--tag-bg', theme.tagBg)
  root.style.setProperty('--card-radius', theme.cardRadius)
  
  localStorage.setItem(THEME_KEY, themeName)
  currentTheme.value = themeName
}

const toggleTheme = () => {
  const newTheme = currentTheme.value === 'light' ? 'dark' : 'light'
  applyTheme(newTheme)
}

// 初始化主题
applyTheme(currentTheme.value)

export { currentTheme, toggleTheme, themes }