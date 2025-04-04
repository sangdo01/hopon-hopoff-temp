export const paths = {
  home: 'admin/',
  auth: { signIn: '/admin/auth/sign-in', signUp: '/admin/auth/sign-up', resetPassword: '/admin/auth/reset-password' },
  dashboard: {
    overview: '/admin/dashboard',
    account: '/admin/dashboard/account',
    customers: '/admin/dashboard/customers',
    integrations: '/admin/dashboard/integrations',
    settings: '/admin/dashboard/settings',
  },
  errors: { notFound: '/errors/not-found' },
} as const;
