import { apiRequest } from './client'

export type Lesson = {
  id: number
  section_id: number
  teacher_id: number | null
  replacement_teacher_id: number | null
  date: string
  start_time: string
  end_time: string
  status: string
}

export function getLessons() {
  return apiRequest<Lesson[]>('/lessons/')
}
