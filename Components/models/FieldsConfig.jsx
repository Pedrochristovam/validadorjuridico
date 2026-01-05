import React from "react";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Plus, X, GripVertical } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const DEFAULT_FIELDS = [
  { id: "office_name", label: "Nome do Escritório" },
  { id: "cnpj", label: "CNPJ" },
  { id: "address", label: "Endereço" },
  { id: "legal_representative", label: "Responsável Legal" },
  { id: "date", label: "Data" },
  { id: "signature", label: "Assinatura" },
];

export default function FieldsConfig({ 
  selectedFields, 
  onFieldsChange,
  customFields,
  onCustomFieldsChange 
}) {
  const handleFieldToggle = (fieldId) => {
    if (selectedFields.includes(fieldId)) {
      onFieldsChange(selectedFields.filter(f => f !== fieldId));
    } else {
      onFieldsChange([...selectedFields, fieldId]);
    }
  };

  const addCustomField = () => {
    onCustomFieldsChange([
      ...customFields,
      { id: Date.now().toString(), name: "", required: false }
    ]);
  };

  const updateCustomField = (id, updates) => {
    onCustomFieldsChange(
      customFields.map(f => f.id === id ? { ...f, ...updates } : f)
    );
  };

  const removeCustomField = (id) => {
    onCustomFieldsChange(customFields.filter(f => f.id !== id));
  };

  return (
    <div className="space-y-6">
      {/* Default Fields */}
      <div>
        <h4 className="text-sm font-semibold text-slate-700 mb-4">
          Campos Padrão
        </h4>
        <div className="grid sm:grid-cols-2 gap-3">
          {DEFAULT_FIELDS.map((field) => (
            <div
              key={field.id}
              className={`flex items-center gap-3 p-4 rounded-xl border transition-all cursor-pointer ${
                selectedFields.includes(field.id)
                  ? "bg-blue-50 border-blue-200"
                  : "bg-white border-slate-200 hover:border-slate-300"
              }`}
              onClick={() => handleFieldToggle(field.id)}
            >
              <Checkbox
                checked={selectedFields.includes(field.id)}
                onCheckedChange={() => handleFieldToggle(field.id)}
                className="data-[state=checked]:bg-blue-600"
              />
              <span className="text-sm font-medium text-slate-700">
                {field.label}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Custom Fields */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-sm font-semibold text-slate-700">
            Campos Extras
          </h4>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={addCustomField}
            className="gap-2 rounded-lg"
          >
            <Plus className="w-4 h-4" />
            Adicionar Campo
          </Button>
        </div>

        <AnimatePresence>
          {customFields.length > 0 ? (
            <div className="space-y-3">
              {customFields.map((field) => (
                <motion.div
                  key={field.id}
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl border border-slate-200"
                >
                  <GripVertical className="w-4 h-4 text-slate-400" />
                  <Input
                    placeholder="Nome do campo"
                    value={field.name}
                    onChange={(e) => updateCustomField(field.id, { name: e.target.value })}
                    className="flex-1 h-10 rounded-lg border-slate-200"
                  />
                  <div className="flex items-center gap-2">
                    <Checkbox
                      checked={field.required}
                      onCheckedChange={(checked) => updateCustomField(field.id, { required: checked })}
                      className="data-[state=checked]:bg-blue-600"
                    />
                    <span className="text-xs text-slate-500">Obrigatório</span>
                  </div>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    onClick={() => removeCustomField(field.id)}
                    className="h-9 w-9 text-slate-400 hover:text-red-600 hover:bg-red-50"
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 bg-slate-50 rounded-xl border border-dashed border-slate-200">
              <p className="text-sm text-slate-500">
                Nenhum campo extra adicionado
              </p>
            </div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
