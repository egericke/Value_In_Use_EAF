import './globals.css';

export const metadata = {
  title: 'EAF VIU Tool',
  description: 'Value-in-Use Comparison for EAF Materials',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
