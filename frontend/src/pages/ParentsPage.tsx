import { useEffect, useState } from 'react'
import { Alert, Box, Button, Paper, Stack, Table, TableBody, TableCell, TableHead, TableRow, TextField } from '@mui/material'

import { createParent, getParents, type Parent } from '../api/parents'

export default function ParentsPage() {
  const [rows, setRows] = useState<Parent[]>([])
  const [error, setError] = useState<string | null>(null)
  const [fullName, setFullName] = useState('')
  const [phone, setPhone] = useState('')

  useEffect(() => {
    getParents().then(setRows).catch((e: Error) => setError(e.message))
  }, [])

  async function onCreate() {
    const created = await createParent({ full_name: fullName, phone, student_ids: [] })
    setRows((prev) => [...prev, created])
    setFullName('')
    setPhone('')
  }

  return (
    <Stack spacing={2}>
      {error ? <Alert severity="error">{error}</Alert> : null}
      <Paper variant="outlined" sx={{ p: 2 }}>
        <Stack direction="row" spacing={2}>
          <TextField label="ФИО" value={fullName} onChange={(e) => setFullName(e.target.value)} />
          <TextField label="Телефон" value={phone} onChange={(e) => setPhone(e.target.value)} />
          <Button variant="contained" onClick={() => void onCreate()}>Добавить родителя</Button>
        </Stack>
      </Paper>
      <Box>
        <Table>
          <TableHead><TableRow><TableCell>ФИО</TableCell><TableCell>Телефон</TableCell><TableCell>Дети (ID)</TableCell></TableRow></TableHead>
          <TableBody>
            {rows.map((row) => <TableRow key={row.id}><TableCell>{row.full_name}</TableCell><TableCell>{row.phone}</TableCell><TableCell>{row.student_ids.join(', ') || '-'}</TableCell></TableRow>)}
          </TableBody>
        </Table>
      </Box>
    </Stack>
  )
}
