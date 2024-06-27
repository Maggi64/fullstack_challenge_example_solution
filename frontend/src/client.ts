const baseURL = import.meta.env.VITE_CODESPACE_NAME
  ? `https://${import.meta.env.VITE_CODESPACE_NAME}-${import.meta.env.VITE_BACKEND_PORT}.app.github.dev`
  : `http://localhost:${import.meta.env.VITE_BACKEND_PORT}`;

export async function getData<Response>(url: string): Promise<Response> {
  const response = await fetch(`${baseURL}${url}`);
  return response.json();
}

export async function postData<Response>(url: string, data: unknown): Promise<Response> {
  const response = await fetch(`${baseURL}${url}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return response.json();
}