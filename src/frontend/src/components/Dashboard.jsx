import React from "react";
import { motion } from "framer-motion";

export default function Dashboard({handleReset}) {
    return (
        <motion.div
            className="bg-white rounded-2xl shadow-md p-6 w-full max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
        >
            <div className="dashboard-page">
                <h2 className="mb-4 text-center">
                    Análisis de Emprendimientos Universitarios
                </h2>

                <div className="mb-4 shadow-sm">
                    <iframe
                        width="100%"
                        height="600"
                        src="https://lookerstudio.google.com/embed/reporting/ed1b7c4e-92f7-4439-81ea-196f1e7573f7/page/39XHF"
                        frameBorder="0"
                        style={{
                            border: "0",
                            borderRadius: "0.5rem",
                            boxShadow: "0 0px 12px rgba(0, 0, 0, 0.5)"
                        }}
                        allowFullScreen
                        sandbox="allow-storage-access-by-user-activation allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"
                    ></iframe>
                </div>
                <br />
                <div className="text-center">
                    <button
                        className="btn btn-primary"
                        onClick={handleReset}
                    >
                        Volver al Inicio
                    </button>
                </div>
            </div>
        </motion.div>
    );
}
