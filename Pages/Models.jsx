import React, { useState } from "react";
import { apiClient } from "@/api/apiClient";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { 
  Plus, 
  FileText, 
  Trash2, 
  Loader2,
  FolderCog,
  CheckCircle,
  X
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import DropZone from "@/components/upload/DropZone";

export default function Models() {
  const [showForm, setShowForm] = useState(false);
  const [modelFile, setModelFile] = useState(null);
  const [isSaving, setIsSaving] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const queryClient = useQueryClient();

  const { data: models = [], isLoading } = useQuery({
    queryKey: ["models"],
    queryFn: () => apiClient.models.list("-created_date"),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => apiClient.models.delete(id),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["models"] });
      await queryClient.refetchQueries({ queryKey: ["models"] });
    },
  });

  const handleSaveModel = async () => {
    if (!modelFile) {
      alert("Por favor, selecione um arquivo modelo");
      return;
    }

    setIsSaving(true);

    try {
      // Usa o nome do arquivo como nome do modelo (sem extensão)
      const fileName = modelFile.name;
      const modelName = fileName.replace(/\.[^/.]+$/, ""); // Remove extensão

      await apiClient.models.create({
        name: modelName,
        file: modelFile,
      });

      // Invalida e recarrega a lista de modelos
      await queryClient.invalidateQueries({ queryKey: ["models"] });
      await queryClient.refetchQueries({ queryKey: ["models"] });
      
      // Reset form
      setModelFile(null);
      setShowForm(false);
      
      // Show success
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      console.error("Erro ao salvar modelo:", error);
      alert(`Erro ao salvar modelo: ${error.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Success Toast */}
      <AnimatePresence>
        {showSuccess && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="fixed top-4 right-4 z-50 bg-gradient-to-r from-emerald-500 to-green-500 text-white px-6 py-3.5 rounded-xl shadow-2xl shadow-emerald-500/30 flex items-center gap-2.5 backdrop-blur-sm border border-emerald-400/20"
          >
            <CheckCircle className="w-5 h-5" />
            Modelo salvo com sucesso!
          </motion.div>
        )}
      </AnimatePresence>

      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="flex items-center justify-between mb-10"
      >
        <div>
          <h1 className="text-3xl font-bold text-slate-900 mb-2 tracking-tight">
            Modelos de Documento
          </h1>
          <p className="text-slate-600 font-medium">
            Faça upload do documento modelo. O sistema lerá automaticamente.
          </p>
        </div>
        
        {!showForm && (
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Button
              onClick={() => setShowForm(true)}
              className="gap-2 rounded-xl h-11 px-5 shadow-lg"
            >
              <Plus className="w-4 h-4" />
              Novo Modelo
            </Button>
          </motion.div>
        )}
      </motion.div>

      {/* Form */}
      <AnimatePresence>
        {showForm && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="mb-8"
          >
            <Card className="p-8 lg:p-10 shadow-2xl">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-bold text-slate-800">
                  Cadastrar Novo Modelo
                </h2>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => {
                    setShowForm(false);
                    setModelFile(null);
                  }}
                  className="rounded-xl"
                >
                  <X className="w-5 h-5" />
                </Button>
              </div>

              <div className="space-y-6">
                {/* File Upload */}
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">
                    Arquivo do Modelo
                    <span className="text-slate-400 font-normal ml-2">(PDF ou DOCX)</span>
                  </label>
                  <p className="text-sm text-slate-500 mb-4">
                    Faça upload do documento modelo. O sistema extrairá o texto automaticamente usando OCR.
                  </p>
                  <DropZone
                    onFileSelect={setModelFile}
                    selectedFile={modelFile}
                    onClear={() => setModelFile(null)}
                  />
                </div>

                {/* Save Button */}
                <div className="flex gap-3 pt-4">
                  <Button
                    variant="outline"
                    onClick={() => {
                      setShowForm(false);
                      setModelFile(null);
                    }}
                    className="rounded-xl h-12 px-6"
                  >
                    Cancelar
                  </Button>
                  <Button
                    onClick={handleSaveModel}
                    disabled={!modelFile || isSaving}
                    className="rounded-xl h-12 px-6 bg-blue-600 hover:bg-blue-700 flex-1"
                  >
                    {isSaving ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Salvando...
                      </>
                    ) : (
                      <>
                        <CheckCircle className="w-4 h-4 mr-2" />
                        Salvar Modelo
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Models List */}
      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        </div>
      ) : models.length > 0 ? (
        <div className="grid gap-4">
          {models.map((model) => (
            <motion.div
              key={model.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <Card className="p-6 hover:shadow-xl transition-all duration-300 hover:scale-[1.01] cursor-pointer group">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                      <FileText className="w-6 h-6 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-slate-800">
                        {model.name}
                      </h3>
                      <p className="text-sm text-slate-500">
                        {model.arquivo_original || "Modelo cadastrado"}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => deleteMutation.mutate(model.id)}
                      className="rounded-lg hover:bg-red-50 hover:text-red-600"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <div className="w-20 h-20 bg-slate-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <FolderCog className="w-10 h-10 text-slate-400" />
          </div>
          <h3 className="text-lg font-semibold text-slate-800 mb-2">
            Nenhum modelo cadastrado
          </h3>
          <p className="text-slate-500 mb-6">
            Faça upload do seu primeiro modelo para começar
          </p>
          <Button
            onClick={() => setShowForm(true)}
            className="gap-2 rounded-xl h-11 px-5 bg-blue-600 hover:bg-blue-700"
          >
            <Plus className="w-4 h-4" />
            Criar Primeiro Modelo
          </Button>
        </div>
      )}
    </div>
  );
}
