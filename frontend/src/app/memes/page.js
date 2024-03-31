"use client"

import Image from "next/image";
import { useState, useEffect, useRef } from 'react';

export default function Memes() {
    const [memes, setMemes] = useState([]);
    const [pageNumber, setPageNumber] = useState(1);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const endOfPageRef = useRef();

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
                    setMemes([...memes, ...data.results]);
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
                <div className="columns-1 gap-5 sm:gap-8 md:columns-1 lg:columns-1">
                    {memes.map((meme, index) => (
                        <Image key={index} className="mt-8" src={meme.img_url} alt="meme photo" placeholder="blur" blurDataURL="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mN8/PBOPQAIcAMh5LCUAAAAAABJRU5ErkJggg==" width={500} height={500} />
                    ))}
                    {loading && <p>Loading...</p>}
                    <div ref={endOfPageRef} />
                </div>
            </div>
        </>
    );
}
