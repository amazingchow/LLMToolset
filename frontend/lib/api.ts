const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:15050';

export interface ModelInfo {
  model_name: string;
  config: {
    [key: string]: string | number | boolean | undefined;
  };
  extracted_params: {
    model_size: number;
    precision: string;
    hidden_size: number;
    num_hidden_layers: number;
    num_attention_heads: number;
    num_key_value_heads: number;
  };
}

export interface ConfigOptions {
  data_types: string[];
  optimizers: string[];
  available_models: string[];
}

export interface MemoryCalculationRequest {
  model_name: string;
  precision: string;
  batch_size: number;
  sequence_length: number;
  kv_cache_precision?: string;
  optimizer?: string;
  trainable_parameters?: number;
  use_flash_attention?: boolean;
  use_page_attention?: boolean;
}

export interface MemoryResult {
  model_weights_memory: string;
  kv_cache_memory?: string;
  activation_memory: string;
  inference_memory?: string;
  optimizer_memory?: string;
  gradients_memory?: string;
  training_memory?: string;
  overhead_memory: string;
}

export interface CalculationResponse {
  calculation_type: 'inference' | 'training';
  parameters: Record<string, string | number | boolean | undefined>;
  memory_requirements: MemoryResult;
}

export async function fetchModels(): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/api/models`);
  if (!response.ok) {
    throw new Error('Failed to fetch models');
  }
  const data = await response.json();
  return data.models;
}

export async function fetchModelInfo(modelName: string): Promise<ModelInfo> {
  const response = await fetch(`${API_BASE_URL}/api/models/${encodeURIComponent(modelName)}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch model info for ${modelName}`);
  }
  return response.json();
}

export async function fetchConfigOptions(): Promise<ConfigOptions> {
  const response = await fetch(`${API_BASE_URL}/api/config/options`);
  if (!response.ok) {
    throw new Error('Failed to fetch config options');
  }
  return response.json();
}

export async function calculateInferenceMemory(request: MemoryCalculationRequest): Promise<CalculationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/memory/inference`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to calculate inference memory');
  }

  return response.json();
}

export async function calculateTrainingMemory(request: MemoryCalculationRequest): Promise<CalculationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/memory/training`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to calculate training memory');
  }

  return response.json();
}
