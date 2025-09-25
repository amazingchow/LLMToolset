import { useTranslations } from 'next-intl';

import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export function RegisterForm({ className, ...props }: React.ComponentProps<'div'>) {
  const t = useTranslations('RegisterPage');
  return (
    <div className={cn('flex flex-col gap-6', className)} {...props}>
      <Card>
        <CardHeader>
          <CardTitle>{t('c_h_title')}</CardTitle>
          <CardDescription>{t('c_h_description')}</CardDescription>
        </CardHeader>
        <CardContent>
          <form>
            <div className="flex flex-col gap-6">
              <div className="grid gap-3">
                <Label htmlFor="email">{t('c_c_email')}</Label>
                <Input id="email" type="email" placeholder="m@example.com" required />
              </div>
              <div className="grid gap-3">
                <Label htmlFor="password">{t('c_c_password')}</Label>
                <Input id="password" type="password" required />
              </div>
              <div className="grid gap-3">
                <Label htmlFor="confirm_password">{t('c_c_confirm_password')}</Label>
                <Input id="confirm_password" type="password" required />
              </div>
              <div className="flex flex-col gap-3">
                <Button type="submit" className="w-full">
                  {t('c_c_register')}
                </Button>
              </div>
            </div>
            <div className="mt-4 text-center text-sm">
              {t('c_c_already_have_an_account')}{' '}
              <a href="#" className="underline underline-offset-4">
                {t('c_c_login')}
              </a>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
