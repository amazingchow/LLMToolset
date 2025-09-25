'use client';

import { useTranslations } from 'next-intl';

import { type CalculationResponse } from '@/lib/api';
import { parseMemoryToGB } from '@/lib/utils';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface MemoryBreakdownProps {
  result: CalculationResponse;
  calculationType: 'inference' | 'training';
}

export function MemoryBreakdown({ result, calculationType }: MemoryBreakdownProps) {
  const t = useTranslations('MemoryBreakdownComponent');

  const { memory_requirements } = result;

  const getMemoryItems = () => {
    const items = [
      {
        label: t('memory_item_1'),
        value: memory_requirements.model_weights_memory || '0 GB',
        color: 'bg-blue-500',
        percentage: 0,
      },
      {
        label: t('memory_item_2'),
        value: memory_requirements.kv_cache_memory || '0 GB',
        color: 'bg-purple-500',
        percentage: 0,
      },
      {
        label: t('memory_item_3'),
        value: memory_requirements.activation_memory || '0 GB',
        color: 'bg-green-500',
        percentage: 0,
      },
      {
        label: t('memory_item_4'),
        value: memory_requirements.overhead_memory || '0 GB',
        color: 'bg-red-500',
        percentage: 0,
      },
    ];

    if (calculationType === 'training') {
      items.push(
        {
          label: t('memory_item_5'),
          value: memory_requirements.optimizer_memory || '0 GB',
          color: 'bg-orange-500',
          percentage: 0,
        },
        {
          label: t('memory_item_6'),
          value: memory_requirements.gradients_memory || '0 GB',
          color: 'bg-yellow-500',
          percentage: 0,
        },
      );
    }

    const totalMemoryKey = calculationType === 'inference' ? 'inference_memory' : 'training_memory';
    const totalMemory = parseMemoryToGB(memory_requirements[totalMemoryKey] || '0 GB');

    items.forEach((item) => {
      const itemMemory = parseMemoryToGB(item.value || '0 GB');
      item.percentage = totalMemory > 0 ? (itemMemory / totalMemory) * 100 : 0;
    });

    return items;
  };

  const memoryItems = getMemoryItems();
  const totalMemoryKey = calculationType === 'inference' ? 'inference_memory' : 'training_memory';
  const totalMemory = memory_requirements[totalMemoryKey] || '0 GB';

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('c_h_title')}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="h-4 w-full overflow-hidden rounded-full bg-gray-200">
          <div className="flex h-full">
            {memoryItems.map((item, index) => (
              <div key={index} className={item.color} style={{ width: `${item.percentage}%` }} />
            ))}
          </div>
        </div>
        <div className="space-y-3">
          {memoryItems.map((item, index) => (
            <div key={index} className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className={`h-3 w-3 rounded-full ${item.color}`} />
                <span className="text-sm font-medium">{item.label}</span>
              </div>
              <div className="text-right">
                <div className="text-sm font-bold">{parseMemoryToGB(item.value).toFixed(2)} GB</div>
                <div className="text-xs text-gray-500">{item.percentage.toFixed(1)}%</div>
              </div>
            </div>
          ))}
        </div>
        <div className="border-t pt-3">
          <div className="flex items-center justify-between font-bold">
            <span>{t('c_c_total')}</span>
            <span>{parseMemoryToGB(totalMemory).toFixed(2)} GB</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
