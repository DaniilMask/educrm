/**
 * Файл src/api/sections.ts:
 * Простое описание: этот файл управляет частью интерфейса или запросами к API.
 * Комментарий добавлен для прозрачности структуры фронтенда.
 */

import { apiRequest } from './client'

export type Section = {
  id: number
  name: string
  branch_id: number
  teacher_id: number | null
  substitute_teacher_id: number | null
  start_date: string | null
  weekday: string | null
  start_time: string | null
  end_time: string | null
}

export function getSections() {
  return apiRequest<Section[]>('/sections/')
}
