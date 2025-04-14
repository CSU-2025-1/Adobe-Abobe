import React, { useState } from 'react';
import {
  Container,
  TopButtons,
  UploadLabel,
  HiddenInput,
  Button,
  MainContent,
  Sidebar,
  ImageArea,
  ImageWrapper,
  PreviewImage,
  Placeholder,
  SliderWrapper,
  Slider, ArrowForwardButton, ArrowBackButton
} from './styles';
import axios from 'axios';

export default function PhotoUploadPage() {
  const [image, setImage] = useState(null);



  const handleUpload = async (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    setImage(URL.createObjectURL(selectedFile));

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await axios.post('http://localhost:8000/upload/', formData);
      console.log('Изображение успешно загружено');
    } catch (error) {
      console.error('Ошибка при загрузке:', error);
      alert('Ошибка при загрузке изображения');
    }
  };

  const handleSave = () => {
    if (!image) {
      alert('Сначала загрузите изображение.');
    } else {
      window.open('http://localhost:8000/download/last', '_blank');
    }
  };

  return (
    <Container>
      <TopButtons>
        <UploadLabel>
          Загрузить
          <HiddenInput type="file" accept="image/*" onChange={handleUpload} />
        </UploadLabel>
        <ArrowBackButton />
        <ArrowForwardButton />
        <Button onClick={handleSave}>Сохранить</Button>
      </TopButtons>

      <MainContent>
        <Sidebar>Здесь будут пресеты</Sidebar>

        <ImageArea>
          <ImageWrapper>
            {image ? (
              <PreviewImage
                src={image}
                alt="Загруженное изображение"

              />
            ) : (
              <Placeholder>Изображение не загружено</Placeholder>
            )}
          </ImageWrapper>

          <SliderWrapper>
            <Slider
              type="range"
              min="0"
              max="200"

              orient="vertical"
            />
          </SliderWrapper>
        </ImageArea>
      </MainContent>
    </Container>
  );
}
