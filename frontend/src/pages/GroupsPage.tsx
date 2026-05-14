/**
 * Файл src/pages/GroupsPage.tsx:
 * Простое описание: этот файл управляет частью интерфейса или запросами к API.
 * Комментарий добавлен для прозрачности структуры фронтенда.
 */

import { useEffect, useState } from 'react'
import { Alert, Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material'

import { getSections, type Section } from '../api/sections'

export default function GroupsPage() {
  const [rows, setRows] = useState<Section[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getSections().then(setRows).catch((e: Error) => setError(e.message))
  }, [])

  if (error) return <Alert severity="error">{error}</Alert>

  return (
    <Table>
      <TableHead><TableRow><TableCell>Секция</TableCell><TableCell>Филиал</TableCell><TableCell>День</TableCell><TableCell>Время</TableCell></TableRow></TableHead>
      <TableBody>
        {rows.map((row) => <TableRow key={row.id}><TableCell>{row.name}</TableCell><TableCell>{row.branch_id}</TableCell><TableCell>{row.weekday ?? '-'}</TableCell><TableCell>{row.start_time ?? '-'} - {row.end_time ?? '-'}</TableCell></TableRow>)}
      </TableBody>
    </Table>
  )
}
