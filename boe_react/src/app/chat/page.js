"use client";
import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Montserrat } from 'next/font/google';

const montserrat = Montserrat({ subsets: ['latin'] });

const ChatScreen = () => {
  const router = useRouter();
  const [question, setQuestion] = useState('');
  const [chat, setChat] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (router.isReady) {
      const { question } = router.query;
      if (question) {
        setQuestion(decodeURIComponent(question));
        setChat([
          { role: 'user', content: decodeURIComponent(question) },
          { role: 'assistant', content: 'Thank you for your question. I am processing it now...' }
        ]);
        handleSendMessage(null, decodeURIComponent(question));
      }
    }
  }, [router.isReady, router.query]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chat]);

  const handleSendMessage = async (e, initialQuestion = null) => {
    e?.preventDefault();
    const messageToSend = initialQuestion || newMessage.trim();
    if (messageToSend) {
      setChat(prev => [...prev, { role: 'user', content: messageToSend }]);
      setNewMessage('');
      setIsLoading(true);

      try {
        const response = await fetch('http://127.0.0.1:3550/chat_stream', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: `query=${encodeURIComponent(messageToSend)}`,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let assistantMessage = '';

        setChat(prev => [...prev, { role: 'assistant', content: '' }]);

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          
          const chunk = decoder.decode(value);
          assistantMessage += chunk;
          
          setChat(prev => {
            const newChat = [...prev];
            newChat[newChat.length - 1] = { role: 'assistant', content: assistantMessage };
            return newChat;
          });
        }
      } catch (error) {
        console.error('Error:', error);
        setChat(prev => [...prev, { role: 'assistant', content: 'Lo siento, ha ocurrido un error al procesar tu mensaje.' }]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className={`min-h-screen bg-black text-white flex flex-col ${montserrat.className}`}>
      <header className="bg-gray-900 p-4">
        <h1 className="text-2xl font-bold">Chat</h1>
      </header>
      <div className="flex-grow overflow-auto p-4 space-y-4">
        {chat.map((message, index) => (
          <div key={index} className={`max-w-3/4 ${message.role === 'user' ? 'ml-auto' : 'mr-auto'}`}>
            <div className={`rounded-lg p-3 ${message.role === 'user' ? 'bg-blue-600' : 'bg-gray-700'}`}>
              {message.content}
            </div>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <form onSubmit={handleSendMessage} className="p-4 bg-gray-900">
        <div className="flex space-x-2">
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Escribe tu mensaje..."
            className="flex-grow px-4 py-2 rounded-full bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button 
            type="submit"
            className="px-6 py-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors disabled:bg-gray-500 disabled:cursor-not-allowed"
            disabled={!newMessage.trim() || isLoading}
          >
            {isLoading ? 'Enviando...' : 'Enviar'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatScreen;