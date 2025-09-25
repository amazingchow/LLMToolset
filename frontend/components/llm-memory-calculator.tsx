'use client';

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { useQuery } from '@tanstack/react-query';
import { Bug, Calculator, HelpCircle } from 'lucide-react';
import { useTranslations } from 'next-intl';

import {
  calculateInferenceMemory,
  calculateTrainingMemory,
  fetchConfigOptions,
  type CalculationResponse,
  type MemoryCalculationRequest,
} from '@/lib/api';
import { GPU_DATA, type GPUInfo } from '@/lib/gpu-data';
import { parseMemoryToGB } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import BatchIcon from '@/components/icons/BatchIcon';
import ClusterIcon from '@/components/icons/ClusterIcon';
import GPUIcon from '@/components/icons/GPUIcon';
import InferIcon from '@/components/icons/InferIcon';
import OpenAIIcon from '@/components/icons/OpenAIIcon';
import { MemoryBreakdown } from '@/components/memory-breakdown';
import { ProgressCircle } from '@/components/progress-circle';

export function LLMMemoryCalculator() {
  const t = useTranslations('LLMMemoryCalculatorPage');

  const [calculationType, setCalculationType] = useState<'inference' | 'training'>('inference');
  const [selectedModel, setSelectedModel] = useState<string>('');
  const [parameters, setParameters] = useState({
    precision: 'bfloat16',
    batchSize: 1,
    sequenceLength: 8192,
    kvCachePrecision: 'bfloat16',
    useFlashAttention: true,
    usePageAttention: true,
    peft: 'LoRA',
    trainableParams: 1,
    optimizer: 'AdamW',
    gpu: 'RTX 4090 (24GB)',
    gpuCount: 1,
    gpuMemory: 24,
    totalGpuMemory: 24,
  });
  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState<CalculationResponse | null>(null);

  const { data: configOptions } = useQuery({
    queryKey: ['config-options'],
    queryFn: fetchConfigOptions,
  });

  const models = useMemo(() => {
    return configOptions?.available_models || [];
  }, [configOptions?.available_models]);

  const selectedGpuInfo = useMemo(() => {
    return Object.values(GPU_DATA).find((gpu) => gpu.name === parameters.gpu);
  }, [parameters.gpu]);

  const gpuMemory = useMemo(() => {
    return selectedGpuInfo?.memory || parameters.gpuMemory;
  }, [selectedGpuInfo?.memory, parameters.gpuMemory]);

  const totalGpuMemory = useMemo(() => {
    return gpuMemory * parameters.gpuCount;
  }, [gpuMemory, parameters.gpuCount]);

  useEffect(() => {
    if (models.length > 0 && !selectedModel) {
      const defaultModel = models.find((model) => model.includes('Qwen3-8B')) || models[0];
      setSelectedModel(defaultModel);
    }
  }, [models, selectedModel]);

  const handleCalculate = async () => {
    setIsCalculating(true);
    try {
      const request: MemoryCalculationRequest = {
        model_name: selectedModel,
        precision: parameters.precision,
        batch_size: parameters.batchSize,
        sequence_length: parameters.sequenceLength,
        kv_cache_precision: parameters.kvCachePrecision,
        use_flash_attention: parameters.useFlashAttention,
        use_page_attention: parameters.usePageAttention,
      };
      let response: CalculationResponse;
      if (calculationType === 'inference') {
        response = await calculateInferenceMemory(request);
      } else {
        response = await calculateTrainingMemory({
          ...request,
          optimizer: parameters.optimizer,
          trainable_parameters: parameters.trainableParams,
        });
      }
      setResult(response);
    } catch (error) {
      console.error('Error calculating memory:', error);
    } finally {
      setIsCalculating(false);
    }
  };

  const calculateGpuUtilization = () => {
    if (!result) return 0;
    const totalMemoryKey = calculationType === 'inference' ? 'inference_memory' : 'training_memory';
    const totalMemory = result.memory_requirements[totalMemoryKey];
    if (!totalMemory) return 0;

    const totalGB = parseMemoryToGB(totalMemory);

    return Math.min((totalGB / totalGpuMemory) * 100, 100);
  };
  const gpuUtilization = calculateGpuUtilization();

  const calculateRawGpuUtilization = () => {
    if (!result) return 0;
    const totalMemoryKey = calculationType === 'inference' ? 'inference_memory' : 'training_memory';
    const totalMemory = result.memory_requirements[totalMemoryKey];
    if (!totalMemory) return 0;

    const totalGB = parseMemoryToGB(totalMemory);
    return (totalGB / totalGpuMemory) * 100;
  };
  const rawGpuUtilization = calculateRawGpuUtilization();

  const getUtilizationStatus = () => {
    if (rawGpuUtilization > 100) {
      return { text: t('get_utilization_status_level_4'), className: 'bg-red-600 text-white' };
    }
    if (rawGpuUtilization >= 90) {
      return { text: t('get_utilization_status_level_3'), className: 'bg-red-400 text-white' };
    }
    if (rawGpuUtilization >= 70) {
      return { text: t('get_utilization_status_level_2'), className: 'bg-green-400 text-white' };
    }
    return { text: t('get_utilization_status_level_1'), className: 'bg-green-600 text-white' };
  };
  const utilizationStatus = getUtilizationStatus();

  return (
    <div className="mx-auto grid max-w-7xl grid-cols-1 gap-8 lg:grid-cols-2">
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calculator className="h-5 w-5" />
              {t('l_c_h_title')}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">{t('l_c_c_1_model')} *</label>
              <Select value={selectedModel} onValueChange={setSelectedModel}>
                <SelectTrigger>
                  <div className="flex items-center gap-2">
                    <OpenAIIcon className="h-4 w-4" />
                    <SelectValue />
                  </div>
                </SelectTrigger>
                <SelectContent className="max-h-[300px] overflow-y-auto">
                  {models.map((model) => (
                    <SelectItem key={model} value={model}>
                      {model}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="flex items-center gap-1 text-sm font-medium">
                {t('l_c_c_2_precision')}
                <div className="group relative">
                  <HelpCircle className="h-4 w-4 cursor-help text-gray-400" />
                  <div className="pointer-events-none absolute bottom-full left-1/2 z-10 mb-2 -translate-x-1/2 transform rounded-lg bg-gray-800 px-3 py-2 text-xs whitespace-nowrap text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                    {t('l_c_c_2_precision_tip')}
                    <div className="absolute top-full left-1/2 -translate-x-1/2 transform border-4 border-transparent border-t-gray-800"></div>
                  </div>
                </div>
              </label>
              <Select
                value={parameters.precision}
                onValueChange={(value) => setParameters((prev) => ({ ...prev, precision: value }))}
              >
                <SelectTrigger>
                  <div className="flex items-center gap-2">
                    <InferIcon className="h-4 w-4" />
                    <SelectValue />
                  </div>
                </SelectTrigger>
                <SelectContent className="max-h-[200px] overflow-y-auto">
                  {configOptions?.data_types.map((type) => (
                    <SelectItem key={type} value={type}>
                      {type}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="flex items-center gap-1 text-sm font-medium">
                {t('l_c_c_3_batch_size')}
                <div className="group relative">
                  <HelpCircle className="h-4 w-4 cursor-help text-gray-400" />
                  <div className="pointer-events-none absolute bottom-full left-1/2 z-10 mb-2 -translate-x-1/2 transform rounded-lg bg-gray-800 px-3 py-2 text-xs whitespace-nowrap text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                    {t('l_c_c_3_batch_size_tip')}
                    <div className="absolute top-full left-1/2 -translate-x-1/2 transform border-4 border-transparent border-t-gray-800"></div>
                  </div>
                </div>
              </label>
              <div className="relative">
                <BatchIcon className="absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2" />
                <Input
                  type="number"
                  value={parameters.batchSize}
                  onChange={(e) => {
                    const value = parseInt(e.target.value) || 1;
                    const clampedValue = Math.min(Math.max(value, 1), 32);
                    setParameters((prev) => ({
                      ...prev,
                      batchSize: clampedValue,
                    }));
                  }}
                  min="1"
                  max="32"
                  className="pl-8"
                />
              </div>
            </div>
            <div className="space-y-2">
              <label className="flex items-center gap-1 text-sm font-medium">
                {t('l_c_c_4_sequence_length')}
                <div className="group relative">
                  <HelpCircle className="h-4 w-4 cursor-help text-gray-400" />
                  <div className="pointer-events-none absolute bottom-full left-1/2 z-10 mb-2 -translate-x-1/2 transform rounded-lg bg-gray-800 px-3 py-2 text-xs whitespace-nowrap text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                    {t('l_c_c_4_sequence_length_tip')}
                    <div className="absolute top-full left-1/2 -translate-x-1/2 transform border-4 border-transparent border-t-gray-800"></div>
                  </div>
                </div>
              </label>
              <span className="text-xs text-gray-500">{parameters.sequenceLength}</span>
              <input
                type="range"
                min="1024"
                max="32768"
                step="1024"
                value={parameters.sequenceLength}
                onChange={(e) =>
                  setParameters((prev) => ({
                    ...prev,
                    sequenceLength: parseInt(e.target.value),
                  }))
                }
                className="h-2 w-full cursor-pointer appearance-none rounded-lg bg-gray-200"
              />
              <div className="flex justify-between text-xs text-gray-500">
                <span>1K</span>
                <span>8K</span>
                <span>16K</span>
                <span>24K</span>
                <span>32K</span>
              </div>
            </div>
            <div className="space-y-2">
              <label className="flex items-center gap-1 text-sm font-medium">
                {t('l_c_c_7_kv_cache_precision')}
                <div className="group relative">
                  <HelpCircle className="h-4 w-4 cursor-help text-gray-400" />
                  <div className="pointer-events-none absolute bottom-full left-1/2 z-10 mb-2 -translate-x-1/2 transform rounded-lg bg-gray-800 px-3 py-2 text-xs whitespace-nowrap text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                    {t('l_c_c_7_kv_cache_precision_tip')}
                    <div className="absolute top-full left-1/2 -translate-x-1/2 transform border-4 border-transparent border-t-gray-800"></div>
                  </div>
                </div>
              </label>
              <Select
                value={parameters.precision}
                onValueChange={(value) => setParameters((prev) => ({ ...prev, precision: value }))}
              >
                <SelectTrigger>
                  <div className="flex items-center gap-2">
                    <InferIcon className="h-4 w-4" />
                    <SelectValue />
                  </div>
                </SelectTrigger>
                <SelectContent className="max-h-[200px] overflow-y-auto">
                  {configOptions?.data_types.map((type) => (
                    <SelectItem key={type} value={type}>
                      {type}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t('l_c_c_5_gpu_model')}</label>
              <Select
                value={parameters.gpu}
                onValueChange={(value) => setParameters((prev) => ({ ...prev, gpu: value }))}
              >
                <SelectTrigger>
                  <div className="flex items-center gap-2">
                    <GPUIcon className="h-4 w-4" />
                    <SelectValue />
                  </div>
                </SelectTrigger>
                <SelectContent className="max-h-[200px] overflow-y-auto">
                  {Object.values(GPU_DATA).map((type: GPUInfo) => (
                    <SelectItem key={type.name} value={type.name}>
                      {type.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t('l_c_c_6_gpu_count')}</label>
              <div className="relative">
                <ClusterIcon className="absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2" />
                <Input
                  type="number"
                  value={parameters.gpuCount}
                  onChange={(e) => {
                    const value = parseInt(e.target.value) || 1;
                    const clampedValue = Math.min(Math.max(value, 1), 100000);
                    setParameters((prev) => ({
                      ...prev,
                      gpuCount: clampedValue,
                    }));
                  }}
                  min="1"
                  max="100000"
                  className="pl-8"
                />
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex flex-col items-start gap-2">
            <div className="text-xs text-gray-500">* {t('tips')}</div>
            <Link
              href="https://github.com/amazingchow/LLMToolset/issues/new"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-xs text-gray-400 hover:underline"
            >
              <Bug className="h-4 w-4" />
              {t('feedback')}
            </Link>
          </CardFooter>
        </Card>

        {/* <Card>
          <CardHeader>
            <div className="flex items-center gap-4">
              <label className="flex cursor-pointer items-center gap-2">
                <input
                  type="checkbox"
                  checked={calculationType === 'training'}
                  onChange={(e) => setCalculationType(e.target.checked ? 'training' : 'inference')}
                  className="rounded"
                />
                开发训练模式
              </label>
            </div>
          </CardHeader>
          {calculationType === 'training' && (
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">可训练参数: {parameters.trainableParams}%</label>
                <input
                  type="range"
                  min="1"
                  max="100"
                  value={parameters.trainableParams}
                  onChange={(e) =>
                    setParameters((prev) => ({
                      ...prev,
                      trainableParams: parseInt(e.target.value),
                    }))
                  }
                  className="h-2 w-full cursor-pointer appearance-none rounded-lg bg-gray-200"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">优化器</label>
                <Select
                  value={parameters.optimizer}
                  onValueChange={(value) => setParameters((prev) => ({ ...prev, optimizer: value }))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {configOptions?.optimizers.map((optimizer) => (
                      <SelectItem key={optimizer} value={optimizer}>
                        {optimizer}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          )}
        </Card> */}

        <Button onClick={handleCalculate} disabled={!selectedModel || isCalculating} className="h-12 w-full text-lg">
          {isCalculating ? t('is_calculating') : t('button_name')}
        </Button>
      </div>

      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>{t('r_c_h_title')}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="mb-6 flex items-center justify-center">
              <ProgressCircle percentage={gpuUtilization}>
                <div className="text-center">
                  <div className="text-2xl font-bold">{gpuUtilization.toFixed(1)}%</div>
                  <div className="text-xs text-gray-500">{t('r_c_c_1_gpu_utilization_circle')}</div>
                </div>
              </ProgressCircle>
            </div>
            <div className="space-y-2 text-center">
              <div className="text-2xl font-bold">
                {t('r_c_c_2_gpu_utilization_text_1')}:{' '}
                {result
                  ? parseMemoryToGB(
                      result.memory_requirements[
                        calculationType === 'inference' ? 'inference_memory' : 'training_memory'
                      ] || '0 GB',
                    ).toFixed(2)
                  : '0'}{' '}
                GB{' '}
                <span className={`rounded px-2 py-0.5 text-xs ${utilizationStatus.className}`}>
                  {utilizationStatus.text}
                </span>
              </div>
              <div className="text-sm text-gray-600">
                {t('r_c_c_2_gpu_utilization_text_2')} {totalGpuMemory} GB {t('r_c_c_2_gpu_utilization_text_3')} (x{' '}
                {parameters.gpuCount} GPU)
              </div>
            </div>
          </CardContent>
        </Card>

        {result && <MemoryBreakdown result={result} calculationType={calculationType} />}
      </div>
    </div>
  );
}
