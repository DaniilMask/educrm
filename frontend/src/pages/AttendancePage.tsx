import { useEffect, useState } from 'react'
import { Alert, Button, MenuItem, Paper, Select, Stack, Table, TableBody, TableCell, TableHead, TableRow, TextField } from '@mui/material'

import { getAttendanceByLesson, upsertAttendance, type Attendance } from '../api/attendance'
import { getLessons, type Lesson } from '../api/lessons'
import { getStudents, type Student } from '../api/students'

const attendanceStatuses = ['present', 'absent', 'late', 'trial', 'sick']

export default function AttendancePage() {
  const [lessons, setLessons] = useState<Lesson[]>([])
  const [students, setStudents] = useState<Student[]>([])
  const [lessonId, setLessonId] = useState('')
  const [rows, setRows] = useState<Attendance[]>([])
  const [studentId, setStudentId] = useState('')
  const [status, setStatus] = useState('present')
  const [comment, setComment] = useState('')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getLessons().then(setLessons).catch((e: Error) => setError(e.message))
    getStudents().then(setStudents).catch((e: Error) => setError(e.message))
  }, [])

  async function load() {
    try { setRows(await getAttendanceByLesson(Number(lessonId))) } catch (e) { setError((e as Error).message) }
  }

  async function save() {
    try {
      await upsertAttendance({ lesson_id: Number(lessonId), student_id: Number(studentId), status, comment: comment || null })
      await load()
    } catch (e) { setError((e as Error).message) }
  }

  return (
    <Stack spacing={2}>
      {error ? <Alert severity="error">{error}</Alert> : null}
      <Paper variant="outlined" sx={{ p: 2 }}>
        <Stack direction="row" spacing={2}>
          <Select value={lessonId} onChange={(e) => setLessonId(e.target.value)} displayEmpty sx={{ minWidth: 220 }}>
            <MenuItem value="">Выберите занятие</MenuItem>
            {lessons.map((lesson) => <MenuItem key={lesson.id} value={String(lesson.id)}>#{lesson.id} {lesson.date} {lesson.start_time}</MenuItem>)}
          </Select>
          <Button variant="outlined" onClick={() => void load()}>Загрузить</Button>
          <Select value={studentId} onChange={(e) => setStudentId(e.target.value)} displayEmpty sx={{ minWidth: 240 }}>
            <MenuItem value="">Выберите ребенка</MenuItem>
            {students.map((student) => <MenuItem key={student.id} value={String(student.id)}>{student.full_name}</MenuItem>)}
          </Select>
          <Select value={status} onChange={(e) => setStatus(e.target.value)} sx={{ minWidth: 160 }}>
            {attendanceStatuses.map((item) => <MenuItem key={item} value={item}>{item}</MenuItem>)}
          </Select>
          <TextField label="Комментарий" value={comment} onChange={(e) => setComment(e.target.value)} />
          <Button variant="contained" onClick={() => void save()}>Сохранить</Button>
        </Stack>
      </Paper>
      <Table>
        <TableHead><TableRow><TableCell>Ребенок</TableCell><TableCell>Статус</TableCell><TableCell>Комментарий</TableCell></TableRow></TableHead>
        <TableBody>{rows.map((row) => <TableRow key={row.id}><TableCell>{row.student_id}</TableCell><TableCell>{row.status}</TableCell><TableCell>{row.comment ?? '-'}</TableCell></TableRow>)}</TableBody>
      </Table>
    </Stack>
  )
}
