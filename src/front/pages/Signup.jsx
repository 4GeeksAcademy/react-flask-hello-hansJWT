import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
// Registro de usuario
export const Signup = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const hadleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch(process.env.BACKEND_URL + "/api/signud", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                alert("Usuario registrado correctamente");
                navigate("/login"); // redirigir al login
            } else {
                alert(data.error || "Error al registrarse");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Ocurrio un error");
        }
    };

    return (
        <div className="container mt-5">
            <h1>Registro</h1>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label>Email</label>
                    <input
                        type="email"
                        className="form-control"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary">Registrame</button>
            </form>
        </div>
    );
};
