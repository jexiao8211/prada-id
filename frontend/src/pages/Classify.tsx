import { ClassifyImage }from '../components/ClassifyImage';

const Home = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-4">PRADA SEASON CLASSIFIER</h1>
        <p className="text-gray-600 font-mono font-bold">
          find out what season your prada is from
        </p>
      </div>
      
      <ClassifyImage />
    </div>
  );
};

export default Home; 