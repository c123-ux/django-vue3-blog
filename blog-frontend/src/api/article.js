import api from './index'
import { fixImageUrl } from '@/utils'

const fixArticleCover = (article) => {
  if (!article) return article
  return {
    ...article,
    cover: fixImageUrl(article.cover)
  }
}

const fixArticlesList = (data) => {
  if (!data) return data
  if (data.results) {
    return {
      ...data,
      results: data.results.map(fixArticleCover)
    }
  }
  if (Array.isArray(data)) {
    return data.map(fixArticleCover)
  }
  return fixArticleCover(data)
}

const fixSeriesCover = (series) => {
  if (!series) return series
  return {
    ...series,
    cover: fixImageUrl(series.cover),
    articles: series.articles?.map(fixArticleCover) || []
  }
}

export const getArticles = (params = {}) => {
  return api.get('/articles/', { params }).then(res => {
    res.data = fixArticlesList(res.data)
    return res
  })
}

export const getArticle = (id) => {
  return api.get(`/articles/${id}/`).then(res => {
    res.data = fixArticleCover(res.data)
    return res
  })
}

export const createArticle = (data) => {
  return api.post('/articles/create/', data)
}

export const updateArticle = (id, data) => {
  return api.put(`/articles/${id}/update/`, data)
}

export const deleteArticle = (id) => {
  return api.delete(`/articles/${id}/delete/`)
}

export const uploadImage = (formData) => {
  return api.post('/articles/upload-image/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const searchArticles = (query) => {
  return api.get('/articles/search/', { params: { q: query } }).then(res => {
    res.data = fixArticlesList(res.data)
    return res
  })
}

export const getCategories = () => {
  return api.get('/articles/categories/').then(res => {
    if (res.data.results) {
      res.data = res.data.results
    }
    return res
  })
}

export const getTags = () => {
  return api.get('/articles/tags/').then(res => {
    if (res.data.results) {
      res.data = res.data.results
    }
    return res
  })
}

export const getSeriesList = () => {
  return api.get('/articles/series/').then(res => {
    res.data = fixArticlesList(res.data)
    return res
  })
}

export const getSeries = () => {
  return api.get('/articles/series/').then(res => {
    // 如果返回的是分页数据，提取 results 数组
    if (res.data.results) {
      res.data = res.data.results
    }
    return res
  })
}

export const getSeriesDetail = (slug) => {
  return api.get(`/articles/series/${slug}/`).then(res => {
    res.data = fixSeriesCover(res.data)
    return res
  })
}

export const getStatistics = () => {
  return api.get('/articles/statistics/')
}

export const getArchive = () => {
  return api.get('/articles/archive/')
}

export const getArchiveByYear = (year) => {
  return api.get(`/articles/archive/${year}/`)
}

export const getArchiveByMonth = (year, month) => {
  return api.get(`/articles/archive/${year}/${month}/`)
}

export const getCategoryArticles = (slug, params = {}) => {
  return api.get(`/articles/categories/${slug}/articles/`, { params }).then(res => {
    res.data = fixArticlesList(res.data)
    return res
  })
}

export default api
