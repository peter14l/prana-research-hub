import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'PRANA Research Hub | Kolkata–Howrah Air Quality Intelligence',
  description: 'Internal environmental intelligence platform for outdoor air pollution research across Kolkata and Howrah.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0C0F14] text-[#F3F4F6] min-h-screen antialiased selection:bg-prana-yellow selection:text-black">
        {children}
      </body>
    </html>
  );
}
