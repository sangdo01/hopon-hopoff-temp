import * as React from 'react';
import type { Metadata } from 'next';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
// import Grid from '@mui/material/Unstable_Grid2';
import Grid from '@mui/material/Grid';
import { config } from '@/config';
import { AccountDetailsForm } from '@/components/dashboard/account/account-details-form';
import { AccountInfo } from '@/components/dashboard/account/account-info';

export const metadata = { title: `Account | Dashboard | ${config.site.name}` } satisfies Metadata;

export default function Page(): React.JSX.Element {
  return (
    <Stack spacing={3}>
      <div>
        <Typography variant="h4">Account</Typography>
      </div>
      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 6, lg: 4 }}>
          <AccountInfo />
        </Grid>
        <Grid size={{ xs: 12, md: 6, lg: 8 }}>
          <AccountDetailsForm />
        </Grid>
      </Grid>
    </Stack>
  );
}
