
const API_BASE_URL =
=======
const API_BASE_URL = 

  import.meta.env.VITE_API_BASE_URL ??
  (import.meta.env.DEV
    ? '/api'
    : `${window.location.protocol}//${window.location.hostname}:8000`)

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

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers ?? undefined)
  headers.set('Content-Type', 'application/json')

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers,
  })

  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    const detail = typeof body?.detail === 'string' ? body.detail : `HTTP ${response.status}`
    throw new Error(detail)
  }

  return response.json() as Promise<T>
}

export function getStudents() {
  return request<Student[]>('/students/')
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
  return request<StudentsSummary>(path)
}

export function createStudent(payload: StudentCreatePayload) {
  return request<Student>('/students/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function deleteStudent(studentId: number) {
  return request<{ message: string }>(`/students/${studentId}`, {
    method: 'DELETE',
  })
}
