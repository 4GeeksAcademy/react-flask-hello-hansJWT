import React, { useEffect, useState } from "react";

export const Private = () => {
  const [mensaje, setMensaje] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      setMensaje("No estas autenticado. Por favor inicia sesion.");
      return;
    }
    fetch(import.meta.env.VITE_BACKEND_URL + "/api/private", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.msg) setMensaje(data.msg);
        else setMensaje(data.error || "Token invalido");
      })
      .catch(() => {
        setMensaje("Error al conectar con el servidor.");
      });
  }, []);

  return (
    <div className="container mt-5">
      <h1>Area Privada</h1>
      <p>{mensaje}</p>
    </div>
  );
};
