import React from "react";
import { SimpleGrid, Box } from "@chakra-ui/core";
import BlindItem from "./BlindItem";

function BlindsList({ blinds }) {
  return (
    <Box bg="gray.100">
      <SimpleGrid columns={{ sm: 1, md: 2, lg: 3 }} m="1em">
        {blinds.map(blind => (
          <BlindItem key={blind.id} {...blind}></BlindItem>
        ))}
      </SimpleGrid>
      <Box m={4} pb={4}>
        <BlindItem
          key="all"
          id="all"
          name="All"
          online={true}
          m="10px"
        ></BlindItem>
      </Box>
    </Box>
  );
}

export default BlindsList;
