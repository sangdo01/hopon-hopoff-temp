import React, { ReactNode } from "react";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import GlobalStyles from '@mui/material/GlobalStyles';
import { ThemeProvider } from "@/components/core/theme-provider/theme-provider";
import { AuthGuard } from "@/components/auth/auth-guard";
import { SideNav } from "@/components/layouts/admin/side-nav";
import { MainNav } from "@/components/layouts/admin/main-nav";

export const metadata = {
  title: "Hop On Hop Off",
  description: "Admin dashboard for managing the Hop On Hop Off platform",
};

const AdminLayout = ({ children }: { children: ReactNode }) => {
  return (
    <ThemeProvider>
      <AuthGuard>
      <GlobalStyles
        styles={{
          body: {
            '--MainNav-height': '56px',
            '--MainNav-zIndex': 1000,
            '--SideNav-width': '280px',
            '--SideNav-zIndex': 1100,
            '--MobileNav-width': '320px',
            '--MobileNav-zIndex': 1100,
          },
        }}
      />
      <Box
        sx={{
          bgcolor: 'var(--mui-palette-background-default)',
          display: 'flex',
          flexDirection: 'column',
          position: 'relative',
          minHeight: '100%',
        }}
      >
        <SideNav />
        <Box sx={{ display: 'flex', flex: '1 1 auto', flexDirection: 'column', pl: { lg: 'var(--SideNav-width)' } }}>
          <MainNav />
          <main>
            <Container maxWidth="xl" sx={{ py: '64px' }}>
              {children}
            </Container>
          </main>
        </Box>
      </Box>
    </AuthGuard>
    </ThemeProvider>
  );
};

export default AdminLayout;
