"use client"

import axios from 'axios';
import { useState, useEffect, useRef } from 'react';
import Image from 'next/image';
import ChatContainer from '../../components/ChatContainer';
import MessageBubble from '../../components/MessageBubble';
import ChatInput from '../../components/ChatInput';
import Logo from '../../../../public/jmclicklogo.png';

const ChatPage = ({ isSidebarOpen }) => {
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Halo, selamat datang di Bang Jasmar. Ada yang bisa saya bantu?", isUser: false },
  ]);
  const chatEndRef = useRef(null);

  const handleSend = (message) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: message, isUser: true },
    ]);
    getResponseMessage(message);
  };

  const getResponseMessage = async (message) => {
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:5001/test_mysql', {
        question: message
      });
      const { data } = response;
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: data, isUser: false },
      ]);
    } catch (error) {
      console.error('Error fetching data:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: 'Maaf kami belum bisa menjawabnya :(', isUser: false },
      ]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    const storedMessage = localStorage.getItem('chatMessage');
    if (storedMessage) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: storedMessage, isUser: true },
      ]);
      getResponseMessage(storedMessage);
      localStorage.removeItem('chatMessage');
    }
  }, []);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading]);

  return (
    <div style={{
      height: 'calc(100vh - 4rem)',
      display: 'flex', 
      flexDirection: 'column',
      marginTop: '4rem',
    }}>
      <Image src={Logo} width={180} height={180} alt='logo' />
      <ChatContainer>
        {messages.map((msg, index) => (
          <MessageBubble
            key={index}
            message={msg.text} 
            isUser={msg.isUser}
          />
        ))}
        {loading && (
          <MessageBubble 
            message="" 
            isLoading={loading}
            isUser={false}
          />
        )}
        <div ref={chatEndRef} />
      </ChatContainer>
      <ChatInput
        onSend={handleSend}
        isSidebarOpen={isSidebarOpen}
      />
    </div>
  );
};

export default ChatPage;
