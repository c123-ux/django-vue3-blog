import { watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

export function useSeo(defaults = {}) {
  const route = useRoute()

  const defaultTitle = defaults.title || 'TendCode - 技术博客'
  const defaultDescription = defaults.description || '分享编程学习心得，记录工作实战经验'
  const defaultKeywords = defaults.keywords || 'Python,Django,Vue3,博客'
  const defaultImage = defaults.image || ''

  const setMeta = (name, content, attr = 'name') => {
    if (!content) return
    let el = document.querySelector(`meta[${attr}="${name}"]`)
    if (!el) {
      el = document.createElement('meta')
      el.setAttribute(attr, name)
      document.head.appendChild(el)
    }
    el.setAttribute('content', content)
  }

  const removeMeta = (name, attr = 'name') => {
    const el = document.querySelector(`meta[${attr}="${name}"]`)
    if (el) {
      el.parentNode.removeChild(el)
    }
  }

  const setSeo = (options = {}) => {
    const title = options.title || defaultTitle
    const description = options.description || defaultDescription
    const keywords = options.keywords || defaultKeywords
    const image = options.image || defaultImage
    const url = options.url || window.location.href
    const type = options.type || 'website'
    const siteName = options.siteName || 'TendCode'

    document.title = title

    setMeta('description', description)
    setMeta('keywords', keywords)

    let canonical = document.querySelector('link[rel="canonical"]')
    if (!canonical) {
      canonical = document.createElement('link')
      canonical.setAttribute('rel', 'canonical')
      document.head.appendChild(canonical)
    }
    canonical.setAttribute('href', url)

    setMeta('og:title', title, 'property')
    setMeta('og:description', description, 'property')
    setMeta('og:url', url, 'property')
    setMeta('og:type', type, 'property')
    setMeta('og:site_name', siteName, 'property')
    setMeta('og:locale', 'zh_CN', 'property')

    if (image) {
      setMeta('og:image', image, 'property')
      setMeta('og:image:width', '1200', 'property')
      setMeta('og:image:height', '630', 'property')
    } else {
      removeMeta('og:image', 'property')
      removeMeta('og:image:width', 'property')
      removeMeta('og:image:height', 'property')
    }

    setMeta('twitter:card', 'summary_large_image')
    setMeta('twitter:title', title)
    setMeta('twitter:description', description)
    if (image) {
      setMeta('twitter:image', image)
    } else {
      removeMeta('twitter:image')
    }
  }

  const resetSeo = () => {
    setSeo({
      title: defaultTitle,
      description: defaultDescription,
      keywords: defaultKeywords,
      image: defaultImage,
    })
  }

  return { setSeo, resetSeo }
}

export function useSiteSeo(siteConfig) {
  const { setSeo, resetSeo } = useSeo()
  if (siteConfig) {
    setSeo({
      title: siteConfig.site_name,
      description: siteConfig.site_description,
      keywords: siteConfig.site_keywords,
    })
  }
  return { setSeo, resetSeo }
}

export function usePageSeo() {
  const route = useRoute()
  const { setSeo, resetSeo } = useSeo()

  onMounted(() => {
    resetSeo()
  })

  watch(
    () => route.path,
    () => {
      resetSeo()
    }
  )

  return { setSeo, resetSeo }
}
