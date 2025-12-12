import React, { useState } from "react";
import { apiClient } from "@/api/apiClient";
import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Search,
  FileText,
  Calendar,
  Loader2,
  History as HistoryIcon,
  ExternalLink,
} from "lucide-react";
import { motion } from "framer-motion";

export default function History() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedResult, setSelectedResult] = useState(null);

  const { data: results = [], isLoading } = useQuery({
    queryKey: ["validationResults"],
    queryFn: () => apiClient.validationResults.list("-created_date"),
  });

  const filteredResults = results.filter(
    (r) =>
      r.document_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.model_name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusConfig = (status) => {
    switch (status) {
      case "approved":
        return {
          label: "Aprovado",
          color: "text-emerald-700",
          bg: "bg-emerald-100",
          icon: CheckCircle2,
        };
      case "rejected":
        return {
          label: "Reprovado",
          color: "text-red-700",
          bg: "bg-red-100",
          icon: XCircle,
        };
      default:
        return {
          label: "Ressalvas",
          color: "text-amber-700",
          bg: "bg-amber-100",
          icon: AlertTriangle,
        };
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 mb-1">
            Histórico de Validações
          </h1>
          <p className="text-slate-500">
            Consulte os resultados de validações anteriores
          </p>
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-72">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <Input
            placeholder="Buscar documento..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10 h-11 rounded-xl border-slate-200"
          />
        </div>
      </div>

      {/* Content */}
      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        </div>
      ) : filteredResults.length > 0 ? (
        <div className="grid gap-4">
          {filteredResults.map((result, index) => {
            const statusConfig = getStatusConfig(result.status);
            const StatusIcon = statusConfig.icon;

            return (
              <motion.div
                key={result.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <Card
                  className={`p-5 border-slate-200 hover:shadow-md transition-all cursor-pointer ${
                    selectedResult?.id === result.id ? "ring-2 ring-blue-500" : ""
                  }`}
                  onClick={() =>
                    setSelectedResult(
                      selectedResult?.id === result.id ? null : result
                    )
                  }
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-start gap-4 flex-1">
                      <div
                        className={`w-12 h-12 ${statusConfig.bg} rounded-xl flex items-center justify-center flex-shrink-0`}
                      >
                        <StatusIcon className={`w-6 h-6 ${statusConfig.color}`} />
                      </div>

                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-3 mb-1">
                          <h3 className="font-semibold text-slate-800 truncate">
                            {result.document_name}
                          </h3>
                          <Badge className={`${statusConfig.bg} ${statusConfig.color} border-0`}>
                            {statusConfig.label}
                          </Badge>
                        </div>

                        <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-slate-500">
                          <span className="flex items-center gap-1">
                            <FileText className="w-3.5 h-3.5" />
                            {result.model_name || "Validação Geral"}
                          </span>
                          <span className="flex items-center gap-1">
                            <Calendar className="w-3.5 h-3.5" />
                            {format(new Date(result.created_date), "dd MMM yyyy, HH:mm", {
                              locale: ptBR,
                            })}
                          </span>
                        </div>

                        {/* Stats */}
                        <div className="flex items-center gap-4 mt-3">
                          <span className="flex items-center gap-1 text-xs">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                            <span className="text-slate-600">
                              {result.correct_items?.length || 0} corretos
                            </span>
                          </span>
                          <span className="flex items-center gap-1 text-xs">
                            <XCircle className="w-3.5 h-3.5 text-red-500" />
                            <span className="text-slate-600">
                              {result.errors?.length || 0} erros
                            </span>
                          </span>
                          <span className="flex items-center gap-1 text-xs">
                            <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
                            <span className="text-slate-600">
                              {result.warnings?.length || 0} alertas
                            </span>
                          </span>
                        </div>

                        {/* Expanded Details */}
                        {selectedResult?.id === result.id && (
                          <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: "auto" }}
                            className="mt-4 pt-4 border-t border-slate-100"
                          >
                            <div className="grid sm:grid-cols-3 gap-4">
                              {/* Correct Items */}
                              <div className="bg-emerald-50/50 rounded-xl p-3">
                                <h5 className="text-xs font-semibold text-emerald-700 mb-2">
                                  Pontos Corretos
                                </h5>
                                <ul className="space-y-1">
                                  {result.correct_items?.slice(0, 3).map((item, i) => (
                                    <li key={i} className="text-xs text-slate-600 truncate">
                                      • {item}
                                    </li>
                                  ))}
                                  {(result.correct_items?.length || 0) > 3 && (
                                    <li className="text-xs text-slate-400">
                                      +{result.correct_items.length - 3} mais...
                                    </li>
                                  )}
                                </ul>
                              </div>

                              {/* Errors */}
                              <div className="bg-red-50/50 rounded-xl p-3">
                                <h5 className="text-xs font-semibold text-red-700 mb-2">
                                  Erros
                                </h5>
                                <ul className="space-y-1">
                                  {result.errors?.slice(0, 3).map((item, i) => (
                                    <li key={i} className="text-xs text-slate-600 truncate">
                                      • {item}
                                    </li>
                                  ))}
                                  {(result.errors?.length || 0) > 3 && (
                                    <li className="text-xs text-slate-400">
                                      +{result.errors.length - 3} mais...
                                    </li>
                                  )}
                                  {(!result.errors || result.errors.length === 0) && (
                                    <li className="text-xs text-slate-400">Nenhum erro</li>
                                  )}
                                </ul>
                              </div>

                              {/* Warnings */}
                              <div className="bg-amber-50/50 rounded-xl p-3">
                                <h5 className="text-xs font-semibold text-amber-700 mb-2">
                                  Inconsistências
                                </h5>
                                <ul className="space-y-1">
                                  {result.warnings?.slice(0, 3).map((item, i) => (
                                    <li key={i} className="text-xs text-slate-600 truncate">
                                      • {item}
                                    </li>
                                  ))}
                                  {(result.warnings?.length || 0) > 3 && (
                                    <li className="text-xs text-slate-400">
                                      +{result.warnings.length - 3} mais...
                                    </li>
                                  )}
                                  {(!result.warnings || result.warnings.length === 0) && (
                                    <li className="text-xs text-slate-400">Nenhuma</li>
                                  )}
                                </ul>
                              </div>
                            </div>

                            {result.document_url && (
                              <a
                                href={result.document_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                onClick={(e) => e.stopPropagation()}
                                className="inline-flex items-center gap-2 mt-4 text-sm text-blue-600 hover:text-blue-700"
                              >
                                <ExternalLink className="w-4 h-4" />
                                Ver documento original
                              </a>
                            )}
                          </motion.div>
                        )}
                      </div>
                    </div>
                  </div>
                </Card>
              </motion.div>
            );
          })}
        </div>
      ) : (
        <div className="text-center py-16">
          <div className="w-20 h-20 bg-slate-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <HistoryIcon className="w-10 h-10 text-slate-400" />
          </div>
          <h3 className="text-lg font-semibold text-slate-800 mb-2">
            {searchTerm ? "Nenhum resultado encontrado" : "Nenhuma validação ainda"}
          </h3>
          <p className="text-slate-500">
            {searchTerm
              ? "Tente buscar por outro termo"
              : "Valide seu primeiro documento para ver o histórico"}
          </p>
        </div>
      )}
    </div>
  );
}
