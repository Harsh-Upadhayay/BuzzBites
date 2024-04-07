"use client";
import React, { useState, useEffect, useRef } from "react";
import { Accordion, AccordionItem } from "@nextui-org/react";

export default function App() {
  const [news, setNews] = useState([]);
  const [pageNumber, setPageNumber] = useState(1);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  const observer = useRef();

  useEffect(() => {
    const fetchData = async () => {
      if (!hasMore || loading) return;
      setLoading(true);
      try {
        const response = await fetch(
          `http://localhost:8000/api/news/?page=${pageNumber}`
        );
        const data = await response.json();
        if (data.detail === "Invalid page.") {
          setHasMore(false);
        } else {
          setNews((prevNews) => [...prevNews, ...data.results]);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
      setLoading(false);
    };

    fetchData();
  }, [pageNumber]);

  useEffect(() => {
    const handleScroll = () => {
      const bottom =
        Math.ceil(window.innerHeight + window.scrollY) >=
        document.documentElement.scrollHeight;

      if (bottom && !loading) {
        setPageNumber((prevPageNumber) => prevPageNumber + 1);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, [loading]);

  function convertTimeToReadableDate(timeString) {
    const date = new Date(timeString);
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleString('en-US', options);
  }

  const get_actual_source = (source_name) => {
    if (source_name === "CB") return "Cricbuzz";
    else if (source_name === "HT") return "Hindustan Times";
    else return "Unknown";
  };

  return (
    <div className="">
      <Accordion variant="splitted" className="">
        {news.map((item, index) => (
          <AccordionItem
            key={item.id}
            aria-label={`Accordion ${index + 1}`}
            title={item.title}
            subtitle=<div
            dangerouslySetInnerHTML={{
              __html: `Published : ${convertTimeToReadableDate(item.published_at)}<br>Source : ${get_actual_source(
                item.source
              )}`
            }}
          />
            
          >
            <p className="font-normal text-gray-900 dark:text-gray-400">
              {item.description}
            </p>
          </AccordionItem>
        ))}
      </Accordion>
      {loading && <p>Loading...</p>}
      {!loading && !hasMore && <p>End of News List</p>}
    </div>
  );
}
