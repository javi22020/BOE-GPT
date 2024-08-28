import React, { useState, useRef } from 'react';
import PropTypes from 'prop-types';
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { ScrollArea } from "@/components/ui/scroll-area"

const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [logs, setLogs] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef(null);

  const addLog = (message) => {
    setLogs(prevLogs => [...prevLogs, message]);
  };

  const handleFileChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
      addLog(`File selected: ${event.target.files[0].name}`);
    }
  };

  const uploadFile = async () => {
    if (!file) {
      addLog('No file selected');
      return;
    }

    setIsUploading(true);
    addLog('Starting upload...');

    const chunkSize = 1024 * 1024; // 1MB chunks
    const chunks = Math.ceil(file.size / chunkSize);
    const fileReader = new FileReader();

    for (let chunk = 0; chunk < chunks; chunk++) {
      const start = chunk * chunkSize;
      const end = Math.min(start + chunkSize, file.size);
      const blob = file.slice(start, end);

      const arrayBuffer = await new Promise((resolve) => {
        fileReader.onload = (e) => resolve(e.target.result);
        fileReader.readAsArrayBuffer(blob);
      });

      try {
        const response = await fetch('http://127.0.0.1:4550/receive', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/octet-stream',
            'X-File-Name': file.name,
            'X-Chunk-Number': chunk.toString(),
            'X-Total-Chunks': chunks.toString(),
          },
          body: arrayBuffer,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const newProgress = Math.round(((chunk + 1) / chunks) * 100);
        setProgress(newProgress);
        addLog(`Uploaded chunk ${chunk + 1} of ${chunks} (${newProgress}%)`);
      } catch (error) {
        addLog(`Error uploading chunk ${chunk + 1}: ${error}`);
        setIsUploading(false);
        return;
      }
    }

    addLog('Upload completed successfully!');
    setIsUploading(false);
  };

  return (
    <div className="w-full max-w-md mx-auto p-4 space-y-4">
      <input
        type="file"
        onChange={handleFileChange}
        ref={fileInputRef}
        className="hidden"
      />
      <Button 
        onClick={() => fileInputRef.current?.click()}
        disabled={isUploading}
      >
        Select File
      </Button>
      {file && (
        <p className="text-sm text-muted-foreground">
          Selected file: {file.name}
        </p>
      )}
      <Button 
        onClick={uploadFile} 
        disabled={!file || isUploading}
      >
        Upload File
      </Button>
      {isUploading && (
        <Progress value={progress} className="w-full" />
      )}
      <ScrollArea className="h-[200px] w-full border rounded-md p-4">
        {logs.map((log, index) => (
          <p key={index} className="text-sm">
            {log}
          </p>
        ))}
      </ScrollArea>
    </div>
  );
};

FileUploader.propTypes = {
  // Add any props here if needed
};

export default FileUploader;