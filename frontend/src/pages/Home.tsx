const Home = () => {
  return (
    <div className="space-y-8">
      <div className="text-center py-12">
        <h2 className="text-4xl font-bold mb-4">Welcome to Prada ID</h2>
        <p className="text-xl text-gray-300 max-w-2xl mx-auto">
          Your trusted partner for digital identity solutions. We provide secure, reliable, and user-friendly services.
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-2xl font-semibold mb-4">Our Mission</h3>
          <p className="text-gray-300">
            To provide secure and reliable digital identity solutions that empower individuals and organizations.
          </p>
        </div>
        
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-2xl font-semibold mb-4">Our Vision</h3>
          <p className="text-gray-300">
            To be the leading provider of digital identity solutions, trusted by millions worldwide.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home; 