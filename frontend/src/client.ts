const baseURL = import.meta.env.VITE_CODESPACE_NAME
  ? `https://${import.meta.env.VITE_CODESPACE_NAME}-${import.meta.env.VITE_BACKEND_PORT}.app.github.dev`
  : `http://localhost:${import.meta.env.VITE_BACKEND_PORT}`;

export async function getData<Response>(url: string, params?: URLSearchParams ): Promise<Response> {
  const response = await fetch(`${baseURL}${url}${params ? `?${params.toString()}` : ''}`);
  return response.json();
}

export async function postData<Response>(url: string, data: unknown): Promise<Response | undefined> {
  const response = await fetch(`${baseURL}${url}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (response.status === 204) return;
  return response.json();
}