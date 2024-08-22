"use client";
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Montserrat } from 'next/font/google';
import { Save, RefreshCw, Plus, X } from 'lucide-react';
import axios from 'axios';

const montserrat = Montserrat({ subsets: ['latin'] });

const SettingsPage = () => {
  const router = useRouter();
  const [availableModels, setAvailableModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [boeDates, setBoeDates] = useState([]);
  const [currentDate, setCurrentDate] = useState('');

  useEffect(() => {
    fetchAvailableModels();
  }, []);

  const fetchAvailableModels = async () => {
    try {
      const response = await axios.get('http://llm:4550/all_llms');
      setAvailableModels(response.data);
      if (response.data.length > 0) {
        setSelectedModel(response.data[0].name);
        setMaxContextTokens(response.data[0].config.n_ctx);
      }
    } catch (error) {
      console.error('Error fetching models:', error);
    }
  };

  const handleModelChange = (e) => {
    const modelName = e.target.value;
    setSelectedModel(modelName);
    const selectedModelConfig = availableModels.find(model => model.name === modelName);
    if (selectedModelConfig) {
      setMaxContextTokens(selectedModelConfig.config.n_ctx);
      setContextTokens(Math.min(contextTokens, selectedModelConfig.config.n_ctx));
    }
  };

  const handleSaveSettings = async () => {
    try {
      const modelIndex = availableModels.findIndex(model => model.name === selectedModel);
      if (modelIndex !== -1) {
        await axios.post(`http://llm:4550/set_llm/${modelIndex}`);
      }
      // Here you would also send the contextTokens and boeDates to your backend if needed
      console.log('Settings saved:', { selectedModel, contextTokens, boeDates });
      router.push('/');
    } catch (error) {
      console.error('Error saving settings:', error);
    }
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
            value={selectedModel}
            onChange={handleModelChange}
            className="w-full p-2 bg-gray-700 rounded"
          >
            {availableModels.map((model, index) => (
              <option key={index} value={model.name}>{model.name}</option>
            ))}
          </select>
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
          Aplicar Ajustes
        </button>
      </div>
    </div>
  );
};

export default SettingsPage;