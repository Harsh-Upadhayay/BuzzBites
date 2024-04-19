"use client";
import React, { useState, useEffect, useRef } from "react";
import { Accordion, AccordionItem } from "@nextui-org/react";
import { RadioGroup, Radio } from "@nextui-org/react";

function convertTimeToReadableDate(timeString) {
  const date = new Date(timeString);
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  return date.toLocaleString('en-US', options);
};

const getActualSource = (sourceName) => {
  if (sourceName === "CB") return "Cricbuzz";
  else if (sourceName === "HT") return "Hindustan Times";
  else return "Unknown";
};

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
          // Initialize the selected radio value for each item to 'desc'
          const updatedNews = data.results.map(item => ({ ...item, selectedRadio: 'summary_en' }));
          setNews((prevNews) => [...prevNews, ...updatedNews]);
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

  const handleRadioChange = (e, index) => {
    const { value } = e.target;
    setNews(prevNews => {
      const updatedNews = [...prevNews];
      updatedNews[index].selectedRadio = value;
      return updatedNews;
    });
  };

  return (
    <div className="">
      <Accordion variant="splitted" selectionMode="multiple" className="">
        {news.map((item, index) => (
          <AccordionItem
            key={item.id}
            aria-label={`Accordion ${item.id}`}
            title={item.title}
            subtitle={
                <div
                    dangerouslySetInnerHTML={{
                        __html: `Published : ${convertTimeToReadableDate(item.published_at)}<br>Source : ${getActualSource(
                            item.source
                        )}`,
                    }}
                />
            }
        >
            <RadioGroup
                className="mb-3"
                orientation="horizontal"
                color="warning"
                value={item.selectedRadio}
                onChange={(e) => handleRadioChange(e, index)}
            >
                <Radio value="summary_en">Read in English</Radio>
                <Radio value="summary_hi">Read in Hindi</Radio>
            </RadioGroup>
            {item.selectedRadio === 'summary_en' && <p className="font-normal text-gray-900 dark:text-gray-400">{item.summary}</p>}
            {item.selectedRadio === 'summary_hi' && <p className="font-normal text-gray-900 dark:text-gray-400">{item.summary_hindi}</p>}
        </AccordionItem>
        ))}
      </Accordion>
      {loading && <p>Loading...</p>}
      {!loading && !hasMore && <p>End of News List</p>}
    </div>
  );
}
