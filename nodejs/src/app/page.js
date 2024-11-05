"use client"

import { useState } from 'react';
import { Box, Button, Heading, Input } from '@chakra-ui/react';
import Link from 'next/link';
import Image from 'next/image';
import Logo from '../../public/jmclicklogo.png';
import Send from '../../public/send.png';

const HomePage = () => {
  const [message, setMessage] = useState("");

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  const handleSubmit = (messageButton) => {
    const messageToSend = messageButton || message.trim();
    if (messageToSend) {
      localStorage.setItem('chatMessage', messageToSend);
      window.location.href = "/chat";
    }
  };

  const frequentlyAsked = [
    "Bagaimana kalau saya tidak bisa log in JMClick?",
    "Bagaimana jika saya tidak bisa melakukan absensi?",
    "Bagaimana cara update data E-CV?"
  ]

  return (
    <Box
      h="100vh"
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
    >
      <Image src={Logo} width={200} height={200} alt='logo' />
      <Heading size="lg" textAlign={{ base: "center", md: "start" }}>
        Apa yang bisa Bang Jasmar bantu?
      </Heading>

      <Box mt={8} width={{ base: "100%", md: "50%" }} display="flex">
        <Input
          placeholder="Kirim pesan ke Bang Jasmar..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          bg="white"
          borderRadius="md"
          mr={4}
          onKeyDown={handleKeyDown}
        />
        <Button colorScheme="blue" aria-label="send-message" onClick={() => handleSubmit()}>      
          <Image src={Send} width={24} height={24} alt='logo' />
        </Button>
      </Box>

      <Box display="flex" flexWrap="wrap" justifyContent="center" gap={4} mt={8}>
        {frequentlyAsked.map((item, idx) => (
          <Button
            colorScheme="gray"
            variant="outline"
            rounded={"full"}
            key={idx}
            onClick={() => handleSubmit(item)}
            width={{ base: '100%', sm: 'auto' }}
            whiteSpace="normal"  
          >
            {item}
          </Button>
        ))}
      </Box>
      <Box mt={4}>
        <p>atau</p>
      </Box>
      <Link href="/chat">
        <Button mt={4} colorScheme="blue">
          Kirim Pesan Langsung
        </Button>
      </Link>
    </Box>
  );
};

export default HomePage;
