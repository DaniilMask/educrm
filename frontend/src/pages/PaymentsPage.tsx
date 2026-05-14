import { useEffect, useState } from 'react'
import { Alert, Button, MenuItem, Paper, Select, Stack, Table, TableBody, TableCell, TableHead, TableRow, TextField } from '@mui/material'

import { createPayment, getPayments, type Payment } from '../api/payments'
import { getStudents, type Student } from '../api/students'

export default function PaymentsPage() {
  const [rows, setRows] = useState<Payment[]>([])
  const [students, setStudents] = useState<Student[]>([])
  const [studentId, setStudentId] = useState('')
  const [amount, setAmount] = useState('')
  const [method, setMethod] = useState('cash')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getPayments().then(setRows).catch((e: Error) => setError(e.message))
    getStudents().then(setStudents).catch((e: Error) => setError(e.message))
  }, [])

  async function onCreate() {
    const created = await createPayment({ student_id: Number(studentId), amount, payment_date: new Date().toISOString().slice(0, 10), method, comment: null })
    setRows((prev) => [...prev, created])
  }

  return (
    <Stack spacing={2}>
      {error ? <Alert severity="error">{error}</Alert> : null}
      <Paper variant="outlined" sx={{ p: 2 }}>
        <Stack direction="row" spacing={2}>
          <Select value={studentId} onChange={(e) => setStudentId(e.target.value)} displayEmpty sx={{ minWidth: 260 }}>
            <MenuItem value="">Выберите ребенка</MenuItem>
            {students.map((student) => <MenuItem key={student.id} value={String(student.id)}>{student.full_name}</MenuItem>)}
          </Select>
          <TextField label="Сумма" value={amount} onChange={(e) => setAmount(e.target.value)} />
          <TextField label="Метод" value={method} onChange={(e) => setMethod(e.target.value)} />
          <Button variant="contained" onClick={() => void onCreate()}>Добавить платеж</Button>
        </Stack>
      </Paper>
      <Table>
        <TableHead><TableRow><TableCell>Ребенок</TableCell><TableCell>Сумма</TableCell><TableCell>Дата</TableCell><TableCell>Метод</TableCell></TableRow></TableHead>
        <TableBody>{rows.map((row) => <TableRow key={row.id}><TableCell>{row.student_id}</TableCell><TableCell>{row.amount}</TableCell><TableCell>{row.payment_date}</TableCell><TableCell>{row.method}</TableCell></TableRow>)}</TableBody>
      </Table>
    </Stack>
  )
}
