'use client'
import React from "react";
import { Accordion, AccordionItem, Avatar } from "@nextui-org/react";
import { Divider } from "@nextui-org/react";
import { Button, Card } from "flowbite-react";

export default function App() {
  const defaultContent =
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.";

  return (
    <Accordion variant="splitted">
      <AccordionItem key="1" aria-label="Accordion 1" title="Noteworthy technology acquisitions 2021" subtitle="Published : Today | Source: Hindustan Times"
      >
        <p className="font-normal text-gray-900 dark:text-gray-400">
          Here are the biggest enterprise technology acquisitions of 2021 so far, in reverse chronological order.
        </p>
      </AccordionItem>
      <AccordionItem key="2" aria-label="Accordion 2" title="Noteworthy technology acquisitions 2021">
        <Card href="#" className="max-w">
          <p className="font-normal text-gray-700 dark:text-gray-400">
            Here are the biggest enterprise technology acquisitions of 2021 so far, in reverse chronological order.
          </p>
        </Card>
      </AccordionItem>
      <AccordionItem key="3" aria-label="Accordion 3" title="Noteworthy technology acquisitions 2021">
        <Card href="#" className="max-w">
          <p className="font-normal text-gray-700 dark:text-gray-400">
            Here are the biggest enterprise technology acquisitions of 2021 so far, in reverse chronological order.
          </p>
        </Card>
      </AccordionItem>
    </Accordion>
  );
}
