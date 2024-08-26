"use client";
import React, { useState, useEffect, useRef, createContext, useContext } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { Send, User, Bot, Settings, Sun, Moon } from 'lucide-react';

// Configuración de Axios
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3550',
  withCredentials: true,
});

// Función de logging simple
const log = (message, data = '') => {
  console.log(`[ChatPage] ${message}`, data);
};

// Contexto del tema
const ThemeContext = createContext();

// Hook personalizado para usar el tema
const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme debe ser usado dentro de un ThemeProvider');
  }
  return context;
};

// Proveedor del tema
const ThemeProvider = ({ children }) => {
  const [darkMode, setDarkMode] = useState(false);

  const toggleTheme = () => {
    setDarkMode(!darkMode);
  };

  return (
    <ThemeContext.Provider value={{ darkMode, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

const ChatPage = () => {
  const { darkMode, toggleTheme } = useTheme();
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const router = useRouter();

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
      const response = await api.post('/chat', { query: inputMessage });
      log('Respuesta recibida', response.data);
      
      const botResponse = response.data;
      
      setMessages(prev => [...prev, { text: botResponse, sender: 'bot' }]);
    } catch (error) {
      log('Error en la solicitud', error);
      setMessages(prev => [...prev, { text: 'Error al obtener la respuesta.', sender: 'bot' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSettingsClick = () => {
    router.push('/settings');
  };

  return (
    <div className={`flex flex-col h-screen ${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-900'}`}>
      {/* Barra superior */}
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-blue-600'} text-white p-4 flex justify-between items-center`}>
        <h1 className="text-xl font-bold">Chat BOE</h1>
        <div className="flex items-center">
          <button onClick={toggleTheme} className="p-2 mr-2 hover:bg-opacity-20 hover:bg-white rounded-full">
            {darkMode ? <Sun size={24} /> : <Moon size={24} />}
          </button>
          <button onClick={handleSettingsClick} className="p-2 hover:bg-opacity-20 hover:bg-white rounded-full">
            <Settings size={24} />
          </button>
        </div>
      </div>

      {/* Área de mensajes */}
      <div className={`flex-grow overflow-auto p-4 ${darkMode ? 'bg-gray-800' : 'bg-gray-100'}`}>
        {messages.map((message, index) => (
          <div key={index} className={`mb-4 flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex items-end max-w-3/4 ${message.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              <div className={`p-3 rounded-lg ${
                message.sender === 'user'
                  ? 'bg-blue-500 text-white'
                  : darkMode ? 'bg-gray-700 text-white' : 'bg-white text-gray-900'
              } ${message.sender === 'user' ? 'rounded-br-none' : 'rounded-bl-none'} shadow-md`}>
                {message.text}
              </div>
              <div className={`${message.sender === 'user' ? 'mr-2' : 'ml-2'} mb-1`}>
                {message.sender === 'user' 
                  ? <User size={24} className="text-blue-500" />
                  : <Bot size={24} className={darkMode ? 'text-gray-400' : 'text-gray-600'} />
                }
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Área de entrada de mensaje */}
      <form onSubmit={handleSubmit} className={`${darkMode ? 'bg-gray-800' : 'bg-white'} p-4 flex items-center`}>
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Escribe tu mensaje aquí..."
          disabled={isLoading}
          className={`flex-grow p-2 border ${
            darkMode ? 'bg-gray-700 text-white border-gray-600' : 'bg-white text-gray-900 border-gray-300'
          } rounded-lg mr-2 focus:outline-none focus:ring-2 focus:ring-blue-500`}
        />
        <button 
          type="submit" 
          disabled={isLoading || inputMessage.trim() === ''}
          className={`p-2 ${
            darkMode 
              ? 'bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700' 
              : 'bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300'
          } text-white rounded-lg disabled:text-gray-400 transition-colors`}
        >
          <Send size={24} />
        </button>
      </form>
    </div>
  );
};

const ChatPageWithTheme = () => (
  <ThemeProvider>
    <ChatPage />
  </ThemeProvider>
);

export default ChatPageWithTheme;