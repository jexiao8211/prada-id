import { Outlet, Link } from 'react-router-dom';

const MainLayout = () => {
  return (
    <div className="min-h-screen flex flex-col bg-white">

        {/* Top Navigation */}
      <header className="border-b border-gray-200">
        <div className="container mx-auto px-4">
          <div className="flex items-cewnter justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center">
              <h1 className="text-xl font-bold text-black">PRADA ID</h1>
            </Link>

            {/* Navigation Links */}
            <nav className="flex items-center space-x-8">
              <Link to="/" className="text-gray-700 hover:text-black text-sm font-medium">Home</Link>
              <Link to="/classify" className="text-gray-700 hover:text-black text-sm font-medium">Classify</Link>
              <Link to="/contribute" className="text-gray-700 hover:text-black text-sm font-medium">Contribute</Link>
              <Link to="/about" className="text-gray-700 hover:text-black text-sm font-medium">About</Link>
              <Link to="/contact" className="text-gray-700 hover:text-black text-sm font-medium">Contact</Link>
            </nav>
          </div>
        </div>
      </header>
      {/* Main Content */}
      <main className="flex-grow container mx-auto px-4 py-8">
        <Outlet />
      </main>
      
      {/* Footer */}
      <footer className="bg-white-900 text-black p-4 border-t border-gray-800">
        <div className="container mx-auto px-4">
          <p className="text-center">© 2025 Prada ID. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default MainLayout; 