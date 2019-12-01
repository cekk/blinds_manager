import React from "react";
import { SimpleGrid } from "@chakra-ui/core";
import BlindItem from "./BlindItem";

function BlindsList({ blinds }) {
  return (
    <React.Fragment>
      <SimpleGrid columns={3} spacing={10} m="1em">
        {blinds.map(blind => (
          <BlindItem key={blind.id} {...blind}></BlindItem>
        ))}
      </SimpleGrid>
      <BlindItem
        key="all"
        id="all"
        name="All"
        online={true}
        m="10px"
      ></BlindItem>
    </React.Fragment>
  );
}

export default BlindsList;
