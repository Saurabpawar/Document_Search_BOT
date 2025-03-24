import React from 'react';

import Chatbot from 'react-chatbot-kit'
import './css/Chat.css';
import 'react-chatbot-kit/build/main.css'
import config from './bot/config.js';
import MessageParser from './bot/MessageParser.js';
import ActionProvider from './bot/ActionProvider.js';


const Chat = () => {
  return (
    <div className="container">
        {/* <div style={{ order: '1px solid #ccc' }}> */}
          {/* Chat bot iframe or component can be placed here */}
          
          <div >
            <Chatbot
              config={config}
              messageParser={MessageParser}
              actionProvider={ActionProvider}
            />
          </div>



        </div>
  //  </div>
  );
};

export default Chat;
