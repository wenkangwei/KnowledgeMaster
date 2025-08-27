"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import {
  ChevronLeft,
  ChevronRight,
  Send,
  Upload,
  ImageIcon,
  User,
  Database,
  Users,
  MessageSquare,
  Settings,
  Brain,
} from "lucide-react"

interface KnowledgeCard {
  database: string
  card_id: string
  card_name: string
  card_content: string
  points: Array<{
    point: string
    difficulty: string
  }>
}

interface ChatMessage {
  role: "user" | "assistant"
  content: string
  timestamp: Date
}

interface UserProfile {
  user_name: string
  user_desc: string
  email: string
  gender: string
  contact: string
}

const mockKnowledgeCards: KnowledgeCard[] = [
  {
    database: "Python基础",
    card_id: "py001",
    card_name: "Python变量和数据类型",
    card_content: "Python中的变量不需要声明类型，支持动态类型。主要数据类型包括整数、浮点数、字符串、布尔值等。",
    points: [
      { point: "变量命名规则", difficulty: "初级" },
      { point: "数据类型转换", difficulty: "中级" },
      { point: "内存管理机制", difficulty: "高级" },
    ],
  },
  {
    database: "Python基础",
    card_id: "py002",
    card_name: "Python函数定义",
    card_content: "函数是组织好的，可重复使用的，用来实现单一或相关联功能的代码段。",
    points: [
      { point: "函数定义语法", difficulty: "初级" },
      { point: "参数传递方式", difficulty: "中级" },
    ],
  },
  {
    database: "MySQL数据库",
    card_id: "sql001",
    card_name: "MySQL用户权限管理",
    card_content: "MySQL提供了完善的用户权限管理系统，可以精确控制用户对数据库的访问权限。",
    points: [
      { point: "创建用户账户", difficulty: "初级" },
      { point: "授予权限", difficulty: "中级" },
      { point: "权限继承机制", difficulty: "高级" },
    ],
  },
  {
    database: "MySQL数据库",
    card_id: "sql002",
    card_name: "SQL查询优化",
    card_content: "通过索引、查询重写、执行计划分析等方式优化SQL查询性能。",
    points: [
      { point: "索引使用策略", difficulty: "中级" },
      { point: "执行计划分析", difficulty: "高级" },
    ],
  },
  {
    database: "Web开发",
    card_id: "web001",
    card_name: "React组件生命周期",
    card_content: "React组件从创建到销毁的完整过程，包括挂载、更新和卸载三个阶段。",
    points: [
      { point: "组件挂载过程", difficulty: "中级" },
      { point: "状态更新机制", difficulty: "中级" },
      { point: "性能优化技巧", difficulty: "高级" },
    ],
  },
  {
    database: "Web开发",
    card_id: "web002",
    card_name: "CSS布局技术",
    card_content: "现代CSS布局包括Flexbox、Grid、定位等多种技术，用于创建响应式网页布局。",
    points: [
      { point: "Flexbox布局", difficulty: "中级" },
      { point: "Grid网格系统", difficulty: "中级" },
    ],
  },
]

const telegramGradients = [
  "bg-gradient-to-br from-blue-500 to-purple-600",
  "bg-gradient-to-br from-green-500 to-teal-600",
  "bg-gradient-to-br from-orange-500 to-red-600",
  "bg-gradient-to-br from-purple-500 to-pink-600",
  "bg-gradient-to-br from-indigo-500 to-blue-600",
  "bg-gradient-to-br from-teal-500 to-green-600",
  "bg-gradient-to-br from-pink-500 to-rose-600",
  "bg-gradient-to-br from-cyan-500 to-blue-600",
  "bg-gradient-to-br from-emerald-500 to-teal-600",
  "bg-gradient-to-br from-violet-500 to-purple-600",
  "bg-gradient-to-br from-amber-500 to-orange-600",
  "bg-gradient-to-br from-rose-500 to-pink-600",
]

const getCardGradient = (cardId: string) => {
  const hash = cardId.split("").reduce((acc, char) => acc + char.charCodeAt(0), 0)
  return telegramGradients[hash % telegramGradients.length]
}

export default function KnowledgeChatApp() {
  const [activeTab, setActiveTab] = useState<"personal" | "knowledge" | "community">("personal")
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [chatMode, setChatMode] = useState(false)
  const [knowledgeCards, setKnowledgeCards] = useState<KnowledgeCard[]>([])
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([])
  const [inputValue, setInputValue] = useState("")
  const [selectedCard, setSelectedCard] = useState<KnowledgeCard | null>(null)
  const [userProfile, setUserProfile] = useState<UserProfile>({
    user_name: "",
    user_desc: "",
    email: "",
    gender: "",
    contact: "",
  })
  const [databases, setDatabases] = useState<string[]>([])
  const [selectedDatabase, setSelectedDatabase] = useState<string>("")
  const [reviewHistory, setReviewHistory] = useState<KnowledgeCard[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const fileInputRef = useRef<HTMLInputElement>(null)
  const imageInputRef = useRef<HTMLInputElement>(null)
  const chatScrollRef = useRef<HTMLDivElement>(null)

  // Fetch knowledge cards on component mount
  useEffect(() => {
    fetchKnowledgeCards()
  }, [])

  // Auto-scroll chat to bottom
  useEffect(() => {
    if (chatScrollRef.current) {
      chatScrollRef.current.scrollTop = chatScrollRef.current.scrollHeight
    }
  }, [chatMessages])

  const sendPostRequest = async (requestType: string, data: any, files?: File[]) => {
    try {
      console.log("[v0] Attempting backend connection...")

      // Handle file uploads first if any
      let uploadedFilePaths: string[] = []
      if (files && files.length > 0) {
        uploadedFilePaths = await uploadFiles(files)
      }

      const requestBody = {
        type: requestType,
        data: {
          ...data,
          uploaded_files: uploadedFilePaths,
        },
      }

      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 second timeout

      const response = await fetch("http://localhost:8080/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal,
      })

      clearTimeout(timeoutId)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      console.log("[v0] Backend connected successfully!")
      return result
    } catch (error) {
      console.log("[v0] Backend unavailable, using mock data")
      // Return mock data as fallback
      return getMockResponse(requestType, data)
    }
  }

  const uploadFiles = async (files: File[]): Promise<string[]> => {
    const uploadedPaths: string[] = []

    for (const file of files) {
      try {
        // Generate unique filename
        const timestamp = Date.now()
        const filename = `${timestamp}_${file.name}`

        const localPath = `/uploads/${filename}`
        uploadedPaths.push(localPath)

        console.log("[v0] File prepared for upload:", { originalName: file.name, localPath, size: file.size })
      } catch (error) {
        console.error("[v0] File preparation failed:", error)
      }
    }

    return uploadedPaths
  }

  const getMockResponse = (requestType: string, data: any) => {
    switch (requestType) {
      case "knowledge_cards":
        return {
          cards: mockKnowledgeCards,
          status: "success",
          message: "Using mock knowledge cards",
        }
      case "database_cards":
        return {
          cards: mockKnowledgeCards.filter((card) => card.database === data.database_name),
          status: "success",
          message: `Filtered cards for ${data.database_name}`,
        }
      case "chat_message":
        let mockResponse = "这是一个模拟的AI回复。由于后端服务器未连接，我正在使用本地模拟数据为您提供回答。"

        if (data.uploaded_files && data.uploaded_files.length > 0) {
          mockResponse =
            `我看到您上传了 ${data.uploaded_files.length} 个文件: ${data.uploaded_files.join(", ")}` +
            "由于后端服务器未连接，我无法处理这些文件，但在实际环境中，我会分析这些文件并为您提供相关回答。"
        } else if (data.message.toLowerCase().includes("python")) {
          mockResponse =
            "Python是一种高级编程语言，以其简洁的语法和强大的功能而闻名。它广泛应用于数据科学、Web开发、人工智能等领域。Python的设计哲学强调代码的可读性和简洁的语法。"
        } else if (data.message.toLowerCase().includes("mysql") || data.message.toLowerCase().includes("数据库")) {
          mockResponse =
            "MySQL是一个开源的关系型数据库管理系统，支持SQL查询语言。它具有高性能、可靠性强、易于使用等特点。MySQL广泛用于Web应用程序，是LAMP技术栈的重要组成部分。"
        } else if (data.message.toLowerCase().includes("react") || data.message.toLowerCase().includes("前端")) {
          mockResponse =
            "React是Facebook开发的用于构建用户界面的JavaScript库。它采用组件化开发模式，支持虚拟DOM，提供了高效的页面渲染机制。React的核心概念包括组件、状态管理和生命周期。"
        }

        return {
          response: mockResponse,
          status: "success",
          message: "Mock response generated",
        }
      default:
        return {
          error: "Unknown request type",
          status: "error",
        }
    }
  }

  const fetchKnowledgeCards = async () => {
    try {
      setIsLoading(true)
      const result = await sendPostRequest("knowledge_cards", {})

      if (result.cards) {
        setKnowledgeCards(result.cards)
        const uniqueDatabases = [...new Set(result.cards.map((card: KnowledgeCard) => card.database))]
        setDatabases(uniqueDatabases)
      }
    } catch (error) {
      console.log("[v0] Using fallback mock data")
      setKnowledgeCards(mockKnowledgeCards)
      const uniqueDatabases = [...new Set(mockKnowledgeCards.map((card: KnowledgeCard) => card.database))]
      setDatabases(uniqueDatabases)
    } finally {
      setIsLoading(false)
    }
  }

  const fetchDatabaseCards = async (databaseName: string) => {
    try {
      setIsLoading(true)
      const result = await sendPostRequest("database_cards", { database_name: databaseName })

      if (result.cards) {
        setKnowledgeCards(result.cards)
      }
    } catch (error) {
      console.log("[v0] Using filtered mock data for database:", databaseName)
      const filteredCards = mockKnowledgeCards.filter((card) => card.database === databaseName)
      setKnowledgeCards(filteredCards)
    } finally {
      setIsLoading(false)
    }
  }

  const sendMessage = async (files?: File[]) => {
    if (!inputValue.trim() && (!files || files.length === 0)) return

    const userMessage: ChatMessage = {
      role: "user",
      content: inputValue || (files ? `上传了 ${files.length} 个文件: ${files.map((f) => f.name).join(", ")}` : ""),
      timestamp: new Date(),
    }

    setChatMessages((prev) => [...prev, userMessage])
    const currentInput = inputValue
    setInputValue("")
    setIsLoading(true)
    setChatMode(true)

    try {
      const result = await sendPostRequest(
        "chat_message",
        {
          message: currentInput,
          user_profile: userProfile,
          context: selectedCard ? { card_id: selectedCard.card_id } : null,
        },
        files,
      )

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: result.response || "抱歉，我无法处理您的请求。",
        timestamp: new Date(),
      }

      setChatMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: ChatMessage = {
        role: "assistant",
        content: "抱歉，系统出现了问题。请稍后再试。",
        timestamp: new Date(),
      }
      setChatMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleFileUpload = (type: "file" | "image") => {
    if (type === "file") {
      fileInputRef.current?.click()
    } else {
      imageInputRef.current?.click()
    }
  }

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (files && files.length > 0) {
      const fileArray = Array.from(files)
      sendMessage(fileArray)
    }
    // Reset input
    event.target.value = ""
  }

  const handleCardClick = (card: KnowledgeCard) => {
    setSelectedCard(card)
    setReviewHistory((prev) => {
      const exists = prev.find((c) => c.card_id === card.card_id)
      if (!exists) {
        return [...prev, card]
      }
      return prev
    })
  }

  const renderKnowledgeCards = () => {
    if (chatMode) {
      return (
        <div className="flex-1 flex flex-col">
          <div className="flex items-center justify-between p-4 border-b bg-card">
            <h2 className="text-lg font-semibold">对话</h2>
            <Button variant="ghost" size="sm" onClick={() => setChatMode(false)}>
              返回卡片
            </Button>
          </div>
          <ScrollArea className="flex-1 p-4" ref={chatScrollRef}>
            <div className="space-y-4">
              {chatMessages.map((message, index) => (
                <div key={index} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[80%] p-3 rounded-lg ${
                      message.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
                    }`}
                  >
                    <p className="text-sm">{message.content}</p>
                    <p className="text-xs opacity-70 mt-1">{message.timestamp.toLocaleTimeString()}</p>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-muted text-muted-foreground p-3 rounded-lg">
                    <p className="text-sm">正在思考...</p>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>
        </div>
      )
    }

    return (
      <ScrollArea className="flex-1 p-4">
        <div className="grid grid-cols-2 gap-4">
          {knowledgeCards.map((card) => (
            <Card
              key={card.card_id}
              className="cursor-pointer hover:shadow-lg transition-all duration-300 hover:scale-105 border-0 overflow-hidden"
              onClick={() => handleCardClick(card)}
            >
              <div className={`${getCardGradient(card.card_id)} p-4 text-white`}>
                <div className="flex items-center justify-between mb-2">
                  <Badge variant="secondary" className="text-xs bg-white/20 text-white border-white/30">
                    {card.database}
                  </Badge>
                  <Brain className="h-4 w-4 text-white/80" />
                </div>
                <CardTitle className="text-sm font-medium line-clamp-2 text-white">{card.card_name}</CardTitle>
              </div>
              <CardContent className="pt-3 pb-4 px-4 bg-white">
                <p className="text-xs text-muted-foreground line-clamp-3 mb-3">{card.card_content}</p>
                <div className="flex flex-wrap gap-1">
                  {card.points.slice(0, 2).map((point, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {point.difficulty}
                    </Badge>
                  ))}
                  {card.points.length > 2 && (
                    <Badge variant="outline" className="text-xs">
                      +{card.points.length - 2}
                    </Badge>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </ScrollArea>
    )
  }

  const renderTabContent = () => {
    switch (activeTab) {
      case "knowledge":
        return (
          <div className="flex-1 flex flex-col">
            <div className="p-4 border-b bg-card">
              <h2 className="text-lg font-semibold mb-3">知识库</h2>
              <div className="grid grid-cols-2 gap-2">
                {databases.map((db, index) => (
                  <Card
                    key={db}
                    className={`cursor-pointer transition-all duration-300 hover:scale-105 border-0 overflow-hidden ${
                      selectedDatabase === db ? "ring-2 ring-primary" : ""
                    }`}
                    onClick={() => {
                      setSelectedDatabase(db)
                      fetchDatabaseCards(db)
                    }}
                  >
                    <div className={`${telegramGradients[index % telegramGradients.length]} p-3`}>
                      <div className="flex items-center space-x-2">
                        <Database className="h-4 w-4 text-white" />
                        <span className="text-sm font-medium text-white">{db}</span>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
            {renderKnowledgeCards()}
          </div>
        )
      case "community":
        return (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <Users className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">社区功能</h3>
              <p className="text-muted-foreground">即将推出...</p>
            </div>
          </div>
        )
      default:
        return renderKnowledgeCards()
    }
  }

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Top Navigation */}
      <div className="flex items-center justify-center border-b bg-card px-4 py-3">
        <div className="flex space-x-8">
          {[
            { key: "personal", label: "个人", icon: User },
            { key: "knowledge", label: "知识库", icon: Database },
            { key: "community", label: "社区", icon: Users },
          ].map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setActiveTab(key as any)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                activeTab === key
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted"
              }`}
            >
              <Icon className="h-4 w-4" />
              <span className="font-medium">{label}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 flex">
        {/* Sidebar */}
        <div
          className={`${sidebarCollapsed ? "w-0" : "w-80"} transition-all duration-300 border-r bg-sidebar overflow-hidden`}
        >
          <div className="p-4 space-y-4">
            {/* User Profile Section */}
            <Card>
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-sm">个人信息</CardTitle>
                  <Settings className="h-4 w-4 text-muted-foreground" />
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center space-x-3">
                  <Avatar>
                    <AvatarImage src="/placeholder.svg?height=40&width=40" />
                    <AvatarFallback>{userProfile.user_name ? userProfile.user_name[0] : "U"}</AvatarFallback>
                  </Avatar>
                  <div className="flex-1">
                    <Input
                      placeholder="用户名"
                      value={userProfile.user_name}
                      onChange={(e) => setUserProfile((prev) => ({ ...prev, user_name: e.target.value }))}
                      className="text-sm"
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <Input
                    placeholder="邮箱"
                    value={userProfile.email}
                    onChange={(e) => setUserProfile((prev) => ({ ...prev, email: e.target.value }))}
                    className="text-sm"
                  />
                  <Input
                    placeholder="联系方式"
                    value={userProfile.contact}
                    onChange={(e) => setUserProfile((prev) => ({ ...prev, contact: e.target.value }))}
                    className="text-sm"
                  />
                  <Textarea
                    placeholder="个人描述"
                    value={userProfile.user_desc}
                    onChange={(e) => setUserProfile((prev) => ({ ...prev, user_desc: e.target.value }))}
                    className="text-sm resize-none"
                    rows={2}
                  />
                </div>
              </CardContent>
            </Card>

            <Separator />

            {/* Review History */}
            <div>
              <h3 className="text-sm font-semibold mb-3 flex items-center">
                <MessageSquare className="h-4 w-4 mr-2" />
                复习历史
              </h3>
              <ScrollArea className="h-64">
                <div className="space-y-2">
                  {reviewHistory.map((card) => (
                    <Card
                      key={card.card_id}
                      className="cursor-pointer hover:bg-muted transition-colors"
                      onClick={() => setSelectedCard(card)}
                    >
                      <CardContent className="p-3">
                        <p className="text-xs font-medium line-clamp-1">{card.card_name}</p>
                        <p className="text-xs text-muted-foreground line-clamp-2 mt-1">{card.card_content}</p>
                        <Badge variant="outline" className="text-xs mt-2">
                          {card.database}
                        </Badge>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </ScrollArea>
            </div>
          </div>
        </div>

        {/* Sidebar Toggle */}
        <Button
          variant="ghost"
          size="sm"
          className="absolute left-80 top-1/2 transform -translate-y-1/2 z-10 transition-all duration-300"
          style={{ left: sidebarCollapsed ? "0" : "320px" }}
          onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
        >
          {sidebarCollapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </Button>

        {/* Main Content */}
        <div className="flex-1 flex flex-col">
          {renderTabContent()}

          {/* Fixed Bottom Input */}
          <div className="border-t bg-card p-4">
            <div className="max-w-4xl mx-auto">
              <div className="flex items-end space-x-2">
                <div className="flex-1">
                  <Textarea
                    placeholder="输入您的问题..."
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" && !e.shiftKey) {
                        e.preventDefault()
                        sendMessage()
                      }
                    }}
                    className="resize-none"
                    rows={1}
                  />
                </div>
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm" onClick={() => handleFileUpload("image")}>
                    <ImageIcon className="h-4 w-4" />
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => handleFileUpload("file")}>
                    <Upload className="h-4 w-4" />
                  </Button>
                  <Button onClick={() => sendMessage()} disabled={!inputValue.trim() || isLoading}>
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        accept=".pdf,.doc,.docx,.txt"
        onChange={handleFileChange}
        multiple
      />
      <input ref={imageInputRef} type="file" className="hidden" accept="image/*" onChange={handleFileChange} multiple />

      {/* Knowledge Card Detail Modal */}
      {selectedCard && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-2xl w-full max-h-[80vh] overflow-hidden">
            <CardHeader className="border-b">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>{selectedCard.card_name}</CardTitle>
                  <Badge variant="secondary" className="mt-2">
                    {selectedCard.database}
                  </Badge>
                </div>
                <Button variant="ghost" size="sm" onClick={() => setSelectedCard(null)}>
                  ×
                </Button>
              </div>
            </CardHeader>
            <CardContent className="p-6">
              <ScrollArea className="max-h-96">
                <div className="space-y-4">
                  <div>
                    <h4 className="font-semibold mb-2">内容概述</h4>
                    <p className="text-sm text-muted-foreground">{selectedCard.card_content}</p>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-3">知识点</h4>
                    <div className="space-y-3">
                      {selectedCard.points.map((point, index) => (
                        <div key={index} className="flex items-start space-x-3 p-3 bg-muted rounded-lg">
                          <div className="flex-1">
                            <p className="text-sm">{point.point}</p>
                          </div>
                          <Badge variant="outline" className="text-xs">
                            {point.difficulty}
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
