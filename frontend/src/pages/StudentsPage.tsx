import { useEffect, useState } from 'react'
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
} from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete'

import {
  createStudent,
  deleteStudent,
  getStudents,
  type Student,
} from '../api/students'

function splitFullName(fullName: string) {
  const parts = fullName.trim().split(/\s+/).filter(Boolean)
  return {
    lastName: parts[0] ?? '',
    firstName: parts[1] ?? '',
    middleName: parts.slice(2).join(' '),
  }
}

export default function StudentsPage() {
  const [rows, setRows] = useState<Student[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [open, setOpen] = useState(false)
  const [lastName, setLastName] = useState('')
  const [firstName, setFirstName] = useState('')
  const [middleName, setMiddleName] = useState('')
  const [parentName, setParentName] = useState('')
  const [newStudentPhone, setNewStudentPhone] = useState('')

  async function loadStudents() {
    setLoading(true)
    setError(null)
    try {
      const data = await getStudents()
      setRows(data)
    } catch (requestError) {
      const message =
        requestError instanceof Error ? requestError.message : 'Не удалось загрузить список детей'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadStudents()
  }, [])

  async function handleCreateStudent() {
    if (!lastName.trim() || !firstName.trim()) {
      setError('Заполните фамилию и имя')
      return
    }

    try {
      const fullName = [lastName.trim(), firstName.trim(), middleName.trim()].filter(Boolean).join(' ')
      const created = await createStudent({
        full_name: fullName,
        parent_name: parentName.trim() || undefined,
        phone: newStudentPhone.trim() || undefined,
      })
      setRows((prev) => [...prev, created])
      setOpen(false)
      setLastName('')
      setFirstName('')
      setMiddleName('')
      setParentName('')
      setNewStudentPhone('')
      setError(null)
    } catch (requestError) {
      const message =
        requestError instanceof Error ? requestError.message : 'Не удалось добавить ребенка'
      setError(message)
    }
  }

  async function handleDeleteStudent(studentId: number) {
    try {
      await deleteStudent(studentId)
      setRows((prev) => prev.filter((student) => student.id !== studentId))
      setError(null)
    } catch (requestError) {
      const message =
        requestError instanceof Error ? requestError.message : 'Не удалось удалить запись'
      setError(message)
    }
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
        <Button variant="contained" onClick={() => setOpen(true)}>
          Добавить ребенка
        </Button>
      </Box>

      {error ? (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      ) : null}

      <TableContainer component={Paper}>
        <Table size="medium" aria-label="children">
          <TableHead>
            <TableRow>
              <TableCell>Фамилия</TableCell>
              <TableCell>Имя</TableCell>
              <TableCell>Отчество</TableCell>
              <TableCell>Родитель</TableCell>
              <TableCell align="right">Действия</TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={5} align="center">
                  <CircularProgress size={24} />
                </TableCell>
              </TableRow>
            ) : rows.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} align="center">
                  Пока нет детей
                </TableCell>
              </TableRow>
            ) : (
              rows.map((row) => {
                const parsedName = splitFullName(row.full_name)
                return (
                  <TableRow key={row.id} hover>
                    <TableCell>{parsedName.lastName || '-'}</TableCell>
                    <TableCell>{parsedName.firstName || '-'}</TableCell>
                    <TableCell>{parsedName.middleName || '-'}</TableCell>
                    <TableCell>{row.parent_name ?? '-'}</TableCell>
                  <TableCell align="right">
                    <IconButton
                      aria-label="удалить ребенка"
                      color="error"
                      onClick={() => {
                        void handleDeleteStudent(row.id)
                      }}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                  </TableRow>
                )
              })
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={() => setOpen(false)} fullWidth maxWidth="sm">
        <DialogTitle>Новый ребенок</DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Фамилия"
            value={lastName}
            onChange={(event) => setLastName(event.target.value)}
            fullWidth
            required
          />
          <TextField
            margin="dense"
            label="Имя"
            value={firstName}
            onChange={(event) => setFirstName(event.target.value)}
            fullWidth
            required
          />
          <TextField
            margin="dense"
            label="Отчество"
            value={middleName}
            onChange={(event) => setMiddleName(event.target.value)}
            fullWidth
          />
          <TextField
            margin="dense"
            label="Родитель"
            value={parentName}
            onChange={(event) => setParentName(event.target.value)}
            fullWidth
          />
          <TextField
            margin="dense"
            label="Телефон"
            value={newStudentPhone}
            onChange={(event) => setNewStudentPhone(event.target.value)}
            fullWidth
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Отмена</Button>
          <Button
            variant="contained"
            onClick={() => {
              void handleCreateStudent()
            }}
          >
            Сохранить
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
