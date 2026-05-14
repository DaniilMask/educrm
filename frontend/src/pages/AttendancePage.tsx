import { useState } from 'react'
import { Alert, Button, Paper, Stack, Table, TableBody, TableCell, TableHead, TableRow, TextField } from '@mui/material'

import { getAttendanceByLesson, upsertAttendance, type Attendance } from '../api/attendance'

export default function AttendancePage() {
  const [lessonId, setLessonId] = useState('')
  const [rows, setRows] = useState<Attendance[]>([])
  const [studentId, setStudentId] = useState('')
  const [status, setStatus] = useState('present')
  const [error, setError] = useState<string | null>(null)

  async function load() {
    try { setRows(await getAttendanceByLesson(Number(lessonId))) } catch (e) { setError((e as Error).message) }
  }

  async function save() {
    try {
      await upsertAttendance({ lesson_id: Number(lessonId), student_id: Number(studentId), status, comment: null })
      await load()
    } catch (e) { setError((e as Error).message) }
  }

  return (
    <Stack spacing={2}>
      {error ? <Alert severity="error">{error}</Alert> : null}
      <Paper variant="outlined" sx={{ p: 2 }}>
        <Stack direction="row" spacing={2}>
          <TextField label="ID занятия" value={lessonId} onChange={(e) => setLessonId(e.target.value)} />
          <Button variant="outlined" onClick={() => void load()}>Загрузить</Button>
          <TextField label="ID ребенка" value={studentId} onChange={(e) => setStudentId(e.target.value)} />
          <TextField label="Статус" value={status} onChange={(e) => setStatus(e.target.value)} />
          <Button variant="contained" onClick={() => void save()}>Сохранить</Button>
        </Stack>
      </Paper>
      <Table>
        <TableHead><TableRow><TableCell>Ребенок</TableCell><TableCell>Статус</TableCell></TableRow></TableHead>
        <TableBody>{rows.map((row) => <TableRow key={row.id}><TableCell>{row.student_id}</TableCell><TableCell>{row.status}</TableCell></TableRow>)}</TableBody>
      </Table>
    </Stack>
  )
}
