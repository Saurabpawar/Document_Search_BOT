import React, { useState, useEffect, useRef } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import axios from "axios";
import Chatbot from "react-chatbot-kit";
import "react-chatbot-kit/build/main.css";

// Import Chatbot Configuration
import "./css/Chat.css";
import config from "./bot/config";
import MessageParser from "./bot/MessageParser";
import ActionProvider from "./bot/ActionProvider";

// Import Global Styles
import "./css/styles.css";

// Import Login Component
import Login from "./Login"; // Ensure this matches the correct file path

// Sidebar Component
const Sidebar = ({ handleLogout, fetchDocuments, files, handleDelete, handleFileUpload, isUploading, processingFile }) => {
    const role = localStorage.getItem("role");

    return (
        <div className="sidebar">
            <h2 className="sidebar-heading">📂 Document Manager</h2>

            {role === "admin" && (
                <div className="upload-section">
                    <input type="file" id="fileUpload" disabled={isUploading} />
                    <button onClick={handleFileUpload} className="upload-btn" disabled={isUploading}>
                        {isUploading ? "Processing..." : "Upload"}
                    </button>
                </div>
            )}
            <div>
            <h2 style={{ textAlign: "center" }}>Available Documents</h2> 
            <div className="file-list-container">
                <ul className="file-list">
                    {files.length > 0 ? (
                        files.map((file, index) => (
                            <li key={index} className="file-item">
                                <span className="file-name">{file}</span>
                                {role === "admin" && (
                                    <button
                                        className="delete-btn"
                                        onClick={() => handleDelete(file)}
                                        disabled={processingFile === file}
                                    >
                                        {processingFile === file ? "Processing..." : "🗑️"}
                                    </button>
                                )}
                            </li>
                        ))
                    ) : (
                        <li>No documents uploaded yet.</li>
                    )}
                </ul>
            </div>
            </div>

            <button onClick={handleLogout} className="logout-btn">
                Logout
            </button>
        </div>
    );
};

// Dashboard Component
const Dashboard = () => {
    const [files, setFiles] = useState([]);
    const [isUploading, setIsUploading] = useState(false);
    const [processingFile, setProcessingFile] = useState(null);
    const navigate = useNavigate();
    const fileInputRef = useRef(null);

    useEffect(() => {
        fetchDocuments();
    }, []);

    const fetchDocuments = async () => {
        try {
            const res = await axios.get("http://localhost:5000/list_documents", { withCredentials: true });
            setFiles(res.data.documents);
        } catch (error) {
            console.error("Error fetching documents", error);
        }
    };

    const handleFileUpload = async () => {
        const fileInput = document.getElementById("fileUpload");
        const selectedFile = fileInput.files[0];
        if (!selectedFile) return alert("Please select a file to upload.");

        if (selectedFile.size > 2 * 1024 * 1024) {
            alert("File size exceeds the 2MB limit.");
            return;
        }

        setIsUploading(true);
        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            await axios.post("http://localhost:5000/upload", formData, { withCredentials: true });
            fetchDocuments();
            alert("✅ File uploaded successfully!");
        } catch (error) {
            alert(`Error uploading file: ${error.response?.data.error || error.message}`);
        }

        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
        setIsUploading(false);
    };

    const handleDelete = async (filename) => {
        if (!window.confirm(`Are you sure you want to delete ${filename}?`)) return;

        setProcessingFile(filename);
        try {
            await axios.delete(`http://localhost:5000/delete/${filename}`, { withCredentials: true });
            fetchDocuments();
            alert("✅ File deleted successfully!");
        } catch (error) {
            alert(`Error deleting file: ${error.response?.data.error || error.message}`);
        }
        setProcessingFile(null);
    };

    const handleLogout = async () => {
        try {
            await axios.post("http://localhost:5000/logout", {}, { withCredentials: true });
            localStorage.removeItem("isAuthenticated");
            localStorage.removeItem("role");
            navigate("/");
        } catch (error) {
            console.error("Error logging out", error);
        }
    };

    return (
        <div className="dashboard-container">
            <Sidebar
                handleLogout={handleLogout}
                fetchDocuments={fetchDocuments}
                files={files}
                handleDelete={handleDelete}
                handleFileUpload={handleFileUpload}
                isUploading={isUploading}
                processingFile={processingFile}
            />
            <div className="chat-section">
                <h1 className="chat-heading">📄 Document Search Bot</h1>
                
                <Chatbot config={config} messageParser={MessageParser} actionProvider={ActionProvider} />
            </div>
        </div>
    );
};

// Protected Route
const PrivateRoute = ({ children }) => {
    return localStorage.getItem("isAuthenticated") ? children : <Navigate to="/" />;
};

// Main App Component
const DocumentSearchBot = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
            </Routes>
        </Router>
    );
};

export default DocumentSearchBot;
