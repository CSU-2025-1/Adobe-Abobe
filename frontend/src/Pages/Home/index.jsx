import React, { useState } from 'react';
import {
  Container,
  TopButtons,
  UploadLabel,
  HiddenInput,
  Button,
  MainContent,
  ImageArea,
  ImageWrapper,
  PreviewImage,
  Placeholder,
  SlidersBlock,
  SliderGroup,
  SliderLabel,
  Slider,
  ArrowForwardButton,
  ArrowBackButton,
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
        <ImageArea>
          <ImageWrapper>
            {image ? (
              <PreviewImage src={image} alt="Загруженное изображение" />
            ) : (
              <Placeholder>Изображение не загружено</Placeholder>
            )}
          </ImageWrapper>

          <SlidersBlock>
            <SliderGroup>
              <SliderLabel>Яркость</SliderLabel>
              <Slider type="range" min="0" max="20" orient="horizontal" />
            </SliderGroup>
            <SliderGroup>
              <SliderLabel>Контраст</SliderLabel>
              <Slider type="range" min="0" max="20" orient="horizontal" />
            </SliderGroup>
            <SliderGroup>
              <SliderLabel>Резкость</SliderLabel>
              <Slider type="range" min="0" max="20" orient="horizontal" />
            </SliderGroup>
            <SliderGroup>
              <SliderLabel>Насыщенность цвета</SliderLabel>
              <Slider type="range" min="0" max="20" orient="horizontal" />
            </SliderGroup>
            <SliderGroup>
              <SliderLabel>Размытие</SliderLabel>
              <Slider type="range" min="0" max="20" orient="horizontal" />
            </SliderGroup>
            <SliderGroup>
              <SliderLabel>Гамма-коррекция</SliderLabel>
              <Slider type="range" min="0" max="20" orient="horizontal" />
            </SliderGroup>
            <SliderGroup>
              <SliderLabel>Эффект сепии</SliderLabel>
              <Slider type="range" min="0" max="20" orient="horizontal" />
            </SliderGroup>
            <SliderGroup>
              <SliderLabel>Цветовая температура</SliderLabel>
              <Slider type="range" min="0" max="20" orient="horizontal" />
            </SliderGroup>
            <SliderGroup>
              <SliderLabel>Экспозиция</SliderLabel>
              <Slider type="range" min="0" max="20" orient="horizontal" />
            </SliderGroup>
            <SliderGroup>
              <SliderLabel>Смещение оттенка</SliderLabel>
              <Slider type="range" min="0" max="20" orient="horizontal" />
            </SliderGroup>
          </SlidersBlock>
        </ImageArea>
      </MainContent>
    </Container>
  );
}
