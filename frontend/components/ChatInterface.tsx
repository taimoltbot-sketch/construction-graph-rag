// Frontend Components - Chat Interface

'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, FileText, Sparkles } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism'

// Types
interface Message {
  role: 'user' | 'assistant'
  content: string
  mermaidChart?: string
  sources?: SourceItem[]
}

interface SourceItem {
  node_type: string
  node_id: string
  property_name: string
  property_value: string
  confidence: number
}

interface ChatResponse {
  answer: string
  sources: SourceItem[]
  mermaid_chart?: string
}

// API Client
async function sendMessage(message: string): Promise<ChatResponse> {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  })
  
  if (!response.ok) {
    throw new Error('API request failed')
  }
  
  return response.json()
}

// Components

export function ChatInput({ onSubmit }: { onSubmit: (message: string) => void }) {
  const [input, setInput] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = () => {
    if (input.trim()) {
      onSubmit(input.trim())
      setInput('')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [input])

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      <div className="mx-auto max-w-4xl">
        <div className="relative flex items-end gap-2 rounded-2xl border border-gray-200 bg-gray-50 p-2 shadow-sm focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 transition-all">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="輸入您的問題... 例如：B1樓層的進度如何？"
            className="flex-1 resize-none bg-transparent px-4 py-3 text-gray-900 placeholder-gray-400 focus:outline-none max-h-32"
            rows={1}
          />
          <button
            onClick={handleSubmit}
            disabled={!input.trim()}
            className="rounded-xl bg-blue-600 p-3 text-white transition-all hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>
        <p className="mt-2 text-center text-xs text-gray-400">
          支援 Markdown 語法與 Mermaid 圖表
        </p>
      </div>
    </div>
  )
}

export function ChatMessage({ message }: { message: Message }) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex gap-4 p-6 ${isUser ? 'bg-gray-50' : 'bg-white'}`}>
      <div className={`flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center ${
        isUser ? 'bg-blue-100' : 'bg-green-100'
      }`}>
        {isUser ? (
          <User className="h-5 w-5 text-blue-600" />
        ) : (
          <Bot className="h-5 w-5 text-green-600" />
        )}
      </div>
      
      <div className="flex-1 space-y-3">
        <div className="prose prose-gray max-w-none">
          <ReactMarkdown
            components={{
              code({ inline, className, children, ...props }: { inline?: boolean; className?: string; children?: React.ReactNode } & React.HTMLAttributes<HTMLElement>) {
                const match = className && /language-(\w+)/.exec(className)
                return !inline && match ? (
                  <SyntaxHighlighter
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    style={oneLight as any}
                    language={match[1]}
                    PreTag="div"
                    {...props}
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                ) : (
                  <code className={className} {...props}>
                    {children}
                  </code>
                )
              }
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {/* Mermaid Chart */}
        {message.mermaidChart && (
          <div className="rounded-xl bg-gray-900 p-4 overflow-x-auto">
            <div 
              className="mermaid text-white"
              dangerouslySetInnerHTML={{ __html: message.mermaidChart.replace(/```mermaid|```/g, '') }}
            />
          </div>
        )}

        {/* Sources */}
        {message.sources && message.sources.length > 0 && (
          <div className="rounded-lg bg-blue-50 p-4">
            <h4 className="flex items-center gap-2 text-sm font-medium text-blue-800 mb-2">
              <FileText className="h-4 w-4" />
              資料來源
            </h4>
            <div className="space-y-1">
              {message.sources.map((source, i) => (
                <div key={i} className="flex items-center gap-2 text-xs text-blue-700">
                  <span className="rounded bg-blue-100 px-1.5 py-0.5 font-medium">
                    {source.node_type}
                  </span>
                  <span>{source.property_name}: {source.property_value}</span>
                  <span className="text-blue-400">
                    ({Math.round(source.confidence * 100)}% 信心度)
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: `您好！我是 Construction Graph RAG 助手 🇧

我可以幫您查詢：
- **施工進度**：樓層、施工項目完成度
- **成本分析**：材料用量與費用
- **預算執行**：建案預算使用狀況
- **結算單**：出工結算詳細資料

請輸入您的問題，例如：「B1樓層的鋼筋作業進度如何？」`,
    },
  ])
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (message: string) => {
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: message }])
    setIsLoading(true)

    try {
      const response = await sendMessage(message)
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.answer,
        mermaidChart: response.mermaid_chart,
        sources: response.sources,
      }])
    } catch {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '抱歉，發生錯誤。請稍後再試。',
      }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <header className="flex items-center gap-3 border-b border-gray-200 bg-white px-6 py-4">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-green-500 text-white">
          <Sparkles className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-lg font-semibold text-gray-900">Construction Graph RAG</h1>
          <p className="text-sm text-gray-500">營建業知識圖譜查詢系統</p>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        {messages.map((message, i) => (
          <ChatMessage key={i} message={message} />
        ))}
        {isLoading && (
          <div className="flex items-center gap-2 p-6 text-gray-500">
            <div className="h-2 w-2 animate-spin rounded-full bg-blue-500" />
            <div className="h-2 w-2 animate-spin rounded-full bg-blue-500 delay-75" />
            <div className="h-2 w-2 animate-spin rounded-full bg-blue-500 delay-150" />
            <span>思考中...</span>
          </div>
        )}
      </div>

      {/* Input */}
      <ChatInput onSubmit={handleSubmit} />
    </div>
  )
}
