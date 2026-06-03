<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getMonitorServers, getMonitorHistory, getLocalMetrics } from '@/api/extras'
import { useSeo } from '@/composables/useSeo'

const { setSeo } = useSeo()
const servers = ref([])
const localMetrics = ref(null)
const selectedServer = ref(null)
const history = ref([])
const loading = ref(true)
let refreshTimer = null

const loadData = async () => {
  try {
    loading.value = true
    const [serversRes, localRes] = await Promise.all([
      getMonitorServers(),
      getLocalMetrics().catch(() => ({ data: null })),
    ])
    servers.value = serversRes.data.results || serversRes.data || []
    localMetrics.value = localRes.data
    if (servers.value.length && !selectedServer.value) {
      selectServer(servers.value[0])
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const selectServer = async (server) => {
  selectedServer.value = server
  try {
    const res = await getMonitorHistory(server.id)
    history.value = (res.data.results || res.data || []).reverse()
  } catch (e) {
    history.value = []
  }
}

const barWidth = (val) => `${Math.min(100, val || 0)}%`
const statusColor = (val) => {
  if (val >= 90) return '#ef4444'
  if (val >= 70) return '#f59e0b'
  return '#22c55e'
}

onMounted(() => {
  setSeo({ title: '服务器监控', description: '实时监控服务器 CPU、内存、磁盘状态' })
  loadData()
  refreshTimer = setInterval(loadData, 30000)
})

onUnmounted(() => {
  if (refreshTimer) clearInterval(refreshTimer)
})
</script>

<template>
  <div class="monitor-page">
    <div class="container">
      <header class="page-header">
        <h1>📊 服务器监控</h1>
        <p>参考 izone 云监控，展示服务器运行状态</p>
      </header>

      <div v-if="loading" class="loading">加载中...</div>

      <div v-else class="monitor-grid">
        <div v-if="localMetrics && !localMetrics.error" class="metric-card local-card">
          <h3>🖥️ 本机（Django 服务器）</h3>
          <div class="metric-bars">
            <div class="metric-row">
              <span>CPU</span>
              <div class="bar-bg"><div class="bar-fill" :style="{ width: barWidth(localMetrics.cpu_percent), background: statusColor(localMetrics.cpu_percent) }"></div></div>
              <span>{{ localMetrics.cpu_percent?.toFixed(1) }}%</span>
            </div>
            <div class="metric-row">
              <span>内存</span>
              <div class="bar-bg"><div class="bar-fill" :style="{ width: barWidth(localMetrics.memory_percent), background: statusColor(localMetrics.memory_percent) }"></div></div>
              <span>{{ localMetrics.memory_percent?.toFixed(1) }}%</span>
            </div>
            <div class="metric-row">
              <span>磁盘</span>
              <div class="bar-bg"><div class="bar-fill" :style="{ width: barWidth(localMetrics.disk_percent), background: statusColor(localMetrics.disk_percent) }"></div></div>
              <span>{{ localMetrics.disk_percent?.toFixed(1) }}%</span>
            </div>
          </div>
        </div>

        <div
          v-for="server in servers"
          :key="server.id"
          class="metric-card"
          :class="{ active: selectedServer?.id === server.id }"
          @click="selectServer(server)"
        >
          <h3>{{ server.name }}</h3>
          <p class="hostname">{{ server.hostname || '未知主机' }}</p>
          <div v-if="server.latest_metric" class="metric-bars">
            <div class="metric-row">
              <span>CPU</span>
              <div class="bar-bg"><div class="bar-fill" :style="{ width: barWidth(server.latest_metric.cpu_percent), background: statusColor(server.latest_metric.cpu_percent) }"></div></div>
              <span>{{ server.latest_metric.cpu_percent?.toFixed(1) }}%</span>
            </div>
            <div class="metric-row">
              <span>内存</span>
              <div class="bar-bg"><div class="bar-fill" :style="{ width: barWidth(server.latest_metric.memory_percent), background: statusColor(server.latest_metric.memory_percent) }"></div></div>
              <span>{{ server.latest_metric.memory_percent?.toFixed(1) }}%</span>
            </div>
            <div class="metric-row">
              <span>磁盘</span>
              <div class="bar-bg"><div class="bar-fill" :style="{ width: barWidth(server.latest_metric.disk_percent), background: statusColor(server.latest_metric.disk_percent) }"></div></div>
              <span>{{ server.latest_metric.disk_percent?.toFixed(1) }}%</span>
            </div>
          </div>
          <p v-else class="no-data">暂无上报数据</p>
        </div>
      </div>

      <div v-if="history.length" class="history-section">
        <h2>📈 {{ selectedServer?.name }} 历史记录</h2>
        <div class="history-chart">
          <div v-for="m in history.slice(-20)" :key="m.id" class="history-bar-group">
            <div class="history-bars">
              <div class="h-bar cpu" :style="{ height: barWidth(m.cpu_percent) }" :title="`CPU ${m.cpu_percent}%`"></div>
              <div class="h-bar mem" :style="{ height: barWidth(m.memory_percent) }" :title="`内存 ${m.memory_percent}%`"></div>
            </div>
            <span class="h-time">{{ new Date(m.reported_at).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }) }}</span>
          </div>
        </div>
      </div>

      <div v-if="!servers.length && !loading" class="empty-hint">
        <p>暂无监控服务器。请在 Django Admin 中创建 MonitorServer，然后运行 <code>scripts/monitor_agent.py</code> 上报数据。</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.monitor-page { padding: 2rem 0; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; }
.page-header { text-align: center; margin-bottom: 2rem; }
.page-header h1 { font-size: 2rem; color: var(--text-color); }
.page-header p { color: var(--text-secondary-color); }
.monitor-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }
.metric-card { background: var(--surface-color); border-radius: 12px; padding: 1.5rem; border: 2px solid var(--border-color); cursor: pointer; transition: all 0.2s; }
.metric-card.active, .metric-card:hover { border-color: var(--primary-color); }
.local-card { border-color: var(--primary-color); cursor: default; }
.hostname { color: var(--text-secondary-color); font-size: 0.9rem; margin-bottom: 1rem; }
.metric-bars { display: flex; flex-direction: column; gap: 0.75rem; }
.metric-row { display: grid; grid-template-columns: 40px 1fr 50px; align-items: center; gap: 0.5rem; font-size: 0.9rem; }
.bar-bg { height: 8px; background: var(--background-color); border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
.no-data { color: var(--text-secondary-color); font-size: 0.9rem; }
.history-section { margin-top: 2rem; background: var(--surface-color); border-radius: 12px; padding: 1.5rem; }
.history-chart { display: flex; gap: 4px; align-items: flex-end; height: 120px; overflow-x: auto; padding-top: 1rem; }
.history-bar-group { display: flex; flex-direction: column; align-items: center; gap: 4px; min-width: 30px; }
.history-bars { display: flex; gap: 2px; align-items: flex-end; height: 100px; }
.h-bar { width: 10px; border-radius: 2px 2px 0 0; min-height: 2px; }
.h-bar.cpu { background: #3b82f6; }
.h-bar.mem { background: #8b5cf6; }
.h-time { font-size: 0.65rem; color: var(--text-secondary-color); }
.empty-hint { text-align: center; padding: 2rem; color: var(--text-secondary-color); }
.loading { text-align: center; padding: 3rem; }
</style>
