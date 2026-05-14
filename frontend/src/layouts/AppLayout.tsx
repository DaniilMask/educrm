import { type ReactElement } from 'react'
import { NavLink, Outlet, useLocation } from 'react-router-dom'

import {
  AppBar,
  Box,
  CssBaseline,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
} from '@mui/material'

import {
  Dashboard,
  EventAvailable,
  People,
  School,
  Payments,
} from '@mui/icons-material'

const drawerWidth = 240

const navItems: { to: string; label: string; icon: ReactElement }[] = [
  { to: '/', label: 'Обзор', icon: <Dashboard /> },
  { to: '/students', label: 'Дети', icon: <People /> },
  { to: '/groups', label: 'Секции', icon: <School /> },
  { to: '/attendance', label: 'Посещаемость', icon: <EventAvailable /> },
  { to: '/payments', label: 'Платежи', icon: <Payments /> },
]

const pathTitles: Record<string, string> = {
  '/': 'Обзор',
  '/students': 'Дети',
  '/groups': 'Секции',
  '/attendance': 'Посещаемость',
  '/payments': 'Платежи',
}

export default function AppLayout() {
  const { pathname } = useLocation()
  const pageTitle = pathTitles[pathname] ?? 'EduCRM'

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />

      <AppBar
        position="fixed"
        sx={{ zIndex: 1201 }}
      >
        <Toolbar sx={{ position: 'relative' }}>
          <Typography variant="h6">{pageTitle}</Typography>
          <Box
            sx={{
              position: 'absolute',
              left: '50%',
              transform: 'translateX(-50%)',
              width: 42,
              height: 42,
              border: '1px solid',
              borderColor: 'divider',
              borderRadius: 0.5,
              display: 'grid',
              placeItems: 'center',
            }}
          >
            <Box
              component="img"
              src="/logo.svg"
              alt="Логотип"
              sx={{
                width: 28,
                height: 28,
                objectFit: 'contain',
                display: 'block',
                bgcolor: 'transparent',
              }}
            />
          </Box>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
      >
        <Toolbar />

        <List>
          {navItems.map(({ to, label, icon }) => (
            <ListItemButton
              key={to}
              component={NavLink}
              to={to}
              end={to === '/'}
              sx={(theme) => ({
                '&.active': {
                  bgcolor: 'action.selected',
                  borderRight: `3px solid ${theme.palette.primary.main}`,
                },
              })}
            >
              <ListItemIcon sx={{ color: 'inherit' }}>{icon}</ListItemIcon>

              <ListItemText primary={label} />
            </ListItemButton>
          ))}
        </List>
      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
        }}
      >
        <Toolbar />

        <Outlet />
      </Box>
    </Box>
  )
}
