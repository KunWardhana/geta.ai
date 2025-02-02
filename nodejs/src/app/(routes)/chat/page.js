"use client"

import axios from 'axios';
import { useState, useEffect, useRef } from 'react';
import Image from 'next/image';
import ChatContainer from '../../components/ChatContainer';
import MessageBubble from '../../components/MessageBubble';
import ChatInput from '../../components/ChatInput';
import Logo from '../../../../public/travoylogo.png';

const ChatPage = ({ isSidebarOpen }) => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Halo, selamat datang di Geta. Ada yang bisa saya bantu?", isUser: false },
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
      const response = await axios.post(`${apiUrl}/prompt_llm`, {
        question: message
      });
      const { data } = response;
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: data?.result, isUser: false },
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
      <ChatContainer>
        <Image src={Logo} width={150} height={150} alt='logo' />
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
