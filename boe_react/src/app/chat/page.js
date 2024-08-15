"use client";
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Montserrat } from 'next/font/google';

const montserrat = Montserrat({ subsets: ['latin'] });

const ChatScreen = () => {
  const router = useRouter();
  const [question, setQuestion] = useState('');
  const [chat, setChat] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    if (router.isReady) {
      const { question } = router.query;
      if (question) {
        setQuestion(decodeURIComponent(question));
        setChat([
          { role: 'user', content: decodeURIComponent(question) },
          { role: 'assistant', content: 'Thank you for your question. I am processing it now...' }
        ]);
      }
    }
  }, [router.isReady, router.query]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (newMessage.trim()) {
      setChat([...chat, { role: 'user', content: newMessage }]);
      setNewMessage('');
      // Simulate BOE-GPT response
      setTimeout(() => {
        setChat(prevChat => [...prevChat, { role: 'assistant', content: `I've received your message: "${newMessage}". How can I assist you further?` }]);
      }, 1000);
    }
  };

  return (
    <div className={`min-h-screen bg-black text-white flex flex-col ${montserrat.className}`}>
      <header className="bg-gray-900 p-4">
        <h1 className="text-2xl font-bold">BOE-GPT Chat</h1>
      </header>
      <div className="flex-grow overflow-auto p-4 space-y-4">
        {chat.map((message, index) => (
          <div key={index} className={`max-w-3/4 ${message.role === 'user' ? 'ml-auto' : 'mr-auto'}`}>
            <div className={`rounded-lg p-3 ${message.role === 'user' ? 'bg-blue-600' : 'bg-gray-700'}`}>
              {message.content}
            </div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSendMessage} className="p-4 bg-gray-900">
        <div className="flex space-x-2">
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-grow px-4 py-2 rounded-full bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button 
            type="submit"
            className="px-6 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors disabled:bg-gray-500 disabled:cursor-not-allowed"
            disabled={!newMessage.trim()}
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatScreen;