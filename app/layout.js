import './globals.css';

export const metadata = {
  title: 'EAF VIU Tool',
  description: 'Hybrid App for EAF Material Comparison',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
