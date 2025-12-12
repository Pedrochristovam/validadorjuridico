import React, { useState } from "react";
import { apiClient } from "@/api/apiClient";
import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Loader2, Sparkles, FileCheck } from "lucide-react";
import { motion } from "framer-motion";
import DropZone from "@/components/upload/DropZone";
import ValidationResults from "@/components/validation/ValidationResults";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedModel] = useState("");
  const [isValidating, setIsValidating] = useState(false);
  const [validationResult, setValidationResult] = useState(null);

  const { data: models = [] } = useQuery({
    queryKey: ["models"],
    queryFn: () => apiClient.models.list(),
  });

  const handleValidate = async () => {
    if (!selectedFile) return;

    setIsValidating(true);

    try {
      // Upload do arquivo e extração de texto
      const uploadResult = await apiClient.documents.upload(selectedFile);

      // Encontrar modelo selecionado
      const model = models.find(m => m.id === selectedModel);

      // Validação com o backend usando o modelo selecionado
      const analysis = await apiClient.documents.validate({
        texto_extraido: uploadResult.texto_extraido,
        modelo_id: selectedModel || 'default',
      });

      // Salvar resultado
      const result = await apiClient.validationResults.create({
        document_name: selectedFile.name,
        model_id: selectedModel || null,
        model_name: model?.name || "Validação Geral",
        document_url: uploadResult.file_url,
        ...analysis
      });

      setValidationResult(result);
    } catch (error) {
      console.error("Erro na validação:", error);
    } finally {
      setIsValidating(false);
    }
  };

  const handleNewValidation = () => {
    setSelectedFile(null);
    setSelectedModel("");
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
    <div className="max-w-3xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-10"
      >
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 rounded-full text-blue-600 text-sm font-medium mb-4">
          <Sparkles className="w-4 h-4" />
          Validação Inteligente com IA
        </div>
        <h1 className="text-3xl lg:text-4xl font-bold text-slate-800 mb-3">
          Validador de Documentos
        </h1>
        <p className="text-slate-500 text-lg">
          Envie seu documento e receba uma análise completa em segundos
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-3xl border border-slate-200 shadow-xl shadow-slate-200/50 p-6 lg:p-8"
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
          <Button
            onClick={handleValidate}
            disabled={!selectedFile || isValidating}
            className="w-full h-14 rounded-xl bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-base font-semibold shadow-lg shadow-blue-500/25 transition-all hover:shadow-xl hover:shadow-blue-500/30"
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
        </div>
      </motion.div>

      {/* Info Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="grid sm:grid-cols-3 gap-4 mt-8"
      >
        {[
          { icon: "📄", title: "Upload Fácil", desc: "Arraste ou selecione" },
          { icon: "🤖", title: "IA Avançada", desc: "Análise inteligente" },
          { icon: "⚡", title: "Resultado Rápido", desc: "Em segundos" },
        ].map((item, index) => (
          <div
            key={index}
            className="bg-white/60 backdrop-blur-sm rounded-2xl border border-slate-200/50 p-5 text-center"
          >
            <div className="text-2xl mb-2">{item.icon}</div>
            <h4 className="font-semibold text-slate-800 text-sm mb-1">
              {item.title}
            </h4>
            <p className="text-xs text-slate-500">{item.desc}</p>
          </div>
        ))}
      </motion.div>
    </div>
  );
}
