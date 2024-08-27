"use client";
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { ArrowLeft, Download, Check, Sun, Moon } from 'lucide-react';
import { ThemeProvider, useTheme } from '../contexts/theme';

const api_docs = axios.create({
  baseURL: 'http://localhost:6550',
  withCredentials: true,
});

const api_chain = axios.create({
  baseURL: 'http://localhost:3550',
})

const SettingsPageContent = () => {
  const { darkMode, toggleTheme } = useTheme();
  const [selectedDate, setSelectedDate] = useState('');
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const router = useRouter();

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      const response = await api_chain.get('/available_models');
      setModels(response.data);
      if (response.data.length > 0) {
        setSelectedModel(response.data[0]);
      }
    } catch (error) {
      console.error('Error fetching models:', error);
      setMessage('Error al cargar los modelos disponibles.');
    }
  };

  const handleDateChange = (e) => {
    const date = e.target.value;
    if (new Date(date) <= new Date()) {
      setSelectedDate(date);
    } else {
      setMessage('No se pueden seleccionar fechas futuras.');
    }
  };

  const handleModelChange = (e) => {
    setSelectedModel(e.target.value);
  };

  const handleDownload = async () => {
    if (!selectedDate) {
      setMessage('Por favor, selecciona una fecha.');
      return;
    }
    setIsLoading(true);
    try {
      const response = await api_docs.post('/send_to_chroma/' + selectedDate.replace('*-', ''));
      setMessage('BOE descargado correctamente.');
    } catch (error) {
      console.error('Error downloading BOE:', error);
      setMessage('Error al descargar el BOE.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    setIsLoading(true);
    try {
      await api_docs.post('/update_settings', { model: selectedModel });
      setMessage('Configuración guardada correctamente.');
    } catch (error) {
      console.error('Error saving settings:', error);
      setMessage('Error al guardar la configuración.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`flex flex-col h-screen ${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-900'}`}>
      <div className={`${darkMode ? 'bg-gray-800' : 'bg-blue-600'} text-white p-4 flex justify-between items-center`}>
        <div className="flex items-center">
          <button onClick={() => router.push('/')} className="mr-4">
            <ArrowLeft size={24} />
          </button>
          <h1 className="text-xl font-bold">Ajustes</h1>
        </div>
        <button onClick={toggleTheme} className="p-2 hover:bg-opacity-20 hover:bg-white rounded-full">
          {darkMode ? <Sun size={24} /> : <Moon size={24} />}
        </button>
      </div>
      
      <div className="flex-grow p-4 overflow-auto">
        <div className={`mb-6 p-4 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-white'} shadow-md`}>
          <h2 className="text-lg font-semibold mb-2">Descargar BOE</h2>
          <input
            type="date"
            value={selectedDate}
            onChange={handleDateChange}
            max={new Date().toISOString().split('T')[0]}
            className={`w-full p-2 mb-2 rounded ${
              darkMode ? 'bg-gray-700 text-white' : 'bg-gray-100 text-gray-900'
            } border ${darkMode ? 'border-gray-600' : 'border-gray-300'}`}
          />
          <button
            onClick={handleDownload}
            disabled={isLoading || !selectedDate}
            className={`w-full p-2 rounded ${
              darkMode
                ? 'bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700'
                : 'bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300'
            } text-white disabled:text-gray-400 transition-colors flex items-center justify-center`}
          >
            <Download size={18} className="mr-2" />
            Descargar BOE
          </button>
        </div>

        <div className={`mb-6 p-4 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-white'} shadow-md`}>
          <h2 className="text-lg font-semibold mb-2">Modelo de Lenguaje</h2>
          <select
            value={selectedModel}
            onChange={handleModelChange}
            className={`w-full p-2 mb-2 rounded ${
              darkMode ? 'bg-gray-700 text-white' : 'bg-gray-100 text-gray-900'
            } border ${darkMode ? 'border-gray-600' : 'border-gray-300'}`}
          >
            {models.map((model) => (
              <option key={model} value={model}>
                {model}
              </option>
            ))}
          </select>
          <button
            onClick={handleSave}
            disabled={isLoading}
            className={`w-full p-2 rounded ${
              darkMode
                ? 'bg-green-600 hover:bg-green-700 disabled:bg-gray-700'
                : 'bg-green-500 hover:bg-green-600 disabled:bg-gray-300'
            } text-white disabled:text-gray-400 transition-colors flex items-center justify-center`}
          >
            <Check size={18} className="mr-2" />
            Guardar Configuración
          </button>
        </div>

        {message && (
          <div className={`p-2 rounded ${
            message.includes('Error')
              ? 'bg-red-100 text-red-700'
              : 'bg-green-100 text-green-700'
          }`}>
            {message}
          </div>
        )}
      </div>
    </div>
  );
};

const SettingsPage = () => (
  <ThemeProvider>
    <SettingsPageContent />
  </ThemeProvider>
);

export default SettingsPage;