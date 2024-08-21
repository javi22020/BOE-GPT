"use client";
import React from 'react';
import { useRouter } from 'next/navigation';
import { Montserrat } from 'next/font/google';
import { MessageSquare, Settings } from 'lucide-react';

const montserrat = Montserrat({ subsets: ['latin'] });

const MainPage = () => {
  const router = useRouter();

  const navigateToChat = () => {
    router.push('/chat');
  };

  const navigateToSettings = () => {
    router.push('/settings');
  };

  return (
    <div className={`min-h-screen bg-black flex flex-col items-center justify-center ${montserrat.className}`}>
      <h1 className="text-6xl font-bold text-white mb-8">BOE-GPT</h1>
      <div className="flex space-x-4">
        <button
          onClick={navigateToChat}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded flex items-center transition duration-300"
        >
          <MessageSquare className="mr-2" size={20} />
          Chat
        </button>
        <button
          onClick={navigateToSettings}
          className="bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded flex items-center transition duration-300"
        >
          <Settings className="mr-2" size={20} />
          Settings
        </button>
      </div>
    </div>
  );
};

export default MainPage;