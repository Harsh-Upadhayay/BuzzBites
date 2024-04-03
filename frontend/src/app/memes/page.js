"use client"

import Image from "next/image";
import { useState, useEffect, useRef } from 'react';

export default function Memes() {
    const [memes, setMemes] = useState([]);
    const [splittedMemes, setSplittedMemes] = useState([]);
    const [pageNumber, setPageNumber] = useState(1);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const endOfPageRef = useRef();

    const splitMemes = (memes) => {
        const columnCount = 3;

        // Dynamically create a list of lists; the length of the list will be columnCount
        var splittedMemes = [];

        // Initialize the inner lists
        for (let i = 0; i < columnCount; i++) {
            splittedMemes.push([]);
        }

        for (let i = 0; i < memes.length; i++) {
            for (let j = 0; j < columnCount; j++) {
                if (memes[i * columnCount + j]) {
                    splittedMemes[j][i] = memes[i * columnCount + j];
                }
            }
        }

        return splittedMemes;
    };

    useEffect(() => {
        setSplittedMemes(splitMemes(memes));
        // Additional logic if needed on component mount
    }, [memes]);

    useEffect(() => {
        const fetchData = async () => {
            if (!hasMore || loading) return; // Stop fetching if there's no more data or already loading
            setLoading(true);
            try {
                const response = await fetch(`http://localhost:8000/api/memes/?page=${pageNumber}`);
                const data = await response.json();
                if (data.detail === "Invalid page.") {
                    setHasMore(false); // Stop fetching if the page is invalid
                } else {
                    setMemes(prevMemes => [...prevMemes, ...data.results]);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
            setLoading(false);
        };

        fetchData();
    }, [pageNumber, hasMore]);

    useEffect(() => {
        const handleScroll = () => {
            if (endOfPageRef.current && window.innerHeight + window.scrollY >= document.body.scrollHeight) {
                setPageNumber(prevPageNumber => prevPageNumber + 1);
            }
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);


    return (
        <>
            <div className="p-5 sm:p-8">
            <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4">
            { splittedMemes.map((memeList, columnIndex) => (
                <div key={columnIndex}  className="grid gap-4">
                    {memeList.map((meme, index) => (
                        <img 
                            key={index}
                            className="mt-8 cursor-pointer h-auto max-w-full rounded-lg" 
                            src={meme.img_url} 
                            alt="meme photo" 
                            placeholder="blur" 
                            blurDataURL="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mN8/PBOPQAIcAMh5LCUAAAAAABJRU5ErkJggg==" 
                            width={500} 
                            height={500} 
                        />
                    ))}
                    <div ref={endOfPageRef} />
                </div>
            ))}
            </div>
            </div>
        </>
    );
}
