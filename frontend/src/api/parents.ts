import { apiRequest } from './client'

export type Parent = {
  id: number
  full_name: string
  phone: string
  student_ids: number[]
}

export function getParents() {
  return apiRequest<Parent[]>('/parents/')
}

export function createParent(payload: { full_name: string; phone: string; student_ids: number[] }) {
  return apiRequest<Parent>('/parents/', { method: 'POST', body: JSON.stringify(payload) })
}
