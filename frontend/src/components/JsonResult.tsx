import React from 'react';

interface JsonResultProps {
  data: any;
}

export const JsonResult: React.FC<JsonResultProps> = ({ data }) => {
  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold mb-2">Analysis Result:</h3>
      <pre className="bg-gray-100 p-4 rounded-lg overflow-auto max-h-96 text-sm">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
};

// Made with Bob
