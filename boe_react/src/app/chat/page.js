"use client";
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, User, Bot } from 'lucide-react';

// Función de logging simple
const log = (message, data = '') => {
  console.log(`[ChatPage] ${message}`, data);
};

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
    log('Mensajes actualizados', messages);
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (inputMessage.trim() === '') return;

    setIsLoading(true);
    log('Enviando mensaje', inputMessage);
    setMessages(prev => [...prev, { text: inputMessage, sender: 'user' }]);
    setInputMessage('');

    try {
      const response = await axios.post('http://127.0.0.1:3550/chat', { query: inputMessage });
      log('Respuesta recibida', response.data);
      setMessages(prev => [...prev, { text: response.data.content, sender: 'bot' }]);
    } catch (error) {
      log('Error en la solicitud', error);
      setMessages(prev => [...prev, { text: 'Error al obtener la respuesta.', sender: 'bot' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto p-4">
      <div className="flex-grow overflow-auto mb-4 border border-gray-300 rounded-lg p-4">
        {messages.map((message, index) => (
          <div key={index} className={`mb-2 flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex items-center ${message.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              <span className={`inline-block p-2 rounded-lg ${message.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'}`}>
                {message.text}
              </span>
              <span className="mx-2">
                {message.sender === 'user' ? <User size={24} /> : <Bot size={24} />}
              </span>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Escribe tu mensaje aquí..."
          disabled={isLoading}
          className="flex-grow p-2 border border-gray-300 rounded-lg"
        />
        <button 
          type="submit" 
          disabled={isLoading || inputMessage.trim() === ''}
          className="p-2 bg-blue-500 text-white rounded-lg disabled:bg-gray-300"
        >
          <Send size={24} />
        </button>
      </form>
    </div>
  );
};

export default ChatPage;