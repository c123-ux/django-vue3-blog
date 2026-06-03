export const fixImageUrl = (url) => {
  if (!url) return null
  const urlStr = String(url)
  // 检查是否被错误加上了前缀
  if (urlStr.includes('/media/https%3A')) {
    return decodeURIComponent(urlStr.replace(/^.*\/media\//, ''))
  }
  if (urlStr.includes('/media/http%3A')) {
    return decodeURIComponent(urlStr.replace(/^.*\/media\//, ''))
  }
  return urlStr
}
