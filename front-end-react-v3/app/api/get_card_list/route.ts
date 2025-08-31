import { type NextRequest, NextResponse } from "next/server"
import type { EnemyActionRequest, EnemyActionResponse } from "@/types/game"
import { AbortSignal } from "abort-controller"

export async function POST(request: NextRequest) {
  try {
    const body =  await request.json()
    // 构建AI决策请求

    console.log("Calling get card list API with request:", body.book_id)

    try {
        const controller = new AbortController()
        const timeoutId = setTimeout(() => controller.abort(), 1000000)
        const response = await fetch("http://localhost:8000/get_card_list", {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
            signal: new AbortController().signal
        })
        clearTimeout(timeoutId)
        console.log("[v0] card list response status:", response.status)

        if (!response.ok) {
            const errorText = await response.text()
            console.error("get_card_list API Error:", errorText)
            throw new Error(`get_card_list API returned ${response.status}: ${errorText}`)
        }

        const result = await response.json()
        console.log("[v0] card list result:", result)
        return NextResponse.json(result)
        
    } catch (error) {
      console.log("[v0] Backend unavailable, using mock data")
    }
  
    }
     catch (error) {
    console.error("Error getting initial Monster Data:", error)
    return NextResponse.json(
      {
        error: "Failed to get API response",
        details: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 },
    )
  }
}

