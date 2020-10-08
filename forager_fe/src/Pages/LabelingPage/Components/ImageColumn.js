import React, { useState, useEffect } from "react";
import styled from "styled-components";

const Image = styled.img`
  margin-top: 10px;
  width: 100%;
  box-shadow: 0 2px 3px -1px rgba(0,0,0,0.5);
  cursor: pointer;
  transition: background 0.2s ease, opacity 0.2s ease;
  &:hover {
    background: white;
    opacity: 0.7;
    mix-blend-mode: multiply;
  }
`;

const Column = styled.div`
  width: 200px;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow-y: scroll;
  box-shadow: 0 2px 3px -3px rgba(0,0,0,0.5);

  img:first-child {
      margin-top: 0;
  }
`;

const ImageColumn = ({ datasetName, imagePaths, onImageClick }) => {
  // const imagesUrl = "https://127.0.0.1:8000/api/get_results/" + datasetName;
  // const [loading, setLoading] = useState(false);
  // const [images, setImages] = useState(images);

  // useEffect(() => {
  //   const fetchImages = async () => {
  //     // setLoading(true)
  //     const newImages = await fetch(imagesUrl, {credentials: 'include'}).then(results => results.json());
  //     setImages(newImages);
  //     // setLoading(false);
  //   }
  //   fetchImages()
  // }, [imagesUrl, setImages])

  // if (loading) {
  //     // return spinner
  // }

  return (
    <Column>
      {imagePaths.map((path, idx) => <Image key={idx} src={path} onClick={() => onImageClick(idx)} />)}
    </Column>
  );
}

export default ImageColumn;
