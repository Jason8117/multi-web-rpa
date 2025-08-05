import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    appDir: true,
  },
  output: 'standalone',
  trailingSlash: false,
};

export default nextConfig;
