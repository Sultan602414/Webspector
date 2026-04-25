const BASE_URL = '/api'; // Proxied by Vite in dev

export const triggerRun = async (formData) => {
  const response = await fetch(`${BASE_URL}/run`, {
    method: 'POST',
    body: formData, // FormData handles multipart/form-data correctly
  });
  if (!response.ok) {
    throw new Error(`Server error: ${response.status}`);
  }
  return response.json();
};

export const getSessionStatus = async (sessionId) => {
  const response = await fetch(`${BASE_URL}/session/${sessionId}?format=json`);
  if (!response.ok) {
    throw new Error(`Server error: ${response.status}`);
  }
  return response.json();
};
