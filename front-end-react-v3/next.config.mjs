/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },

  compiler: {
    removeConsole: process.env.NODE_ENV === 'production' // 生产环境才移除
  }
}

export default nextConfig
