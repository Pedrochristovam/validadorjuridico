import React from "react";
import { CheckCircle2, XCircle, AlertTriangle, Download, FileText, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

export default function ValidationResults({ result, onNewValidation }) {
  const getStatusConfig = () => {
    switch (result.status) {
      case "approved":
        return {
          label: "Aprovado",
          color: "text-emerald-600",
          bg: "bg-emerald-50",
          border: "border-emerald-200",
          icon: CheckCircle2,
        };
      case "rejected":
        return {
          label: "Reprovado",
          color: "text-red-600",
          bg: "bg-red-50",
          border: "border-red-200",
          icon: XCircle,
        };
      default:
        return {
          label: "Com Ressalvas",
          color: "text-amber-600",
          bg: "bg-amber-50",
          border: "border-amber-200",
          icon: AlertTriangle,
        };
    }
  };

  const statusConfig = getStatusConfig();
  const StatusIcon = statusConfig.icon;

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: { opacity: 1, x: 0 }
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="space-y-6"
    >
      {/* Status Header */}
      <motion.div
        variants={itemVariants}
        className={`${statusConfig.bg} ${statusConfig.border} border rounded-2xl p-6`}
      >
        <div className="flex items-center gap-4">
          <div className={`w-14 h-14 rounded-xl ${statusConfig.bg} flex items-center justify-center`}>
            <StatusIcon className={`w-8 h-8 ${statusConfig.color}`} />
          </div>
          <div>
            <h3 className={`text-xl font-bold ${statusConfig.color}`}>
              {statusConfig.label}
            </h3>
            <p className="text-slate-600 text-sm mt-1">
              {result.document_name}
            </p>
          </div>
        </div>
      </motion.div>

      {/* Results Grid */}
      <div className="grid lg:grid-cols-3 gap-4">
        {/* Correct Items */}
        <motion.div
          variants={itemVariants}
          className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm"
        >
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-emerald-100 rounded-xl flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            </div>
            <div>
              <h4 className="font-semibold text-slate-800">Corretos</h4>
              <p className="text-xs text-slate-500">{result.correct_items?.length || 0} itens</p>
            </div>
          </div>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {result.correct_items?.map((item, index) => (
              <div
                key={index}
                className="flex items-start gap-2 p-3 bg-emerald-50/50 rounded-xl"
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                <span className="text-sm text-slate-700">{item}</span>
              </div>
            ))}
            {(!result.correct_items || result.correct_items.length === 0) && (
              <p className="text-sm text-slate-400 text-center py-4">Nenhum item</p>
            )}
          </div>
        </motion.div>

        {/* Errors */}
        <motion.div
          variants={itemVariants}
          className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm"
        >
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center">
              <XCircle className="w-5 h-5 text-red-600" />
            </div>
            <div>
              <h4 className="font-semibold text-slate-800">Erros</h4>
              <p className="text-xs text-slate-500">{result.errors?.length || 0} itens</p>
            </div>
          </div>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {result.errors?.map((item, index) => (
              <div
                key={index}
                className="flex items-start gap-2 p-3 bg-red-50/50 rounded-xl"
              >
                <XCircle className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                <span className="text-sm text-slate-700">{item}</span>
              </div>
            ))}
            {(!result.errors || result.errors.length === 0) && (
              <p className="text-sm text-slate-400 text-center py-4">Nenhum erro</p>
            )}
          </div>
        </motion.div>

        {/* Warnings */}
        <motion.div
          variants={itemVariants}
          className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm"
        >
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-amber-100 rounded-xl flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-amber-600" />
            </div>
            <div>
              <h4 className="font-semibold text-slate-800">Inconsistências</h4>
              <p className="text-xs text-slate-500">{result.warnings?.length || 0} itens</p>
            </div>
          </div>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {result.warnings?.map((item, index) => (
              <div
                key={index}
                className="flex items-start gap-2 p-3 bg-amber-50/50 rounded-xl"
              >
                <AlertTriangle className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" />
                <span className="text-sm text-slate-700">{item}</span>
              </div>
            ))}
            {(!result.warnings || result.warnings.length === 0) && (
              <p className="text-sm text-slate-400 text-center py-4">Nenhuma inconsistência</p>
            )}
          </div>
        </motion.div>
      </div>

      {/* Actions */}
      <motion.div
        variants={itemVariants}
        className="flex flex-wrap gap-3 pt-4"
      >
        <Button
          variant="outline"
          className="gap-2 rounded-xl h-12 px-5"
        >
          <Download className="w-4 h-4" />
          Baixar Relatório PDF
        </Button>
        <Button
          onClick={onNewValidation}
          className="gap-2 rounded-xl h-12 px-5 bg-blue-600 hover:bg-blue-700"
        >
          <RotateCcw className="w-4 h-4" />
          Validar Novo Documento
        </Button>
      </motion.div>
    </motion.div>
  );
}


