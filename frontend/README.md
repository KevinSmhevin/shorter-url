# ShortURL Frontend

A modern React frontend for the ShortURL URL shortening service, built with Vite, React Router, and Tailwind CSS.

## Features

- 🚀 Fast and responsive UI built with React and Vite
- 🎨 Modern design with blue/gray/white color scheme
- 📊 Real-time analytics dashboard
- 🔗 URL shortening with custom codes
- 📱 Fully responsive design
- ⚡ Fast page loads with code splitting

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Lucide React** - Icon library
- **date-fns** - Date formatting

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
```

3. Create a `.env` file (optional):
```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

4. Start the development server:
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

The app will be available at `http://localhost:3000`

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable React components
│   │   ├── Layout.jsx
│   │   ├── URLShortener.jsx
│   │   ├── URLList.jsx
│   │   └── AnalyticsChart.jsx
│   ├── contexts/         # React Context providers
│   │   └── URLContext.jsx
│   ├── pages/            # Page components
│   │   ├── Home.jsx
│   │   ├── URLs.jsx
│   │   └── Analytics.jsx
│   ├── services/         # API service layer
│   │   └── api.js
│   ├── App.jsx           # Main app component
│   ├── main.jsx          # Entry point
│   └── index.css         # Global styles
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Features Overview

### Home Page
- URL shortening form with optional custom code and expiration
- Feature highlights
- Copy-to-clipboard functionality

### My URLs Page
- List of all shortened URLs
- Pagination support
- Quick actions (copy, view analytics, deactivate)
- Click count and creation date display

### Analytics Page
- Total clicks and unique visitors
- Clicks by date chart
- Clicks by hour chart
- Top referers list

## API Integration

The frontend communicates with the FastAPI backend through the API service layer (`src/services/api.js`). Make sure the backend is running on `http://localhost:8000` (or configure `VITE_API_BASE_URL`).

## Styling

The app uses Tailwind CSS with a custom color palette:
- Primary: Blue shades (`primary-50` to `primary-900`)
- Gray: Gray shades (`gray-50` to `gray-900`)
- White: Background and card colors

Custom utility classes are defined in `src/index.css`:
- `.btn-primary` - Primary button style
- `.btn-secondary` - Secondary button style
- `.input-field` - Input field style
- `.card` - Card container style

## Building for Production

```bash
npm run build
```

The production build will be in the `dist` directory, ready to be deployed to any static hosting service.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT

