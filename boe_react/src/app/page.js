"use client";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Montserrat } from 'next/font/google';

const montserrat = Montserrat({ subsets: ['latin'] });

const MainPage = () => {
  const [question, setQuestion] = useState('');
  const router = useRouter();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim()) {
      router.push(`/chat?question=${encodeURIComponent(question)}`);
    }
  };

  return (
    <div className={`min-h-screen bg-black flex flex-col items-center justify-center ${montserrat.className}`}>
      <h1 className="text-6xl font-bold text-white mb-8">BOE-GPT</h1>
      <form onSubmit={handleSubmit} className="w-full max-w-md">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question..."
          className="w-full px-4 py-2 rounded-full bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button 
          type="submit"
          className="mt-4 w-full px-6 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors disabled:bg-gray-500 disabled:cursor-not-allowed"
          disabled={!question.trim()}
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default MainPage;