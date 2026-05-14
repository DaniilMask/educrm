import { apiRequest } from './client'

export type Payment = {
  id: number
  student_id: number
  amount: string
  payment_date: string
  method: string
  comment: string | null
}

export function getPayments() {
  return apiRequest<Payment[]>('/payments/')
}

export function createPayment(payload: Omit<Payment, 'id'>) {
  return apiRequest<Payment>('/payments/', { method: 'POST', body: JSON.stringify(payload) })
}
