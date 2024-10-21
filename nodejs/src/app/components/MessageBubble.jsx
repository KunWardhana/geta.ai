"use client"

import { Box, Text, keyframes } from '@chakra-ui/react';
// import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const dotAnimation = keyframes`
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(0.5); opacity: 0.5; }
  100% { transform: scale(1); opacity: 1; }
`;

const MessageBubble = ({ message, isUser, isLoading }) => {
  // const data = [
  //   {
  //     "name": "Page A",
  //     "uv": 4000,
  //     "pv": 2400
  //   },
  //   {
  //     "name": "Page B",
  //     "uv": 3000,
  //     "pv": 1398
  //   },
  //   {
  //     "name": "Page C",
  //     "uv": 2000,
  //     "pv": 9800
  //   },
  //   {
  //     "name": "Page D",
  //     "uv": 2780,
  //     "pv": 3908
  //   },
  //   {
  //     "name": "Page E",
  //     "uv": 1890,
  //     "pv": 4800
  //   },
  //   {
  //     "name": "Page F",
  //     "uv": 2390,
  //     "pv": 3800
  //   },
  //   {
  //     "name": "Page G",
  //     "uv": 3490,
  //     "pv": 4300
  //   }
  // ]

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
        animation={`${dotAnimation} 0.6s ease-in-out infinite`}
      />
      <Box
        width="8px"
        height="8px"
        bg="gray.500"
        borderRadius="50%"
        animation={`${dotAnimation} 0.6s ease-in-out infinite`}
      />
    </Box>
  );

  return (
    <Box
      alignSelf={isUser ? 'flex-end' : 'flex-start'}
      maxWidth="75%"
    >
      <Box
        bg={isUser ? 'blue.500' : 'gray.200'}
        color={isUser ? 'white' : 'black'}
        borderRadius="lg"
        px={4}
        py={2}
        width="fit-content"
      >
        {isLoading ? (
          <DotLoader />
        ) : (
          <Text style={{ whiteSpace: "pre-line" }}>
            {message}
          </Text>
        )}
      </Box>
      {/* <div style={{ marginTop: "24px" }}>
        {(message.includes('barchart') && isUser == false) ? (
          <BarChart width={500} height={250} data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="pv" fill="#8884d8" />
            <Bar dataKey="uv" fill="#82ca9d" />
          </BarChart>
        ) : (<></>)}
        {(message.includes('linechart') && isUser == false) ? (
          <LineChart width={500} height={250} data={data}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="pv" stroke="#8884d8" />
            <Line type="monotone" dataKey="uv" stroke="#82ca9d" />
          </LineChart>
        ) : (<></>)}
      </div> */}
    </Box>
  );
};

export default MessageBubble;
