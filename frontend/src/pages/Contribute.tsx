import { ContributeImage }from '../components/ContributeImage';

const Home = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-4">CONTRIBUTE</h1>
        <p className="text-gray-600 font-mono font-bold">
          upload an image to the database
        </p>
      </div>
      
      <ContributeImage />
    </div>
  );
};

export default Home; 