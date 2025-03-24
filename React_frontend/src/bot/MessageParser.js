import React from 'react';

const MessageParser = ({ children, actions }) => {
  // Function to parse the incoming message
  const parse = (message) => {
    console.log(message); // Log the message
    actions.newMessage(message); // Trigger the action to create a new message
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          parse: parse, // Pass the parse function to children
          actions, // Pass actions to children
        });
      })}
    </div>
  );
};

export default MessageParser;
