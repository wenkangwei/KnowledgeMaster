"use client"

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

  const fetchKnowledgeCards = async () => {
    try {
      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 500))

      setKnowledgeCards(mockKnowledgeCards)

      // Extract unique databases
      const uniqueDatabases = [...new Set(mockKnowledgeCards.map((card: KnowledgeCard) => card.database))]
      setDatabases(uniqueDatabases)
    } catch (error) {
      console.error("Failed to fetch knowledge cards:", error)
    }
  }

  const fetchDatabaseCards = async (databaseName: string) => {
    try {
      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 300))

      const filteredCards = mockKnowledgeCards.filter((card) => card.database === databaseName)
      setKnowledgeCards(filteredCards)
    } catch (error) {
      console.error("Failed to fetch database cards:", error)
    }
  }

  const sendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: ChatMessage = {
      role: "user",
      content: inputValue,
      timestamp: new Date(),
    }

    setChatMessages((prev) => [...prev, userMessage])
    const currentInput = inputValue
    setInputValue("")
    setIsLoading(true)
    setChatMode(true)

    try {
      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 1000))

      // Generate mock response based on input
      let mockResponse = "这是一个模拟的AI回复。"

      if (currentInput.toLowerCase().includes("python")) {
        mockResponse =
          "Python是一种高级编程语言，以其简洁的语法和强大的功能而闻名。它广泛应用于数据科学、Web开发、人工智能等领域。"
      } else if (currentInput.toLowerCase().includes("mysql") || currentInput.toLowerCase().includes("数据库")) {
        mockResponse =
          "MySQL是一个开源的关系型数据库管理系统，支持SQL查询语言。它具有高性能、可靠性强、易于使用等特点。"
      } else if (currentInput.toLowerCase().includes("react") || currentInput.toLowerCase().includes("前端")) {
        mockResponse =
          "React是Facebook开发的用于构建用户界面的JavaScript库。它采用组件化开发模式，支持虚拟DOM，提供了高效的页面渲染机制。"
      }

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: mockResponse,
        timestamp: new Date(),
      }

      setChatMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error("Failed to send message:", error)
    } finally {
      setIsLoading(false)
    }
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

  const handleFileUpload = (type: "file" | "image") => {
    if (type === "file") {
      fileInputRef.current?.click()
    } else {
      imageInputRef.current?.click()
    }
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
              className="cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => handleCardClick(card)}
            >
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <Badge variant="secondary" className="text-xs">
                    {card.database}
                  </Badge>
                  <Brain className="h-4 w-4 text-muted-foreground" />
                </div>
                <CardTitle className="text-sm font-medium line-clamp-2">{card.card_name}</CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <p className="text-xs text-muted-foreground line-clamp-3">{card.card_content}</p>
                <div className="mt-2 flex flex-wrap gap-1">
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
                {databases.map((db) => (
                  <Card
                    key={db}
                    className={`cursor-pointer transition-colors ${
                      selectedDatabase === db ? "bg-primary text-primary-foreground" : "hover:bg-muted"
                    }`}
                    onClick={() => {
                      setSelectedDatabase(db)
                      fetchDatabaseCards(db)
                    }}
                  >
                    <CardContent className="p-3">
                      <div className="flex items-center space-x-2">
                        <Database className="h-4 w-4" />
                        <span className="text-sm font-medium">{db}</span>
                      </div>
                    </CardContent>
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
                  <Button onClick={sendMessage} disabled={!inputValue.trim() || isLoading}>
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Hidden File Inputs */}
      <input ref={fileInputRef} type="file" className="hidden" accept=".pdf,.doc,.docx,.txt" />
      <input ref={imageInputRef} type="file" className="hidden" accept="image/*" />

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
