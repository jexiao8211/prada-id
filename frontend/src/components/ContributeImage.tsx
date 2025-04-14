import { useState, useCallback } from 'react';
import { imageApi } from '../utils/api';

interface ClassificationResult {
  category: string;
  season?: string;
  year?: string;
  confidence: number;
}

export const ContributeImage = () => {
  // State management using React hooks
  const [selectedFile, setSelectedFile] = useState<File | null>(null);  // Stores the selected image file
  const [preview, setPreview] = useState<string>('');  // Stores the preview URL of the selected image
  const [loading, setLoading] = useState(false);  // Tracks upload/processing state

  const [selectedSeason, setSelectedSeason] = useState<string>('');
  const [selectedYear, setSelectedYear] = useState<string>('');
  const [error, setError] = useState<string>('');  // Stores any error messages

  // Handle when a user selects a file
  const handleFileSelect = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setError('');

    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please select an image file');
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError('Image size should be less than 5MB');
      return;
    }

    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
  }, []);

  const handleRemoveImage = useCallback(() => {
    setSelectedFile(null);
    setPreview('');
    setError('');
  }, []);

  // Handle when the user clicks the upload button
  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }
    if (!selectedSeason) {
      setError('Please select a season first');
      return;
    }
    if (!selectedYear) {
      setError('Please select a year first');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const seasonYear = `${selectedSeason} ${selectedYear}`;
      const response = await imageApi.contributeImage(selectedFile, seasonYear);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to upload image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleYearChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedYear(event.target.value);
  };

  const handleSeasonChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedSeason(event.target.value);
  };

  // UI elements for image upload
  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
      <div className="space-y-6">
        {/* File Input or Preview Section */}
        {!selectedFile ? (
          <div className="flex flex-col items-center">
            <label 
              htmlFor="image-upload"
              className="w-full h-32 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center cursor-pointer hover:border-gray-400 transition-colors"
            >
              <div className="text-center">
                <p className="text-gray-600">Click to upload a Prada item image</p>
                <p className="text-sm text-gray-400">PNG, JPG up to 5MB</p>
              </div>
              <input
                id="image-upload"
                type="file"
                className="hidden"
                accept="image/*"
                onChange={handleFileSelect}
              />
            </label>            
          </div>
        ) : (
          <div className="relative">
            <button
              onClick={handleRemoveImage}
              className="absolute -top-2 -right-2 bg-gray-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
              aria-label="Remove image"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
            <img
              src={preview}
              alt="Preview"
              className="w-full h-48 object-contain rounded-lg"
            />
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="p-3 bg-red-50 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        )}

        {/* Upload Button - Only show when image is selected */}
        {selectedFile && (
          <button
            onClick={handleUpload}
            disabled={loading}
            className={`w-full py-2 px-4 rounded-lg text-white font-medium ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            {loading ? `Uploading ${selectedSeason} ${selectedYear}...` : 'Upload Image'}
          </button>
        )}
      </div>

      {/* Season and Year Selectors */}
      <div className="flex justify-between w-full mt-4">
        <select value={selectedSeason} onChange={handleSeasonChange} required>
          <option value="">select season</option>
          <option value="SS">Spring/Summer</option>
          <option value="AW">Autumn/Winter</option>
        </select>

        <select value={selectedYear} onChange={handleYearChange} required>
          <option value="">select year</option>
          <option value="1999">1999</option>
          <option value="2000">2000</option>
          <option value="2001">2001</option>
          {/* Add more years as needed */}
        </select>
      </div>

    </div>
  );
}; 