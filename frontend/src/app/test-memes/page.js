"use client"

import { useState, useEffect, useRef } from 'react';
import Masonry from "react-masonry-css";

function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

export default function Memes() {
    const [memes, setMemes] = useState([]);
    const [pageNumber, setPageNumber] = useState(1);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const endOfPageRef = useRef();

    const breakpointColumnsObj = {
        default: 4,
        768: 3,
        500: 2,
        100: 1
    };

    useEffect(() => {
        const fetchData = async () => {
            if (!hasMore || loading) return;
            setLoading(true);
            try {
                const response = await fetch(`http://localhost:8000/api/memes/?page=${pageNumber}`);
                const data = await response.json();
                if (data.detail === "Invalid page.") {
                    setHasMore(false);
                } else {
                    setMemes(prevMemes => [...prevMemes, ...data.results]);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
            setLoading(false);
        };

        fetchData();
    }, [pageNumber]);

    useEffect(() => {
        const handleScroll = debounce(() => {
            const columns = document.querySelectorAll('.my-masonry-grid_column');
            const minHeight = Math.min(...Array.from(columns).map(column => column.offsetHeight));
            if (endOfPageRef.current && window.innerHeight + window.scrollY >= minHeight - 1000) {
                console.log('reached end');
                if(!loading){
                    console.log('page changes');
                    setPageNumber(prevPageNumber => prevPageNumber + 1);
                }
            }

            // const columns = document.querySelectorAll('.my-masonry-grid_column');
            // let minHeight = Infinity;
            // columns.forEach(column => {
            //     let heightSum = 0;
            //     column.childNodes.forEach(childNode => {
            //         heightSum += childNode.offsetHeight;
            //     });
            //     minHeight = Math.min(minHeight, heightSum);
            // });
            // if (endOfPageRef.current && window.innerHeight + window.scrollY >= minHeight) {
            //     console.log('reached end');
            //     if (!loading) {
            //         console.log('page changes');
            //         setPageNumber(prevPageNumber => prevPageNumber + 1);
            //     }
            // }
        }, 300);

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);


    return (
        <>
            <Masonry
                breakpointCols={breakpointColumnsObj}
                className="my-masonry-grid"
                columnClassName="my-masonry-grid_column h-auto"
            >
                {memes.map((meme, index) => (
                    <img
                        key={meme.id}
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
            </Masonry>
        </>
    );
}
