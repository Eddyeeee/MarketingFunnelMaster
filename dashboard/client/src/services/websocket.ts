import { WebSocketMessage } from '@intelligence-dashboard/shared'

export class IntelligenceWebSocketClient {
  private ws: WebSocket | null = null
  private url: string
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  private subscriptions = new Set<string>()
  private messageHandlers = new Map<string, Set<(data: any) => void>>()

  constructor(url: string = 'ws://localhost:4001') {
    this.url = url
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        resolve()
        return
      }

      this.ws = new WebSocket(this.url)

      this.ws.onopen = () => {
        console.log('WebSocket connected')
        this.reconnectAttempts = 0
        
        // Re-subscribe to all channels
        this.subscriptions.forEach(channel => {
          this.sendMessage({ type: 'subscribe', channel })
        })
        
        resolve()
      }

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          this.handleMessage(message)
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      this.ws.onclose = () => {
        console.log('WebSocket disconnected')
        this.attemptReconnect()
      }

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        reject(error)
      }
    })
  }

  private attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached')
      return
    }

    this.reconnectAttempts++
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1)
    
    console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`)
    
    setTimeout(() => {
      this.connect().catch(console.error)
    }, delay)
  }

  private handleMessage(message: WebSocketMessage) {
    const handlers = this.messageHandlers.get(message.type)
    if (handlers) {
      handlers.forEach(handler => handler(message.data))
    }
  }

  subscribe(channel: string): void {
    this.subscriptions.add(channel)
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.sendMessage({ type: 'subscribe', channel })
    }
  }

  unsubscribe(channel: string): void {
    this.subscriptions.delete(channel)
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.sendMessage({ type: 'unsubscribe', channel })
    }
  }

  on(messageType: string, handler: (data: any) => void): void {
    if (!this.messageHandlers.has(messageType)) {
      this.messageHandlers.set(messageType, new Set())
    }
    this.messageHandlers.get(messageType)!.add(handler)
  }

  off(messageType: string, handler: (data: any) => void): void {
    const handlers = this.messageHandlers.get(messageType)
    if (handlers) {
      handlers.delete(handler)
      if (handlers.size === 0) {
        this.messageHandlers.delete(messageType)
      }
    }
  }

  requestProcesses(): void {
    this.sendMessage({ type: 'get_processes' })
  }

  requestMetrics(platform?: string): void {
    this.sendMessage({ type: 'get_metrics', platform })
  }

  requestRevenue(timeframe?: string): void {
    this.sendMessage({ type: 'get_revenue', timeframe })
  }

  private sendMessage(message: any): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    }
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  get isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN
  }
}

export const wsClient = new IntelligenceWebSocketClient(
  import.meta.env.VITE_WS_URI || 'ws://localhost:4001'
)