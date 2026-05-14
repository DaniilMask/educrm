import { apiRequest } from './client'

export type Student = {
  id: number
  full_name: string
  phone: string | null
  parent_name: string | null
  parent_phone: string | null
  status: string
  notes: string | null
}

export type StudentCreatePayload = {
  full_name: string
  phone?: string
  parent_name?: string
  parent_phone?: string
  parent_id?: number
  notes?: string
}

export type StudentsSummary = {
  total_children: number
  active_children: number
  inactive_children: number
  start_date: string | null
  end_date: string | null
  group_name: string | null
}


export function getStudents() {
  return apiRequest<Student[]>('/students/')
}

export function getStudentsSummary(params?: {
  startDate?: string
  endDate?: string
  groupName?: string
}) {
  const searchParams = new URLSearchParams()
  if (params?.startDate) {
    searchParams.set('start_date', params.startDate)
  }
  if (params?.endDate) {
    searchParams.set('end_date', params.endDate)
  }
  if (params?.groupName && params.groupName !== 'all') {
    searchParams.set('group_name', params.groupName)
  }

  const query = searchParams.toString()
  const path = query ? `/students/stats/summary?${query}` : '/students/stats/summary'
  return apiRequest<StudentsSummary>(path)
}

export function createStudent(payload: StudentCreatePayload) {
  return apiRequest<Student>('/students/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function deleteStudent(studentId: number) {
  return apiRequest<{ message: string }>(`/students/${studentId}`, {
    method: 'DELETE',
  })
}
