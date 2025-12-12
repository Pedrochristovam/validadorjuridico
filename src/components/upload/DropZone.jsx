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
            className={`relative border-2 border-dashed rounded-3xl p-12 transition-all duration-500 cursor-pointer group backdrop-blur-sm ${
              isDragging
                ? "border-blue-500 bg-gradient-to-br from-blue-50/80 to-indigo-50/80 shadow-xl shadow-blue-500/20 scale-[1.02]"
                : "border-slate-300/60 hover:border-blue-400/60 hover:bg-gradient-to-br hover:from-slate-50/50 hover:to-blue-50/30 hover:shadow-lg"
            }`}
          >
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileInput}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            
            <div className="flex flex-col items-center text-center">
              <div className={`w-20 h-20 rounded-3xl flex items-center justify-center mb-6 transition-all duration-500 ${
                isDragging 
                  ? "bg-gradient-to-br from-blue-500 to-indigo-500 scale-110 shadow-xl shadow-blue-500/30" 
                  : "bg-gradient-to-br from-slate-100 to-slate-200 group-hover:from-blue-100 group-hover:to-indigo-100 group-hover:scale-105 group-hover:shadow-lg"
              }`}>
                <Upload className={`w-8 h-8 transition-all duration-300 ${
                  isDragging ? "text-white scale-110" : "text-slate-500 group-hover:text-blue-600 group-hover:scale-110"
                }`} />
              </div>
              
              <h3 className="text-xl font-bold text-slate-900 mb-2.5">
                Arraste seu documento aqui
              </h3>
              <p className="text-slate-500 text-sm mb-5 font-medium">
                ou clique para selecionar
              </p>
              <div className="flex items-center gap-2.5">
                <span className="px-4 py-1.5 bg-white/80 backdrop-blur-sm rounded-xl text-xs font-semibold text-slate-700 border border-slate-200/60 shadow-sm">
                  PDF
                </span>
                <span className="px-4 py-1.5 bg-white/80 backdrop-blur-sm rounded-xl text-xs font-semibold text-slate-700 border border-slate-200/60 shadow-sm">
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
            className="bg-gradient-to-br from-blue-50/90 via-indigo-50/80 to-slate-50/90 backdrop-blur-xl border border-blue-200/60 rounded-3xl p-6 shadow-xl"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/25">
                  <FileText className="w-7 h-7 text-white" />
                </div>
                <div>
                  <p className="font-semibold text-slate-800 mb-1">{selectedFile.name}</p>
                  <p className="text-sm text-slate-500">{formatFileSize(selectedFile.size)}</p>
                </div>
              </div>
              <button
                onClick={onClear}
                className="w-10 h-10 rounded-xl bg-white/90 backdrop-blur-sm border border-slate-200/60 flex items-center justify-center hover:bg-red-50 hover:border-red-300 hover:text-red-600 transition-all duration-300 hover:scale-110 shadow-sm hover:shadow-md"
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

