import api from './index'

export const getOAuthUrl = (provider) => {
  return api.get(`/auth/oauth/${provider}/`)
}

export const getNotes = () => api.get('/notes/')
export const getNote = (id) => api.get(`/notes/${id}/`)
export const createNote = (data) => api.post('/notes/create/', data)
export const updateNote = (id, data) => api.put(`/notes/${id}/update/`, data)
export const deleteNote = (id) => api.delete(`/notes/${id}/delete/`)

export const getMonitorServers = () => api.get('/monitoring/servers/')
export const getMonitorHistory = (serverId) => api.get(`/monitoring/servers/${serverId}/metrics/`)
export const getLocalMetrics = () => api.get('/monitoring/local/')
