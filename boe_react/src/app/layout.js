import React from 'react';
import { Montserrat } from 'next/font/google';
import "./globals.css";

const montserrat = Montserrat({ subsets: ['latin'] });

export const metadata = {
  title: "BOE-GPT",
  description: "Autor: Javier Cervera",
};

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <div className={`min-h-screen bg-black ${montserrat.className}`}>
          {children}
        </div>
      </body>
    </html>
  );
}
