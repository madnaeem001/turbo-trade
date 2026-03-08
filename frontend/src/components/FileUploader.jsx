import React, { useState } from 'react';

function FileUploader({ onFileSelect }) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.name.endsWith('.csv')) {
        setSelectedFile(file);
        onFileSelect(file);
      }
    }
  };

  const handleFileInput = (e) => {
    const file = e.target.files?.[0];
    if (file && file.name.endsWith('.csv')) {
      setSelectedFile(file);
      onFileSelect(file);
    }
  };

  return (
    <div
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      className={`border-2 border-dashed rounded-xl p-12 text-center transition-all ${
        dragActive
          ? 'border-cyan-400 bg-cyan-500/10'
          : 'border-slate-600 bg-slate-800/50 hover:border-slate-500'
      }`}
    >
      <input
        type="file"
        accept=".csv"
        onChange={handleFileInput}
        id="file-input"
        className="hidden"
      />
      <label htmlFor="file-input" className="cursor-pointer">
        <div className="text-5xl mb-4 text-cyan-400">
          <i className="fas fa-cloud-arrow-up"></i>
        </div>
        <h3 className="text-2xl font-bold text-white mb-2">
          Upload CSV Data File
        </h3>
        <p className="text-slate-400 mb-4">
          Drag and drop or click to select historical OHLCV data
        </p>
        <div className="bg-cyan-600 hover:bg-cyan-700 text-white font-bold py-3 px-8 rounded-lg inline-block transition-colors">
          Select File
        </div>
      </label>
      {selectedFile && (
        <div className="mt-4 text-green-400 font-semibold">
          <i className="fas fa-check-circle mr-2"></i>
          {selectedFile.name} ready to upload
        </div>
      )}
    </div>
  );
}

export default FileUploader;
