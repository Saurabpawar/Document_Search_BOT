import React from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';


const ActionProvider = ({ createChatBotMessage, setState, children }) => {

const newMessage = async (msg) => {
  try {
    const response = await searchDocument(msg);
    const reply = createChatBotMessage(response); // You can customize this message
    updateState(reply);
  } catch (error) {
    console.error("Error occurred while creating new message:", error);
  }
  
};

const searchDocument = async (query) => {
  try {
    // const response = await axios.get(`http://localhost:8080/ai/search/${payload}`,{withCredentials:true});
    // return response.data.message;  

    const res = await axios.post(
      "http://localhost:5000/query",
      {  query: query },
      { headers: { "Content-Type": "application/json" }, withCredentials: true }
    );
    return res.data.response
  } catch (error) {
    console.error("Error occurred during the document search:", error);
    toast.error('Fetch error:', error);
    return `Unable to Fetch data! \nPlease try Again later!`
  }
};


  // Function to update the state with the new message
  const updateState = (message) => {
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, message],
    }));
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            newMessage, // Pass the newMessage action to children
          },
        });
      })}
    </div>
  );
};

export default ActionProvider;
