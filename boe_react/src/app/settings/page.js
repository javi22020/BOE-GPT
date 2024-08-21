"use client";
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Montserrat } from 'next/font/google';
import { Save, RefreshCw, Plus, X } from 'lucide-react';

const montserrat = Montserrat({ subsets: ['latin'] });

const SettingsPage = () => {
  const router = useRouter();
  const [model, setModel] = useState('gpt-3.5-turbo');
  const [contextTokens, setContextTokens] = useState(2048);
  const [boeDates, setBoeDates] = useState([]);
  const [currentDate, setCurrentDate] = useState('');

  const handleSaveSettings = () => {
    // Aquí iría la lógica para guardar los ajustes
    console.log('Settings saved:', { model, contextTokens, boeDates });
    // Simular reinicio de la app
    router.push('/');
  };

  const handleAddDate = () => {
    if (currentDate && !boeDates.includes(currentDate)) {
      setBoeDates([...boeDates, currentDate]);
      setCurrentDate('');
    }
  };

  const handleRemoveDate = (dateToRemove) => {
    setBoeDates(boeDates.filter(date => date !== dateToRemove));
  };

  return (
    <div className={`min-h-screen bg-black flex flex-col items-center justify-center ${montserrat.className}`}>
      <h1 className="text-4xl font-bold text-white mb-8">Ajustes</h1>
      
      <div className="w-full max-w-md space-y-6 text-white">
        <div>
          <label htmlFor="model-select" className="block mb-2">Modelo de Lenguaje</label>
          <select
            id="model-select"
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className="w-full p-2 bg-gray-700 rounded"
          >
            <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
            <option value="gpt-4">GPT-4</option>
            <option value="claude-v1">Claude v1</option>
          </select>
        </div>

        <div>
          <label htmlFor="context-tokens" className="block mb-2">
            Tokens de Contexto: {contextTokens}
          </label>
          <input
            type="range"
            id="context-tokens"
            min="1024"
            max="8192"
            step="1024"
            value={contextTokens}
            onChange={(e) => setContextTokens(Number(e.target.value))}
            className="w-full"
          />
        </div>

        <div>
          <label htmlFor="boe-date" className="block mb-2">Fechas BOE a Descargar</label>
          <div className="flex">
            <input
              type="date"
              id="boe-date"
              value={currentDate}
              onChange={(e) => setCurrentDate(e.target.value)}
              className="flex-grow p-2 bg-gray-700 rounded-l"
            />
            <button
              onClick={handleAddDate}
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-r"
            >
              <Plus size={20} />
            </button>
          </div>
          <div className="mt-2 space-y-2">
            {boeDates.map((date, index) => (
              <div key={index} className="flex items-center bg-gray-700 rounded p-2">
                <span className="flex-grow">{date}</span>
                <button
                  onClick={() => handleRemoveDate(date)}
                  className="text-red-500 hover:text-red-700"
                >
                  <X size={20} />
                </button>
              </div>
            ))}
          </div>
        </div>

        <button
          onClick={handleSaveSettings}
          className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded flex items-center justify-center transition duration-300"
        >
          <Save className="mr-2" size={20} />
          Aplicar Ajustes y Reiniciar
        </button>
      </div>
    </div>
  );
};

export default SettingsPage;