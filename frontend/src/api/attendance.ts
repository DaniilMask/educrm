/**
 * Файл src/api/attendance.ts:
 * Простое описание: этот файл управляет частью интерфейса или запросами к API.
 * Комментарий добавлен для прозрачности структуры фронтенда.
 */

import { apiRequest } from './client'

export type Attendance = {
  id: number
  lesson_id: number
  student_id: number
  status: string
  comment: string | null
}

export function getAttendanceByLesson(lessonId: number) {
  return apiRequest<Attendance[]>(`/attendance/lesson/${lessonId}`)
}

export function upsertAttendance(payload: Omit<Attendance, 'id'>) {
  return apiRequest<Attendance>('/attendance/', { method: 'POST', body: JSON.stringify(payload) })
}
