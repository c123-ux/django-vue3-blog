import { createRouter, createWebHistory } from 'vue-router'

const lazyLoad = (importFn) => {
  return () => {
    return importFn().catch((error) => {
      console.error('[Router] Chunk load failed, retrying...', error)
      return new Promise((resolve) => {
        setTimeout(() => {
          importFn().then(resolve).catch((err2) => {
            console.error('[Router] Chunk load retry failed:', err2)
            resolve(importFn())
          })
        }, 1500)
      })
    })
  }
}

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: lazyLoad(() => import('@/views/HomeView.vue')),
    },
    {
      path: '/articles',
      name: 'articles',
      component: lazyLoad(() => import('@/views/HomeView.vue')),
    },
    {
      path: '/article/:id',
      name: 'article-detail',
      component: lazyLoad(() => import('@/views/ArticleView.vue')),
    },
    {
      path: '/about',
      name: 'about',
      component: lazyLoad(() => import('@/views/AboutView.vue')),
    },
    {
      path: '/search',
      name: 'search',
      component: lazyLoad(() => import('@/views/SearchView.vue')),
    },
    {
      path: '/timeline',
      name: 'timeline',
      component: lazyLoad(() => import('@/views/TimelineView.vue')),
    },
    {
      path: '/categories',
      name: 'categories',
      component: lazyLoad(() => import('@/views/CategoryView.vue')),
    },
    {
      path: '/series',
      name: 'series',
      component: lazyLoad(() => import('@/views/SeriesView.vue')),
    },
    {
      path: '/series/:slug',
      name: 'series-detail',
      component: lazyLoad(() => import('@/views/SeriesDetailView.vue')),
    },
    {
      path: '/archive',
      name: 'archive',
      component: lazyLoad(() => import('@/views/ArchiveView.vue')),
    },
    {
      path: '/archive/:year/:month',
      name: 'archive-month',
      component: lazyLoad(() => import('@/views/ArchiveView.vue')),
    },
    {
      path: '/friends',
      name: 'friends',
      component: lazyLoad(() => import('@/views/FriendLinkView.vue')),
    },
    {
      path: '/notes',
      name: 'notes',
      component: lazyLoad(() => import('@/views/NotesView.vue')),
    },
    {
      path: '/tools',
      name: 'tools',
      component: lazyLoad(() => import('@/views/ToolsView.vue')),
    },
    {
      path: '/monitoring',
      name: 'monitoring',
      component: lazyLoad(() => import('@/views/MonitoringView.vue')),
    },
    {
      path: '/write',
      name: 'write',
      component: lazyLoad(() => import('@/views/GuestEditorView.vue')),
    },
  ],
})

router.onError((error, to) => {
  console.error('[Router] Navigation error to', to.path, ':', error)
})

export default router
