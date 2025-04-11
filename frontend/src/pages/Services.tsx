const Services = () => {
  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold">Our Services</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-semibold mb-2">Service 1</h3>
          <p className="text-gray-300">Description of service 1 and what it offers to clients.</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-semibold mb-2">Service 2</h3>
          <p className="text-gray-300">Description of service 2 and what it offers to clients.</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-semibold mb-2">Service 3</h3>
          <p className="text-gray-300">Description of service 3 and what it offers to clients.</p>
        </div>
      </div>
    </div>
  );
};

export default Services; 