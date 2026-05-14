/**
 * Файл src/api/client.ts:
 * Простое описание: этот файл управляет частью интерфейса или запросами к API.
 * Комментарий добавлен для прозрачности структуры фронтенда.
 */

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  (import.meta.env.DEV
    ? '/api'
    : `${window.location.protocol}//${window.location.hostname}:8000`)

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
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
