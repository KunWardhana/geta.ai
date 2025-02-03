"use client";

import { Box, Text } from "@chakra-ui/react";
import { keyframes } from "@emotion/react";
import { useEffect, useState } from "react";

const dotAnimation = keyframes`
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(0.5); opacity: 0.5; }
  100% { transform: scale(1); opacity: 1; }
`;

const MessageBubble = ({ message, isUser, isStreaming }) => {
  const [displayMessage, setDisplayMessage] = useState("");

  useEffect(() => {
    if (isStreaming) {
      setDisplayMessage("");
    } else {
      setDisplayMessage(message);
    }
  }, [message, isStreaming]);

  useEffect(() => {
    if (isStreaming && message) {
      setDisplayMessage((prev) => prev + message); 
    }
  }, [message]);

  const DotLoader = () => (
    <Box display="flex" justifyContent="center" alignItems="center" paddingTop={2} paddingBottom={2} gap={2}>
      <Box
        width="8px"
        height="8px"
        bg="gray.500"
        borderRadius="50%"
        animation={`${dotAnimation} 0.6s ease-in-out infinite`}
      />
      <Box
        width="8px"
        height="8px"
        bg="gray.500"
        borderRadius="50%"
        animation={`${dotAnimation} 0.6s ease-in-out infinite 0.2s`}
      />
      <Box
        width="8px"
        height="8px"
        bg="gray.500"
        borderRadius="50%"
        animation={`${dotAnimation} 0.6s ease-in-out infinite 0.4s`}
      />
    </Box>
  );

  return (
    <Box alignSelf={isUser ? "flex-end" : "flex-start"} maxWidth="75%">
      <Box
        bg={isUser ? "#344879" : "gray.200"}
        color={isUser ? "white" : "black"}
        borderRadius="lg"
        px={4}
        py={2}
        width="fit-content"
      >
        {isStreaming && !displayMessage ? <DotLoader /> : <Text style={{ whiteSpace: "pre-line" }}>{displayMessage}</Text>}
      </Box>
    </Box>
  );
};

export default MessageBubble;
