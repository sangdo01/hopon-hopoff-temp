'use client';

import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import { Experimental_CssVarsProvider as CssVarsProvider } from '@mui/material/styles';

import { createTheme } from '@/styles/theme/create-theme';

import EmotionCache from './emotion-cache';

import { ThemeProvider as ThemeProviderMUI } from '@mui/material/styles';

export interface ThemeProviderProps {
  children: React.ReactNode;
}

export function ThemeProvider({ children }: ThemeProviderProps): React.JSX.Element {
  const theme = createTheme();

  return (
    // <EmotionCache options={{ key: 'mui' }}>
    //   <CssVarsProvider theme={theme}>
    //     <CssBaseline />
    //     {children}
    //   </CssVarsProvider>
    // </EmotionCache>
    <EmotionCache options={{ key: 'mui' }}>
      <ThemeProviderMUI theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProviderMUI>
    </EmotionCache>
  );
}
