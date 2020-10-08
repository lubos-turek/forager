import React, { useState, useEffect } from "react";
import styled from "styled-components";

const Image = styled.img`
  margin-top: 10px;
  margin-right: 10px;
  object-fit: contain;
  box-shadow: 0 2px 3px -1px rgba(0,0,0,0.5);
  cursor: pointer;
  transition: background 0.2s ease, opacity 0.2s ease;
  &:hover {
    background: white;
    opacity: 0.7;
    mix-blend-mode: multiply;
  }
`;

const Grid = styled.div`
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  height: 100%;
  overflow-y: scroll;
  justify-content: space-evenly;
`;

const ImageGrid = ({
  datasetName,
  onImageClick,
  imageHeight
}) => {
  const imagesUrl = "http://127.0.0.1:8000/api/get_results/" + datasetName;
  // const [loading, setLoading] = useState(false);
  const [images, setImages] = useState([]);

  useEffect(() => {
    const fetchImages = async () => {
      // setLoading(true)
      const newImages = await fetch(imagesUrl).then(results => results.json());
      setImages(newImages);
      // setLoading(false);
    }
    
    fetchImages()
  }, [imagesUrl, setImages])

  return (<Grid id="image_grid">
    {images.map(img => <Image key={img.idx} style={{height: imageHeight + 'px'}} className="grid_item" src={img.path} onClick={() => onImageClick(img.idx)} />)}
  </Grid>);
}

export default ImageGrid;