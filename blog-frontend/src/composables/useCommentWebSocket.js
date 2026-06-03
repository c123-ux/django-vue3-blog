import { ref, onUnmounted } from 'vue'

export function useCommentWebSocket(articleId, { onNewComment, onDeleteComment, onTyping, onError } = {}) {
  const connected = ref(false)
  const typingUsers = ref([])
  let ws = null
  let typingTimer = null

  const connect = (token) => {
    const id = typeof articleId === 'function' ? articleId() : articleId
    if (!token || !id) return

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const url = `${protocol}//${host}/ws/comments/${id}/?token=${encodeURIComponent(token)}`

    ws = new WebSocket(url)

    ws.onopen = () => {
      connected.value = true
    }

    ws.onclose = () => {
      connected.value = false
    }

    ws.onerror = () => {
      onError?.('WebSocket 连接失败')
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'new_comment') {
          onNewComment?.(data.comment)
        } else if (data.type === 'delete_comment') {
          onDeleteComment?.(data.comment_id)
        } else if (data.type === 'typing') {
          if (data.is_typing) {
            if (!typingUsers.value.includes(data.user)) {
              typingUsers.value.push(data.user)
            }
          } else {
            typingUsers.value = typingUsers.value.filter(u => u !== data.user)
          }
          onTyping?.(typingUsers.value)
        } else if (data.type === 'error') {
          onError?.(data.message)
        }
      } catch (e) {
        console.error('WS message parse error', e)
      }
    }
  }

  const disconnect = () => {
    if (ws) {
      ws.close()
      ws = null
    }
    connected.value = false
  }

  const sendComment = (content, parentId = null) => {
    if (!ws || ws.readyState !== WebSocket.OPEN) return false
    ws.send(JSON.stringify({
      type: 'new_comment',
      content,
      parent_id: parentId,
    }))
    return true
  }

  const sendTyping = (isTyping) => {
    if (!ws || ws.readyState !== WebSocket.OPEN) return
    clearTimeout(typingTimer)
    ws.send(JSON.stringify({ type: 'typing', is_typing: isTyping }))
    if (isTyping) {
      typingTimer = setTimeout(() => sendTyping(false), 2000)
    }
  }

  const deleteComment = (commentId) => {
    if (!ws || ws.readyState !== WebSocket.OPEN) return false
    ws.send(JSON.stringify({ type: 'delete_comment', comment_id: commentId }))
    return true
  }

  onUnmounted(disconnect)

  return { connected, typingUsers, connect, disconnect, sendComment, sendTyping, deleteComment }
}
