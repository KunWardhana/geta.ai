"use client"

import axios from 'axios';
import { useState, useEffect, useRef } from 'react';
import Image from 'next/image';
import ChatContainer from '../../components/ChatContainer';
import MessageBubble from '../../components/MessageBubble';
import ChatInput from '../../components/ChatInput';
import Logo from '../../../../public/geta_logo.png';

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

  const getLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${position.coords.latitude}&lon=${position.coords.longitude}`)
            .then(response => response.json())
            .then(data => {
              const locData = `Tolong carikan rest area terdekat berdasarkan lokasi saya saat ini: ${data.display_name}`;
              setMessages((prevMessages) => [
                ...prevMessages,
                { text: locData, isUser: true },
              ]);
              getResponseMessage(locData)
            })
            .catch(error => console.error("Error:", error));
        },
        (err) => {
          const errorMessage = "⚠️ Gagal mendapatkan lokasi. Periksa izin lokasi di browser Anda.";
          setMessages((prevMessages) => [
            ...prevMessages,
            { text: errorMessage, isUser: false },
          ]);
        }
      );
    } else {
      const unsupportedMessage = "⚠️ Geolocation tidak didukung di browser ini.";
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: unsupportedMessage, isUser: false },
      ]);
    }
  };

  const getResponseMessage = async (message) => {
    setLoading(true);
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: "", isUser: false, isStreaming: true },
    ]);
  
    try {
      const response = await fetch(`${apiUrl}/stream_llm`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: message }),
      });
  
      if (!response.ok || !response.body) {
        throw new Error("Response stream error");
      }
  
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedText = "";
  
      while (true) {
        const { done, value } = await reader.read();
        if (done) {        
          console.log("Streaming complete.");
          break;
        }
  
        const chunk = decoder.decode(value, { stream: true });
        accumulatedText += chunk;
  
        setMessages((prevMessages) => {
          const newMessages = [...prevMessages];
          newMessages[newMessages.length - 1] = {
            ...newMessages[newMessages.length - 1],
            text: accumulatedText,
            isStreaming: true,
            isUser: false
          };
          return newMessages;
        });
      }
  
      setMessages((prevMessages) => {
        const newMessages = [...prevMessages];
        newMessages[newMessages.length - 1] = {
          ...newMessages[newMessages.length - 1],
          isStreaming: false,
          isUser: false
        };
        return newMessages;
      });
  
    } catch (error) {
      console.error("Error fetching data:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: "Maaf kami belum bisa menjawabnya :(", isUser: false },
      ]);
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    let storedMessage = localStorage.getItem('chatMessage');
    if (storedMessage) {

      if (storedMessage.includes("lokasi saat ini")) {
        getLocation();
      } else {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: storedMessage, isUser: true },
        ]);
        getResponseMessage(storedMessage);
      }

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
        <Image src={Logo} width={200} height={80} alt='logo' />
        {messages.map((msg, index) => (
          <MessageBubble
            key={index}
            message={msg.text}
            isUser={msg.isUser}
            isStreaming={index === messages.length - 1 && msg.isStreaming}
          />
        ))}

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
