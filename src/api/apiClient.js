// Cliente API para conectar com o backend FastAPI
// Usa variável de ambiente em produção, fallback para localhost em desenvolvimento
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = {
  models: {
    list: async (orderBy = "-created_date") => {
      try {
        const response = await fetch(`${API_BASE_URL}/modelos`, {
          method: 'GET',
        });
        
        if (!response.ok) {
          throw new Error(`Erro ao listar modelos: ${response.statusText}`);
        }
        
        const result = await response.json();
        return result.modelos || [];
      } catch (error) {
        console.error("Erro ao listar modelos:", error);
        return [];
      }
    },
    create: async (data) => {
      try {
        const formData = new FormData();
        formData.append('nome', data.name);
        
        if (data.file) {
          formData.append('file', data.file);
        }
        
        const response = await fetch(`${API_BASE_URL}/uploadModelo`, {
          method: 'POST',
          body: formData,
        });
        
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({ detail: response.statusText }));
          throw new Error(errorData.detail || `Erro ao criar modelo: ${response.statusText}`);
        }
        
        const result = await response.json();
        return {
          id: result.modelo_id || Date.now().toString(),
          name: result.nome || data.name,
          ...result,
          created_date: new Date().toISOString(),
        };
      } catch (error) {
        console.error("Erro ao criar modelo:", error);
        throw error;
      }
    },
    delete: async (id) => {
      try {
        const response = await fetch(`${API_BASE_URL}/modelos/${id}`, {
          method: 'DELETE',
        });
        
        if (!response.ok) {
          throw new Error(`Erro ao excluir modelo: ${response.statusText}`);
        }
        
        return { success: true };
      } catch (error) {
        console.error("Erro ao excluir modelo:", error);
        throw error;
      }
    },
  },
  documents: {
    upload: async (file) => {
      try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${API_BASE_URL}/uploadDocumento`, {
          method: 'POST',
          body: formData,
        });
        
        if (!response.ok) {
          throw new Error(`Erro no upload: ${response.statusText}`);
        }
        
        const result = await response.json();
        
        return {
          file_url: result.filename,
          texto_extraido: result.texto_extraido,
          filename: result.filename,
        };
      } catch (error) {
        console.error("Erro no upload:", error);
        throw error;
      }
    },
    validate: async ({ texto_extraido, modelo_id }) => {
      try {
        const response = await fetch(`${API_BASE_URL}/validar`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            texto_documento: texto_extraido || '',
            modelo_id: modelo_id || 'default',
            use_ai: true,
          }),
        });
        
        if (!response.ok) {
          throw new Error(`Erro na validação: ${response.statusText}`);
        }
        
        const result = await response.json();
        
        return {
          correct_items: result.corretos || [],
          errors: result.faltando || [],
          warnings: result.duvidosos || [],
          status: result.status_geral === 'APROVADO' ? 'approved' : 
                 result.status_geral === 'REPROVADO' ? 'rejected' : 'warning',
          evidencias: result.evidencias || {},
          corretos: result.corretos || [],
          faltando: result.faltando || [],
          duvidosos: result.duvidosos || [],
        };
      } catch (error) {
        console.error("Erro na validação:", error);
        throw error;
      }
    },
  },
  validationResults: {
    list: async (orderBy = "-created_date") => {
      // Implementar histórico se necessário
      return [];
    },
    create: async (data) => {
      return {
        id: Date.now().toString(),
        ...data,
        created_date: new Date().toISOString(),
      };
    },
  },
};

export { apiClient };
