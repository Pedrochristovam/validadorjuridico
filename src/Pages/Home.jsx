import React, { useState } from "react";
import { apiClient } from "@/api/apiClient";
import { Button } from "@/components/ui/button.jsx";
import { Loader2, Sparkles, FileCheck } from "lucide-react";
import { motion } from "framer-motion";
import DropZone from "@/components/upload/DropZone";
import ValidationResults from "@/components/validation/ValidationResults";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isValidating, setIsValidating] = useState(false);
  const [validationResult, setValidationResult] = useState(null);

  const handleValidate = async () => {
    if (!selectedFile) return;

    setIsValidating(true);

    try {
      // Upload do arquivo e extração de texto
      const uploadResult = await apiClient.documents.upload(selectedFile);

      // Validação com o backend usando o modelo padrão interno
      const analysis = await apiClient.documents.validate({
        texto_extraido: uploadResult.texto_extraido,
        modelo_id: "default",
      });

      // Salvar resultado
      const result = await apiClient.validationResults.create({
        document_name: selectedFile.name,
        model_id: "default",
        model_name: analysis.modelo_usado || "Modelo Interno",
        document_url: uploadResult.file_url,
        ...analysis
      });

      setValidationResult(result);
    } catch (error) {
      console.error("Erro na validação:", error);
      alert(`Erro ao validar documento: ${error.message}`);
    } finally {
      setIsValidating(false);
    }
  };

  const handleNewValidation = () => {
    setSelectedFile(null);
    setValidationResult(null);
  };

  if (validationResult) {
    return (
      <div className="max-w-5xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-slate-800 mb-2">
              Resultado da Validação
            </h1>
            <p className="text-slate-500">
              Análise completa do documento enviado
            </p>
          </div>

          <ValidationResults 
            result={validationResult}
            onNewValidation={handleNewValidation}
          />
        </motion.div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-12"
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1, duration: 0.4 }}
          className="inline-flex items-center gap-2.5 px-5 py-2.5 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-full text-blue-700 text-sm font-semibold mb-6 shadow-sm border border-blue-100/50"
        >
          <Sparkles className="w-4 h-4 animate-pulse" />
          Validação Inteligente com IA
        </motion.div>
        <motion.h1
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="text-4xl lg:text-5xl font-bold text-slate-900 mb-4 tracking-tight"
        >
          Validador de Documentos
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="text-slate-600 text-lg lg:text-xl max-w-2xl mx-auto"
        >
          Envie seu documento e receba uma análise completa em segundos
        </motion.p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.5 }}
        className="bg-white/80 backdrop-blur-xl rounded-3xl border border-slate-200/60 shadow-2xl shadow-slate-200/20 p-8 lg:p-10 hover:shadow-3xl hover:shadow-slate-200/30 transition-all duration-500"
      >
        <div className="space-y-6">
          {/* File Upload */}
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-3">
              Documento para Validação
            </label>
            <DropZone
              onFileSelect={setSelectedFile}
              selectedFile={selectedFile}
              onClear={() => setSelectedFile(null)}
            />
          </div>

          {/* Submit Button */}
          <motion.div
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            transition={{ type: "spring", stiffness: 400, damping: 17 }}
          >
            <Button
              onClick={handleValidate}
              disabled={!selectedFile || isValidating}
              className="w-full h-14 rounded-xl bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-600 hover:from-blue-700 hover:via-blue-600 hover:to-indigo-700 text-base font-semibold shadow-xl shadow-blue-500/30 transition-all duration-300 hover:shadow-2xl hover:shadow-blue-500/40 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              {isValidating ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Analisando documento...
                </>
              ) : (
                <>
                  <FileCheck className="w-5 h-5 mr-2" />
                  Validar Documento
                </>
              )}
            </Button>
          </motion.div>
        </div>
      </motion.div>

      {/* Info Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.5 }}
        className="grid sm:grid-cols-3 gap-5 mt-10"
      >
        {[
          { icon: "📄", title: "Upload Fácil", desc: "Arraste ou selecione" },
          { icon: "🤖", title: "IA Avançada", desc: "Análise inteligente" },
          { icon: "⚡", title: "Resultado Rápido", desc: "Em segundos" },
        ].map((item, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 + index * 0.1, duration: 0.4 }}
            whileHover={{ y: -5, scale: 1.02 }}
            className="bg-white/70 backdrop-blur-xl rounded-2xl border border-slate-200/60 p-6 text-center shadow-lg hover:shadow-xl transition-all duration-300 group cursor-pointer"
          >
            <div className="text-3xl mb-3 transform group-hover:scale-110 transition-transform duration-300">{item.icon}</div>
            <h4 className="font-semibold text-slate-800 text-sm mb-1.5">
              {item.title}
            </h4>
            <p className="text-xs text-slate-500">{item.desc}</p>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}
