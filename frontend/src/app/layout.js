import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Header from "./components/Header";
import { ThemeModeScript } from "flowbite-react";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
    <head>
      </head>
      <body className={inter.className}>
        <div className="antialiased bg-gray-50 dark:bg-gray-900">
          <Navbar />
          <Sidebar />
          <main className="p-4 md:ml-64 h-auto pt-20">
            {children}
          </main>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js"></script>
      </body>
    </html>
  );
}
