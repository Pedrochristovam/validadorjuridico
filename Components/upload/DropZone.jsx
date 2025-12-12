import React, { useState, useCallback } from "react";
import { Upload, File, X, FileText } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function DropZone({ onFileSelect, selectedFile, onClear }) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDragIn = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragOut = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.type === "application/pdf" || 
          file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
        onFileSelect(file);
      }
    }
  }, [onFileSelect]);

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    if (file) {
      onFileSelect(file);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  return (
    <div className="w-full">
      <AnimatePresence mode="wait">
        {!selectedFile ? (
          <motion.div
            key="dropzone"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            onDragEnter={handleDragIn}
            onDragLeave={handleDragOut}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`relative border-2 border-dashed rounded-2xl p-10 transition-all duration-300 cursor-pointer group ${
              isDragging
                ? "border-blue-500 bg-blue-50/50"
                : "border-slate-200 hover:border-blue-400 hover:bg-slate-50/50"
            }`}
          >
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileInput}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            
            <div className="flex flex-col items-center text-center">
              <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-5 transition-all duration-300 ${
                isDragging 
                  ? "bg-blue-100 scale-110" 
                  : "bg-slate-100 group-hover:bg-blue-100 group-hover:scale-105"
              }`}>
                <Upload className={`w-7 h-7 transition-colors ${
                  isDragging ? "text-blue-600" : "text-slate-400 group-hover:text-blue-600"
                }`} />
              </div>
              
              <h3 className="text-lg font-semibold text-slate-800 mb-2">
                Arraste seu documento aqui
              </h3>
              <p className="text-slate-500 text-sm mb-4">
                ou clique para selecionar
              </p>
              <div className="flex items-center gap-2">
                <span className="px-3 py-1 bg-slate-100 rounded-lg text-xs font-medium text-slate-600">
                  PDF
                </span>
                <span className="px-3 py-1 bg-slate-100 rounded-lg text-xs font-medium text-slate-600">
                  DOCX
                </span>
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="file-preview"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="bg-gradient-to-br from-blue-50 to-slate-50 border border-blue-100 rounded-2xl p-6"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 bg-white rounded-xl border border-slate-200 flex items-center justify-center shadow-sm">
                  <FileText className="w-7 h-7 text-blue-600" />
                </div>
                <div>
                  <p className="font-semibold text-slate-800 mb-1">{selectedFile.name}</p>
                  <p className="text-sm text-slate-500">{formatFileSize(selectedFile.size)}</p>
                </div>
              </div>
              <button
                onClick={onClear}
                className="w-10 h-10 rounded-xl bg-white border border-slate-200 flex items-center justify-center hover:bg-red-50 hover:border-red-200 hover:text-red-600 transition-all"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
