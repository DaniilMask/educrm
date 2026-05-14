# Frontend: прозрачное описание всех частей

## Базовая идея
Frontend показывает страницы CRM и отправляет запросы в backend API.

## Файлы верхнего уровня
- `package.json` — команды запуска и список npm-зависимостей.
- `vite.config.ts` — настройки сборщика Vite.
- `tsconfig*.json` — настройки TypeScript.
- `eslint.config.js` — правила проверки кода.
- `index.html` — HTML-шаблон, куда монтируется React.

## Папка `src/`
- `main.tsx` — стартовая точка React-приложения.
- `App.tsx` — корневой компонент.
- `layouts/AppLayout.tsx` — общий каркас страниц (меню/контент).

## Папка `src/pages/`
- `DashboardPage.tsx` — главная страница с общей информацией.
- `StudentsPage.tsx` — работа с учениками.
- `ParentsPage.tsx` — работа с родителями.
- `GroupsPage.tsx` — работа с группами/секциями.
- `AttendancePage.tsx` — учет посещаемости.
- `PaymentsPage.tsx` — учет оплат.

## Папка `src/api/`
Эти файлы выполняют HTTP-запросы к backend:
- `client.ts` — общий HTTP-клиент (база URL, заголовки, токен).
- `students.ts` — запросы по ученикам.
- `parents.ts` — запросы по родителям.
- `sections.ts` — запросы по секциям.
- `attendance.ts` — запросы по посещаемости.
- `lessons.ts` — запросы по урокам.
- `payments.ts` — запросы по оплатам.

## Как запустить frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Что значит важные слова
- **Component** — кусок интерфейса (как LEGO-блок).
- **State** — данные внутри компонента, которые меняются со временем.
- **Props** — данные, которые компонент получает снаружи.
- **API call** — запрос к серверу за данными.
- **Build** — сборка проекта для публикации.
