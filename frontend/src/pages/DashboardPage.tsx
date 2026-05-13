import { useEffect, useState } from 'react'
import {
  Alert,
  Box,
  Card,
  CardContent,
  CircularProgress,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Stack,
  TextField,
  Typography,
} from '@mui/material'

import { getStudentsSummary, type StudentsSummary } from '../api/students'

type PeriodPreset = 'today' | 'last_7_days' | 'custom'

function formatDate(value: Date) {
  return value.toISOString().slice(0, 10)
}

export default function DashboardPage() {
  const [summary, setSummary] = useState<StudentsSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [periodPreset, setPeriodPreset] = useState<PeriodPreset>('today')
  const [groupName, setGroupName] = useState('all')
  const [startDate, setStartDate] = useState(formatDate(new Date()))
  const [endDate, setEndDate] = useState(formatDate(new Date()))

  useEffect(() => {
    if (periodPreset === 'custom') {
      return
    }

    const now = new Date()
    if (periodPreset === 'today') {
      const date = formatDate(now)
      setStartDate(date)
      setEndDate(date)
      return
    }

    const start = new Date(now)
    start.setDate(now.getDate() - 6)
    setStartDate(formatDate(start))
    setEndDate(formatDate(now))
  }, [periodPreset])

  useEffect(() => {
    async function loadSummary() {
      setLoading(true)
      setError(null)
      try {
        const data = await getStudentsSummary({
          startDate,
          endDate,
          groupName,
        })
        setSummary(data)
      } catch (requestError) {
        const message =
          requestError instanceof Error ? requestError.message : 'Не удалось загрузить статистику'
        setError(message)
      } finally {
        setLoading(false)
      }
    }

    void loadSummary()
  }, [startDate, endDate, groupName])

  const periodLabel =
    periodPreset === 'today'
      ? 'За сегодня'
      : periodPreset === 'last_7_days'
        ? 'За последние 7 дней'
        : `${startDate} - ${endDate}`

  if (loading) {
    return <CircularProgress size={24} />
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>
  }

  if (!summary) {
    return <Alert severity="info">Нет данных для отображения</Alert>
  }

  const stats = [
    { title: 'Всего детей', value: String(summary.total_children) },
    { title: 'Активных', value: String(summary.active_children) },
    { title: 'Неактивных', value: String(summary.inactive_children) },
    { title: 'Доходы', value: '0' },
    { title: 'Расходы', value: '0' },
    { title: 'Новых записей', value: '0' },
  ] as const

  return (
    <Stack spacing={2}>
      <Paper variant="outlined" sx={{ p: 2 }}>
        <Stack direction={{ xs: 'column', md: 'row' }} spacing={2}>
          <FormControl size="small" sx={{ minWidth: 220 }}>
            <InputLabel id="period-label">Статистика</InputLabel>
            <Select
              labelId="period-label"
              value={periodPreset}
              label="Статистика"
              onChange={(event) => setPeriodPreset(event.target.value as PeriodPreset)}
            >
              <MenuItem value="today">За сегодня</MenuItem>
              <MenuItem value="last_7_days">За последние 7 дней</MenuItem>
              <MenuItem value="custom">Период по датам</MenuItem>
            </Select>
          </FormControl>

          <TextField
            size="small"
            label="Дата с"
            type="date"
            value={startDate}
            onChange={(event) => setStartDate(event.target.value)}
            slotProps={{ inputLabel: { shrink: true } }}
          />

          <TextField
            size="small"
            label="Дата по"
            type="date"
            value={endDate}
            onChange={(event) => setEndDate(event.target.value)}
            slotProps={{ inputLabel: { shrink: true } }}
          />

          <FormControl size="small" sx={{ minWidth: 220 }}>
            <InputLabel id="group-label">Группа</InputLabel>
            <Select
              labelId="group-label"
              value={groupName}
              label="Группа"
              onChange={(event) => setGroupName(event.target.value)}
            >
              <MenuItem value="all">Все группы</MenuItem>
              <MenuItem value="junior">Младшая</MenuItem>
              <MenuItem value="middle">Средняя</MenuItem>
              <MenuItem value="senior">Старшая</MenuItem>
            </Select>
          </FormControl>
        </Stack>
      </Paper>

      <Grid container spacing={2}>
        {stats.map(({ title, value }) => (
          <Grid key={title} size={{ xs: 12, sm: 6, md: 4, lg: 2 }}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {title}
                </Typography>

                <Typography variant="h4" component="p">
                  {value}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={2}>
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper variant="outlined" sx={{ p: 2, minHeight: 180 }}>
            <Typography variant="subtitle1" gutterBottom>
              Ближайшие дни рождения
            </Typography>
            <Typography color="text.secondary">Нет данных за выбранный период.</Typography>
          </Paper>
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper variant="outlined" sx={{ p: 2, minHeight: 180 }}>
            <Typography variant="subtitle1" gutterBottom>
              Неотработанные посещения
            </Typography>
            <Typography color="text.secondary">Все посещения отработаны.</Typography>
          </Paper>
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper variant="outlined" sx={{ p: 2, minHeight: 180 }}>
            <Typography variant="subtitle1" gutterBottom>
              Мои текущие задачи
            </Typography>
            <Typography color="text.secondary">У вас нет текущих задач.</Typography>
          </Paper>
        </Grid>
      </Grid>

      <Grid container spacing={2}>
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper variant="outlined" sx={{ p: 2, minHeight: 180 }}>
            <Typography variant="subtitle1" gutterBottom>
              Непродленные абонементы
            </Typography>
            <Typography color="text.secondary">Нет подходящих абонементов.</Typography>
          </Paper>
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper variant="outlined" sx={{ p: 2, minHeight: 180 }}>
            <Typography variant="subtitle1" gutterBottom>
              Задолженности
            </Typography>
            <Typography color="text.secondary">Задолженности отсутствуют.</Typography>
          </Paper>
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <Paper variant="outlined" sx={{ p: 2, minHeight: 180 }}>
            <Typography variant="subtitle1" gutterBottom>
              Неоплаченные посещения
            </Typography>
            <Typography color="text.secondary">Нет неоплаченных посещений.</Typography>
          </Paper>
        </Grid>
      </Grid>

      <Box>
        <Typography variant="caption" color="text.secondary">
          Период отчета: {periodLabel}. Все отчеты дальше строим по этой схеме: диапазон дат +
          выбранная группа.
        </Typography>
      </Box>
    </Stack>
  )
}
