import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const MainLayout = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col selection:bg-primary-container selection:text-on-primary-container bg-background">
      <Navbar />
      <main className="flex-grow flex flex-col relative overflow-hidden">
        {children}
      </main>
      <Footer />
    </div>
  );
};

export default MainLayout;
