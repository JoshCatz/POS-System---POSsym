# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

# POSsym — Frontend

React-based frontend for the POSsym restaurant POS system. Built with Vite for fast development and optimized production builds.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| React | UI framework |
| Vite | Build tool and dev server |
| React Router | Portal routing and navigation |
| Axios | HTTP requests to FastAPI backend |
| Zustand | Lightweight state management |

---

## Getting Started

### Prerequisites
- Node.js 18+
- Backend running via Docker (`docker compose up` from project root)

### Install and Run
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173`

---

## Project Structure

```
/frontend/src
  /portals
    /employee             ← Employee portal (schedule, pay stubs, profile)
    /restaurant           ← Restaurant portal (floor, orders, menu)
  /components             ← Shared UI components
  /services               ← Axios API call functions
  /stores                 ← Zustand state stores
  App.jsx                 ← Top level routing
  main.jsx                ← Entry point
```

---

## The Two Portals

### Employee Portal `/employee/*`
Accessed from home, phone, or any browser. Employees log in with their employee ID and password to view:
- Personal schedule
- Pay stubs and tip history
- Profile and settings

### Restaurant Portal `/restaurant/*`
Accessed from ELO tablets in the restaurant. Employees log in with their employee ID and PIN for fast access to:
- Floor map and table management
- Order taking and management
- Menu browsing
- Payment processing

---

## Connecting to the Backend

All API calls go through `src/services/api.js` which points to the FastAPI backend at `http://localhost:8000` in development. The base URL will be updated to the production AWS endpoint when deployed.

JWT tokens are stored in Zustand state via `src/stores/authStore.js` and automatically attached to every request via an Axios interceptor.

---

## Current State

```
[✔] Vite + React initialized
[✔] React Router, Axios, Zustand installed
[✔] Folder structure established
[ ] API service layer
[ ] Auth store
[ ] Portal routing
[ ] Login pages
[ ] Restaurant menu browser (first real data connection)
[ ] Floor map
[ ] Order management
[ ] Payment flow
[ ] Employee portal pages
```

---

## Next Steps

The immediate build priority is establishing the foundation that everything else plugs into:

1. **`src/services/api.js`** — Axios instance with base URL and JWT interceptor
2. **`src/stores/authStore.js`** — Zustand store managing token, employee info, and login/logout
3. **`src/App.jsx`** — React Router splitting traffic between employee and restaurant portals
4. **Login pages** — Both portals need login UI connected to `/auth/login/pos` and `/auth/login/portal`
5. **Restaurant menu page** — First page connected to real data via `GET /menu`

Once the foundation is in place, the restaurant portal builds out in this order:
```
Floor map → Table view → Order taking → Payment → Kitchen display
```

The employee portal builds in parallel:
```
Dashboard → Schedule → Pay stubs → Profile
```

---

## Development Notes

- The backend must be running for API calls to work
- Seed data script available: `docker compose exec api python seed.py`
- API documentation available at `http://localhost:8000/docs`
- Both portals share the same React app — routing determines which portal loads