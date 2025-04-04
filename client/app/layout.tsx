
import * as React from 'react';
import type { Viewport } from 'next';
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { UserProvider } from '@/contexts/user-context';
import { LocalizationProvider } from '@/components/core/localization-provider';
import '@/styles/global.css';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const viewport = { width: 'device-width', initialScale: 1 } satisfies Viewport;

interface LayoutProps {
  children: React.ReactNode;
}

export const metadata: Metadata = {
  title: "Hop On Hop Off Vietnam Official Site-The Best Sightseeing Tour in VN",
  description: "Enjoy the flexibility of all days bus tour to explore the city's sights at your leisure.The best tour in HCMC & Hanoi. Get your tickets online now & save!",
};

export default function RootLayout({ children }: LayoutProps): React.JSX.Element {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <LocalizationProvider>
          <UserProvider>
            {children}
          </UserProvider>
        </LocalizationProvider>
      </body>
    </html>
  );
}
