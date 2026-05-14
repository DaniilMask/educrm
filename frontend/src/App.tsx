import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import AppLayout from './layouts/AppLayout'
import AttendancePage from './pages/AttendancePage'
import DashboardPage from './pages/DashboardPage'
import GroupsPage from './pages/GroupsPage'
import StudentsPage from './pages/StudentsPage'
import ParentsPage from './pages/ParentsPage'
import PaymentsPage from './pages/PaymentsPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="students" element={<StudentsPage />} />
          <Route path="groups" element={<GroupsPage />} />
          <Route path="parents" element={<ParentsPage />} />
          <Route path="attendance" element={<AttendancePage />} />
          <Route path="payments" element={<PaymentsPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
