export interface GPUInfo {
  id: string;
  name: string;
  memory: number; // in GB
  category: 'Nvidia GPU' | 'Apple Silicon';
}

export const GPU_DATA: Record<string, GPUInfo> = {
  // NVIDIA GPUs
  '3060_12': {
    id: '3060_12',
    name: 'RTX 3060 (12GB)',
    memory: 12,
    category: 'Nvidia GPU',
  },
  '3060ti_8': {
    id: '3060ti_8',
    name: 'RTX 3060 Ti (8GB)',
    memory: 8,
    category: 'Nvidia GPU',
  },
  '3070_8': {
    id: '3070_8',
    name: 'RTX 3070 (8GB)',
    memory: 8,
    category: 'Nvidia GPU',
  },
  '3070ti_8': {
    id: '3070ti_8',
    name: 'RTX 3070 Ti (8GB)',
    memory: 8,
    category: 'Nvidia GPU',
  },
  '3080_10': {
    id: '3080_10',
    name: 'RTX 3080 (10GB)',
    memory: 10,
    category: 'Nvidia GPU',
  },
  '3080_12': {
    id: '3080_12',
    name: 'RTX 3080 (12GB)',
    memory: 12,
    category: 'Nvidia GPU',
  },
  '3080ti_12': {
    id: '3080ti_12',
    name: 'RTX 3080 Ti (12GB)',
    memory: 12,
    category: 'Nvidia GPU',
  },
  '3090_24': {
    id: '3090_24',
    name: 'RTX 3090 (24GB)',
    memory: 24,
    category: 'Nvidia GPU',
  },
  '3090ti_24': {
    id: '3090ti_24',
    name: 'RTX 3090 Ti (24GB)',
    memory: 24,
    category: 'Nvidia GPU',
  },
  '4060_8': {
    id: '4060_8',
    name: 'RTX 4060 (8GB)',
    memory: 8,
    category: 'Nvidia GPU',
  },
  '4060ti_8': {
    id: '4060ti_8',
    name: 'RTX 4060 Ti (8GB)',
    memory: 8,
    category: 'Nvidia GPU',
  },
  '4060ti_16': {
    id: '4060ti_16',
    name: 'RTX 4060 Ti (16GB)',
    memory: 16,
    category: 'Nvidia GPU',
  },
  '4070_12': {
    id: '4070_12',
    name: 'RTX 4070 (12GB)',
    memory: 12,
    category: 'Nvidia GPU',
  },
  '4070ti_12': {
    id: '4070ti_12',
    name: 'RTX 4070 Ti (12GB)',
    memory: 12,
    category: 'Nvidia GPU',
  },
  '4070tisuper_16': {
    id: '4070tisuper_16',
    name: 'RTX 4070 Ti SUPER (16GB)',
    memory: 16,
    category: 'Nvidia GPU',
  },
  '4070super_12': {
    id: '4070super_12',
    name: 'RTX 4070 SUPER (12GB)',
    memory: 12,
    category: 'Nvidia GPU',
  },
  '4080_16': {
    id: '4080_16',
    name: 'RTX 4080 (16GB)',
    memory: 16,
    category: 'Nvidia GPU',
  },
  '4080super_16': {
    id: '4080super_16',
    name: 'RTX 4080 SUPER (16GB)',
    memory: 16,
    category: 'Nvidia GPU',
  },
  '4090_24': {
    id: '4090_24',
    name: 'RTX 4090 (24GB)',
    memory: 24,
    category: 'Nvidia GPU',
  },
  '5060_8': {
    id: '5060_8',
    name: 'RTX 5060 (8GB)',
    memory: 8,
    category: 'Nvidia GPU',
  },
  '5060ti_8': {
    id: '5060ti_8',
    name: 'RTX 5060 Ti (8GB)',
    memory: 8,
    category: 'Nvidia GPU',
  },
  '5060ti_16': {
    id: '5060ti_16',
    name: 'RTX 5060 Ti (16GB)',
    memory: 16,
    category: 'Nvidia GPU',
  },
  '5070_12': {
    id: '5070_12',
    name: 'RTX 5070 (12GB)',
    memory: 12,
    category: 'Nvidia GPU',
  },
  '5070ti_16': {
    id: '5070ti_16',
    name: 'RTX 5070 Ti (16GB)',
    memory: 16,
    category: 'Nvidia GPU',
  },
  '5080_16': {
    id: '5080_16',
    name: 'RTX 5080 (16GB)',
    memory: 16,
    category: 'Nvidia GPU',
  },
  '5090_32': {
    id: '5090_32',
    name: 'RTX 5090 (32GB)',
    memory: 32,
    category: 'Nvidia GPU',
  },
  rtx_2000_ada_16: {
    id: 'rtx_2000_ada_16',
    name: 'RTX 2000 Ada Generation (16GB)',
    memory: 16,
    category: 'Nvidia GPU',
  },
  rtx_a4000_16: {
    id: 'rtx_a4000_16',
    name: 'RTX A4000 (16GB)',
    memory: 16,
    category: 'Nvidia GPU',
  },
  rtx_a5000_24: {
    id: 'rtx_a5000_24',
    name: 'RTX A5000 (24GB)',
    memory: 24,
    category: 'Nvidia GPU',
  },
  rtx_a6000_48: {
    id: 'rtx_a6000_48',
    name: 'RTX A6000 (48GB)',
    memory: 48,
    category: 'Nvidia GPU',
  },
  rtx_4000_blackwell_24: {
    id: 'rtx_4000_blackwell_24',
    name: 'RTX 4000 Blackwell SFF (24GB)',
    memory: 24,
    category: 'Nvidia GPU',
  },
  rtx_4500_blackwell_32: {
    id: 'rtx_4500_blackwell_32',
    name: 'RTX 4500 Blackwell (32GB)',
    memory: 32,
    category: 'Nvidia GPU',
  },
  rtx_5000_blackwell_48: {
    id: 'rtx_5000_blackwell_48',
    name: 'RTX 5000 Blackwell (48GB)',
    memory: 48,
    category: 'Nvidia GPU',
  },
  rtx_6000_blackwell_96: {
    id: 'rtx_6000_blackwell_96',
    name: 'RTX 6000 Blackwell (96GB)',
    memory: 96,
    category: 'Nvidia GPU',
  },
  l40_48: {
    id: 'l40_48',
    name: 'L40 (48GB)',
    memory: 48,
    category: 'Nvidia GPU',
  },
  l40s_48: {
    id: 'l40s_48',
    name: 'L40S (48GB)',
    memory: 48,
    category: 'Nvidia GPU',
  },
  a2_16: {
    id: 'a2_16',
    name: 'A2 (16GB)',
    memory: 16,
    category: 'Nvidia GPU',
  },
  a16_64: {
    id: 'a16_64',
    name: 'A16 (64GB)',
    memory: 64,
    category: 'Nvidia GPU',
  },
  a30_24: {
    id: 'a30_24',
    name: 'A30 (24GB)',
    memory: 24,
    category: 'Nvidia GPU',
  },
  a40_48: {
    id: 'a40_48',
    name: 'A40 (48GB)',
    memory: 48,
    category: 'Nvidia GPU',
  },
  a100_40: {
    id: 'a100_40',
    name: 'A100 (40GB)',
    memory: 40,
    category: 'Nvidia GPU',
  },
  a100_80: {
    id: 'a100_80',
    name: 'A100 (80GB)',
    memory: 80,
    category: 'Nvidia GPU',
  },
  a800_40: {
    id: 'a800_40',
    name: 'A800 (40GB)',
    memory: 40,
    category: 'Nvidia GPU',
  },
  a800_80: {
    id: 'a800_80',
    name: 'A800 (80GB)',
    memory: 80,
    category: 'Nvidia GPU',
  },
  h100_80: {
    id: 'h100_80',
    name: 'H100 (80GB)',
    memory: 80,
    category: 'Nvidia GPU',
  },
  h100nvl_188: {
    id: 'h100nvl_188',
    name: 'H100 NVL (188GB)',
    memory: 188,
    category: 'Nvidia GPU',
  },
  h200_141: {
    id: 'h200_141',
    name: 'H200 (141GB)',
    memory: 141,
    category: 'Nvidia GPU',
  },
  h800_80: {
    id: 'h800_80',
    name: 'H800 (80GB)',
    memory: 80,
    category: 'Nvidia GPU',
  },
  b100_192: {
    id: 'b100_192',
    name: 'B100 (192GB)',
    memory: 192,
    category: 'Nvidia GPU',
  },
  b200_192: {
    id: 'b200_192',
    name: 'B200 (192GB)',
    memory: 192,
    category: 'Nvidia GPU',
  },
  custom_discrete: {
    id: 'custom_discrete',
    name: 'Custom (GPU)',
    memory: 0, // Custom value
    category: 'Nvidia GPU',
  },

  // Apple Silicon
  m2_pro_16: {
    id: 'm2_pro_16',
    name: 'M2 Pro (16GB)',
    memory: 16,
    category: 'Apple Silicon',
  },
  m2_max_32: {
    id: 'm2_max_32',
    name: 'M2 Max (32GB)',
    memory: 32,
    category: 'Apple Silicon',
  },
  m2_max_64: {
    id: 'm2_max_64',
    name: 'M2 Max (64GB)',
    memory: 64,
    category: 'Apple Silicon',
  },
  m2_max_96: {
    id: 'm2_max_96',
    name: 'M2 Max (96GB)',
    memory: 96,
    category: 'Apple Silicon',
  },
  m2_ultra_64: {
    id: 'm2_ultra_64',
    name: 'M2 Ultra (64GB)',
    memory: 64,
    category: 'Apple Silicon',
  },
  m2_ultra_128: {
    id: 'm2_ultra_128',
    name: 'M2 Ultra (128GB)',
    memory: 128,
    category: 'Apple Silicon',
  },
  m2_ultra_192: {
    id: 'm2_ultra_192',
    name: 'M2 Ultra (192GB)',
    memory: 192,
    category: 'Apple Silicon',
  },
  m3_pro_18: {
    id: 'm3_pro_18',
    name: 'M3 Pro (18GB)',
    memory: 18,
    category: 'Apple Silicon',
  },
  m3_pro_36: {
    id: 'm3_pro_36',
    name: 'M3 Pro (36GB)',
    memory: 36,
    category: 'Apple Silicon',
  },
  m3_max_36: {
    id: 'm3_max_36',
    name: 'M3 Max (36GB)',
    memory: 36,
    category: 'Apple Silicon',
  },
  m3_max_48: {
    id: 'm3_max_48',
    name: 'M3 Max (48GB)',
    memory: 48,
    category: 'Apple Silicon',
  },
  m3_max_64: {
    id: 'm3_max_64',
    name: 'M3 Max (64GB)',
    memory: 64,
    category: 'Apple Silicon',
  },
  m3_max_96: {
    id: 'm3_max_96',
    name: 'M3 Max (96GB)',
    memory: 96,
    category: 'Apple Silicon',
  },
  m3_max_128: {
    id: 'm3_max_128',
    name: 'M3 Max (128GB)',
    memory: 128,
    category: 'Apple Silicon',
  },
  m3_ultra_256: {
    id: 'm3_ultra_256',
    name: 'M3 Ultra (256GB)',
    memory: 256,
    category: 'Apple Silicon',
  },
  m3_ultra_512: {
    id: 'm3_ultra_512',
    name: 'M3 Ultra (512GB)',
    memory: 512,
    category: 'Apple Silicon',
  },
  m4_16: {
    id: 'm4_16',
    name: 'M4 (16GB)',
    memory: 16,
    category: 'Apple Silicon',
  },
  m4_24: {
    id: 'm4_24',
    name: 'M4 (24GB)',
    memory: 24,
    category: 'Apple Silicon',
  },
  m4_32: {
    id: 'm4_32',
    name: 'M4 (32GB)',
    memory: 32,
    category: 'Apple Silicon',
  },
  m4_pro_32: {
    id: 'm4_pro_32',
    name: 'M4 Pro (32GB)',
    memory: 32,
    category: 'Apple Silicon',
  },
  m4_pro_64: {
    id: 'm4_pro_64',
    name: 'M4 Pro (64GB)',
    memory: 64,
    category: 'Apple Silicon',
  },
  m4_max_64: {
    id: 'm4_max_64',
    name: 'M4 Max (64GB)',
    memory: 64,
    category: 'Apple Silicon',
  },
  m4_max_96: {
    id: 'm4_max_96',
    name: 'M4 Max (96GB)',
    memory: 96,
    category: 'Apple Silicon',
  },
  m4_max_128: {
    id: 'm4_max_128',
    name: 'M4 Max (128GB)',
    memory: 128,
    category: 'Apple Silicon',
  },
};

export const getGPUsByCategory = (category: 'Nvidia GPU' | 'Apple Silicon'): GPUInfo[] => {
  return Object.values(GPU_DATA).filter((gpu) => gpu.category === category);
};

export const getGPUsByMemoryRange = (minMemory: number, maxMemory: number): GPUInfo[] => {
  return Object.values(GPU_DATA).filter((gpu) => gpu.memory >= minMemory && gpu.memory <= maxMemory);
};

export const getGPUNames = (): string[] => {
  return Object.values(GPU_DATA).map((gpu) => gpu.name);
};

export const getGPUMemoryOptions = (): number[] => {
  const memories = Object.values(GPU_DATA)
    .map((gpu) => gpu.memory)
    .filter((memory) => memory > 0)
    .sort((a, b) => a - b);

  return [...new Set(memories)];
};
