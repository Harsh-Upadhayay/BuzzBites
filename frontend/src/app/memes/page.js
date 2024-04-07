"use client"

import { useState, useEffect, useRef } from 'react';
import Masonry from "react-masonry-css";
import { Image } from "@nextui-org/react";

function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

function ImageModal({ src, alt, onClose }) {
    return (
        <div className="fixed inset-0 flex justify-center items-center z-50">
            <div className="absolute inset-0 bg-gray-800 bg-opacity-50" onClick={onClose}></div>
            <div className="relative m-2">
                <button className="absolute top-0 right-0 m-4 text-white" onClick={onClose}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                </button>
                <img src={src} alt={alt} className="max-w-screen max-h-svh" />
            </div>
        </div>
    );
}

export default function Memes() {
    const [modalOpen, setModalOpen] = useState(false);
    const [selectedImage, setSelectedImage] = useState('');

    const openModal = (imageSrc) => {
        setSelectedImage(imageSrc);
        setModalOpen(true);
    };

    const closeModal = () => {
        setSelectedImage('');
        setModalOpen(false);
    };

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
                if (!loading) {
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
                    <Image
                        key={meme.id}
                        className="mt-2 cursor-pointer h-auto max-w-full rounded-lg"
                        src={meme.img_url}
                        alt={meme.local_path}
                        placeholder="blur"
                        blurDataURL="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mN8/PBOPQAIcAMh5LCUAAAAAABJRU5ErkJggg=="
                        width={500}
                        height={500}
                        onClick={() => openModal(meme.img_url)}
                    />
                ))}
                <div ref={endOfPageRef} />
            </Masonry>
            {/* Render modal if modalOpen is true */}
            {modalOpen && (
                <ImageModal src={selectedImage} alt="Meme" onClose={closeModal} />
            )}
        </>
    );
}
