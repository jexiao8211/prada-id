const About = () => {
  return (
    <div className="space-y-8">
      <div className="text-center py-8">
        <h2 className="text-3xl font-bold mb-4">About Us</h2>
        <p className="text-xl text-gray-300 max-w-3xl mx-auto">
          Learn more about our company, our values, and our commitment to providing the best digital identity solutions.
        </p>
      </div>
      
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h3 className="text-2xl font-semibold mb-4">Our Story</h3>
        <p className="text-gray-300 mb-4">
          Founded in 2020, Prada ID has been at the forefront of digital identity innovation. We started with a simple mission: 
          to make digital identity management secure, simple, and accessible to everyone.
        </p>
        <p className="text-gray-300">
          Today, we serve thousands of clients worldwide, from individuals to large enterprises, providing them with 
          cutting-edge solutions for their digital identity needs.
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-semibold mb-2">Security</h3>
          <p className="text-gray-300">We prioritize security in everything we do, ensuring your data is protected.</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-semibold mb-2">Innovation</h3>
          <p className="text-gray-300">We constantly innovate to provide the best solutions for our clients.</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-semibold mb-2">Customer Focus</h3>
          <p className="text-gray-300">Our customers are at the center of everything we do.</p>
        </div>
      </div>
    </div>
  );
};

export default About; 