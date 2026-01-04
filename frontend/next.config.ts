/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  // تفعيل دعم الـ Docker
  output: 'standalone', 
};

export default nextConfig;