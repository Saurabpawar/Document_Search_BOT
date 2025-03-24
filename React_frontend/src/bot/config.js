import { createChatBotMessage } from 'react-chatbot-kit';
import Avatar from './Avatar.js';
const config = {

  initialMessages: [createChatBotMessage('Welcome to Document Search Bot!🤖 \nAsk any question releated to documents available!\n')],
  botName : "Document Search Bot",
  customComponents : {
     botAvatar : (props)=> <Avatar {...props}/>
  }

};

export default config;