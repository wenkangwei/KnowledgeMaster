// import { type NextRequest, NextResponse } from "next/server"
// import type { EnemyActionRequest, EnemyActionResponse } from "@/types/game"
// import { AbortSignal } from "abort-controller"


// export async function POST (request: NextRequest) {
//     const body = await request.json()
//     const files: File[] = body.paths
//     console.log("[v0] Starting file download process for", files.length, "files")
//     const downloadedPaths: string[] = []

//     for (const file of  files) {
//       try {
//         // 创建文件的Blob URL并下载到本地
//         const blob = new Blob([file], { type: file.type })
//         const blobUrl = URL.createObjectURL(blob)
        
//         // 创建下载链接
//         const downloadLink = document.createElement('a')
//         downloadLink.href = blobUrl
        
//         // 设置绝对路径（这里使用用户下载目录）
//         const timestamp = Date.now()
//         const filename = `${timestamp}_${file.name}`
//         const absolutePath = `./upload/${filename}` // 修改为你的绝对路径
        
//         downloadLink.download = filename
//         document.body.appendChild(downloadLink)
//         downloadLink.click()
//         document.body.removeChild(downloadLink)
        
//         // 释放Blob URL
//         URL.revokeObjectURL(blobUrl)
        
//         downloadedPaths.push(absolutePath)
//         console.log("[v0] File downloaded to:", absolutePath)

//       } catch (error) {
//         console.error("[v0] File download failed:", error)
//         // 即使下载失败，也返回一个模拟路径继续流程
//         downloadedPaths.push(`./upload/${Date.now()}_${file.name}`)
//       }
//     }

//     console.log("[v0] File download process completed, paths:", downloadedPaths)
//     return NextResponse.json( {files :downloadedPaths})

// }

// // export async function POST(request: NextRequest) {
// //   try {
// //     const body =  await request.json()
// //     // 构建AI决策请求

// //     console.log("Calling get_card_recom API with request:", body)

// //     try {
// //         const controller = new AbortController()
// //         const timeoutId = setTimeout(() => controller.abort(), 1000000)
// //         const response = await fetch("http://localhost:8000/get_card_recom", {
// //             method: "POST",
// //             headers: {
// //             "Content-Type": "application/json",
// //             },
// //             body: JSON.stringify(body),
// //             signal: new AbortController().signal
// //         })
// //         clearTimeout(timeoutId)
// //         console.log("[v0] get_card_recom response status:", response.status)

// //         if (!response.ok) {
// //             const errorText = await response.text()
// //             console.error("get_card_recom API Error:", errorText)
// //             throw new Error(`get_card_recom API returned ${response.status}: ${errorText}`)
// //         }

// //         const result = await response.json()
// //         console.log("[v0] get_card_recom result:", result)
// //         return NextResponse.json(result)
        
// //     } catch (error) {
// //       console.log("[v0] Backend unavailable, using mock data")
// //     }
  
// //     }
// //      catch (error) {
// //     console.error("Error get_card_recom Data:", error)
// //     return NextResponse.json(
// //       {
// //         error: "Failed to get API response",
// //         details: error instanceof Error ? error.message : "Unknown error",
// //       },
// //       { status: 500 },
// //     )
// //   }
// // }


import { NextResponse } from "next/server";
import { revalidatePath } from "next/cache";
import fs from "node:fs/promises";

export async function POST(req: Request) {
  try {
    const formData = await req.formData();
    console.log("upload file POST", formData);
    const file = formData.get("file") as File;

    if (!file) {
      return NextResponse.json({ status: "success", files: [''] });;
}

    const arrayBuffer = await file.arrayBuffer();
    const buffer = new Uint8Array(arrayBuffer);
    await fs.writeFile(`./public/uploads/${file.name}`, buffer);

    revalidatePath("/");

    return NextResponse.json({ status: "success", files: [`./public/uploads/${file.name}`] });
  } catch (e) {
    console.error(e);
    return NextResponse.json({ status: "fail", error: e, files: [] });
  }
}
