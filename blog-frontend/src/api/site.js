import api from './index'

export const getSiteConfig = () => {
  return api.get('/site/')
}

export const getFriendLinks = () => {
  return api.get('/site/friend-links/')
}
